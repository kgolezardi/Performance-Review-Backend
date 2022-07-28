import csv
from collections import defaultdict

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

from core.models import Settings, PersonReview, ProjectReview


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
    return render(request=request, template_name='reporting/self-review.html', context={
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
            has_answerd = []
            for question in selected_round.self_review_project_questions.filter(required=True):
                answer_qs = project_review.answers.filter(question=question)
                if answer_qs.exists():
                    has_answerd.append(bool(answer_qs.get().value))
                else:
                    has_answerd.append(False)
            has_answerd_all = all(has_answerd)
            consulted_with_manager = project_review.consulted_with_manager

            if has_rating and has_answerd_all and consulted_with_manager:
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
