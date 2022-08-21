import csv
from collections import defaultdict

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import User
from core.enums import State
from core.models import Settings, PersonReview, ProjectReview, ManagerPersonReview, ManagerProjectComment


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request=request, template_name='reporting/index.html')


@user_passes_test(lambda u: u.is_superuser)
def self_review_overview(request):
    detailed_report = create_self_review_report()
    managers_report = defaultdict(lambda: {'completed': 0, 'total': 0})
    for user in detailed_report:
        if not user.manager:
            continue
        if detailed_report[user]['completed']:
            managers_report[user.manager]['completed'] += 1
        managers_report[user.manager]['total'] += 1
    managers_report = dict(managers_report)
    return render(request=request, template_name='reporting/self_review.html', context={
        'report': managers_report,
    })


@user_passes_test(lambda u: u.is_superuser)
def self_review_detailed(request):
    detailed_report = create_self_review_report()
    response = HttpResponse(content_type='text/csv')
    response['Content-Desposition'] = 'attachment; filename="self-review.csv"'

    writer = csv.writer(response)
    writer.writerow(['Manager', 'Sahabi', 'Strengths', 'Weaknesses', 'Completed projects',
                     'Inomplete projects', 'Completed'])
    for user, data in detailed_report.items():
        writer.writerow([
            user.manager,
            user,
            data['strengths_count'],
            data['weaknesses_count'],
            data['completed_project_reviews_count'],
            data['incomplete_project_reviews_count'],
            data['completed'],
        ])
    return response


def create_self_review_report():
    report = {}
    selected_round = Settings.load().active_round
    participants = selected_round.participants.all()
    for user in participants:
        self_person_review_qs = PersonReview.objects.filter(
            round=selected_round,
            reviewee=user,
            reviewer=user,
        )
        if self_person_review_qs.exists():
            self_person_review = self_person_review_qs.get()
            strengths_count = len(self_person_review.strengths or [])
            weaknesses_count = len(self_person_review.weaknesses or [])
        else:
            strengths_count = weaknesses_count = 0

        project_reviews = ProjectReview.objects.filter(
            round=selected_round,
            reviewee=user,
        )
        completed_project_reviews_count = 0
        incomplete_project_reviews_count = 0
        for project_review in project_reviews:
            has_rating = bool(project_review.rating)
            has_answered_all = has_answered_all_required_questions(
                project_review,
                selected_round.self_review_project_questions.filter(required=True),
            )
            consulted_with_manager = project_review.consulted_with_manager

            if has_rating and has_answered_all and consulted_with_manager:
                completed_project_reviews_count += 1
            else:
                incomplete_project_reviews_count += 1

        completed = strengths_count > 0 and weaknesses_count > 0 and completed_project_reviews_count > 0 and \
            incomplete_project_reviews_count == 0
        report[user] = {
            'strengths_count': strengths_count,
            'weaknesses_count': weaknesses_count,
            'completed_project_reviews_count': completed_project_reviews_count,
            'incomplete_project_reviews_count': incomplete_project_reviews_count,
            'completed': completed,
        }
    return report


@user_passes_test(lambda u: u.is_superuser)
def manager_adjustment(request):
    selected_round = Settings.load().active_round
    manager_progress = defaultdict(lambda: {'completed': 0, 'total': 0})
    for project_review in ProjectReview.objects.filter(round=selected_round):
        manager = project_review.reviewee.manager
        if not manager:
            continue
        if project_review.approved_by_manager:
            manager_progress[manager]['completed'] += 1
        manager_progress[manager]['total'] += 1

    return render(request=request, template_name='reporting/manager_adjustment.html', context={
        'report': dict(manager_progress),
    })


@user_passes_test(lambda u: u.is_superuser)
def peer_review_overview(request):
    cutoff = int(request.GET.get('cutoff', 5))

    detailed_report = create_peer_review_report()
    managers_report = defaultdict(lambda: {
        'have_not_reviewed': [],
        'less_than_cutoff': [],
        'at_least_cutoff': [],
        'finished': [],
    })
    for user in detailed_report:
        if not user.manager:
            continue
        if len(detailed_report[user]['done']) == 0:
            managers_report[user.manager]['have_not_reviewed'].append(user.username)
        elif len(detailed_report[user]['todo']) == len(detailed_report[user]['doing']) == 0:
            managers_report[user.manager]['finished'].append(user.username)
        elif len(detailed_report[user]['done']) < cutoff:
            managers_report[user.manager]['less_than_cutoff'].append(user.username)
        elif len(detailed_report[user]['done']) >= cutoff:
            managers_report[user.manager]['at_least_cutoff'].append(user.username)
    return render(request=request, template_name='reporting/peer_review.html', context={
        'report': dict(managers_report),
        'cutoff': cutoff,
    })


@user_passes_test(lambda u: u.is_superuser)
def peer_review_detailed(request):
    detailed_report = create_peer_review_report()
    response = HttpResponse(content_type='text/csv')
    response['Content-Desposition'] = 'attachment; filename="peer-review.csv"'

    writer = csv.writer(response)
    writer.writerow(['Manager', 'Sahabi', 'ToDo (Reviewees)', 'Doing (Reviewees)', 'Done (Reviewees)'])
    for user, data in detailed_report.items():
        writer.writerow([
            user.manager,
            user,
            ' - '.join(map(lambda u: u.username, data['todo'])),
            ' - '.join(map(lambda u: u.username, data['doing'])),
            ' - '.join(map(lambda u: u.username, data['done'])),
        ])
    return response


def create_peer_review_report():
    report = defaultdict(lambda: {'todo': [], 'doing': [], 'done': []})
    selected_round = Settings.load().active_round
    participants = selected_round.participants.all()
    for user in participants:
        users_to_review = User.objects.filter(
            projectreview__reviewers=user,
            projectreview__round=selected_round
        ).distinct()
        for reviewee in users_to_review:
            person_review_qs = PersonReview.objects.filter(
                round=selected_round,
                reviewee=reviewee,
                reviewer=user,
            )
            if not person_review_qs.exists() or person_review_qs.get().state == State.TODO.value:
                report[user]['todo'].append(reviewee)
            elif person_review_qs.get().state == State.DOING.value:
                report[user]['doing'].append(reviewee)
            elif person_review_qs.get().state == State.DONE.value:
                report[user]['done'].append(reviewee)
    return dict(report)


@user_passes_test(lambda u: u.is_superuser)
def manager_review(request):
    detailed_report = create_manager_review_report()
    managers_report = defaultdict(lambda: {'completed': 0, 'total': 0})
    for user in detailed_report:
        if not user.manager:
            continue
        if detailed_report[user]:
            managers_report[user.manager]['completed'] += 1
        managers_report[user.manager]['total'] += 1
    managers_report = dict(managers_report)
    return render(request=request, template_name='reporting/manager_review.html', context={
        'report': managers_report,
    })


def create_manager_review_report():
    completed = {}
    selected_round = Settings.load().active_round
    participants = selected_round.participants.all()
    for user in participants:
        manager_person_review_qs = ManagerPersonReview.objects.filter(
            round=selected_round,
            reviewee=user,
        )
        if manager_person_review_qs.exists():
            manager_person_review = manager_person_review_qs.get()
            strengths_count = len(manager_person_review.strengths or [])
            weaknesses_count = len(manager_person_review.weaknesses or [])
            has_overall_rating = bool(manager_person_review.overall_rating)
        else:
            strengths_count = weaknesses_count = 0
            has_overall_rating = False

        project_reviews = ProjectReview.objects.filter(
            round=selected_round,
            reviewee=user,
        )
        incomplete_project_comments_count = 0
        for project_review in project_reviews:
            manager_project_comment_qs = ManagerProjectComment.objects.filter(project_review=project_review)
            if not manager_project_comment_qs.exists():
                incomplete_project_comments_count += 1
                continue
            manager_project_comment = manager_project_comment_qs.get()

            has_rating = bool(manager_project_comment.rating)
            has_answered_all = has_answered_all_required_questions(
                manager_project_comment,
                selected_round.manager_review_project_questions.filter(required=True),
            )

            if not has_rating or not has_answered_all:
                incomplete_project_comments_count += 1

        completed[user] = strengths_count > 0 and weaknesses_count > 0 and has_overall_rating and \
            incomplete_project_comments_count == 0
    return completed


def has_answered_all_required_questions(review, required_questions):
    has_answered = []
    for question in required_questions:
        answer_qs = review.answers.filter(question=question)
        if answer_qs.exists():
            has_answered.append(bool(answer_qs.get().value))
        else:
            has_answered.append(False)
    has_answered_all = all(has_answered)
    return has_answered_all
