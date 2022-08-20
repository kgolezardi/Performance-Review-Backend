from accounts.models import User
from core.enums import Phase
from core.interactors.authorization import can_create_project_review, can_alter_project_review, \
    can_adjust_project_review
from core.interactors.settings import is_at_phase, get_active_round
from core.interactors.utils import filter_query_set_for_manager_review, set_review_answers
from core.models import ProjectReview


def create_project_review(project_name, reviewee):
    if not can_create_project_review(reviewee):
        return None
    if not project_name:
        return None

    project_review, created = ProjectReview.objects.get_or_create(
        round=get_active_round(),
        project_name=project_name,
        reviewee=reviewee
    )

    if not created:
        return None
    return project_review


def set_project_review_reviewers(project_review, reviewers):
    if reviewers is not None:
        reviewers = reviewers[:project_review.round.max_reviewers]
        project_review.reviewers.clear()
        for reviewer in reviewers:
            if reviewer == project_review.reviewee:
                continue
            if reviewer == project_review.reviewee.manager:
                continue
            if reviewer not in project_review.round.participants.all():
                continue
            project_review.reviewers.add(reviewer)


def edit_project_review(project_review, reviewee, **kwargs):
    if not can_alter_project_review(reviewee, project_review):
        return None

    project_name = kwargs.get('project_name', None)
    if project_name and project_name != project_review.project_name:
        if ProjectReview.objects.filter(
                round=project_review.round,
                project_name=project_name,
                reviewee=reviewee
        ).exists():
            return None
        project_review.project_name = project_name

    if 'rating' in kwargs:
        rating = kwargs.get('rating')
        project_review.rating = rating

    answers = kwargs.get('answers', None)
    set_review_answers(project_review, answers, project_review.round.self_review_project_questions.all())

    reviewers = kwargs.get('reviewers', None)
    set_project_review_reviewers(project_review, reviewers)

    if 'consulted_with_manager' in kwargs:
        project_review.consulted_with_manager = kwargs.get('consulted_with_manager')

    project_review.save()
    return project_review


def adjust_project_review(project_review, manager, **kwargs):
    if not can_adjust_project_review(manager, project_review):
        return None

    reviewers = kwargs.get('reviewers', None)
    set_project_review_reviewers(project_review, reviewers)

    if 'approved_by_manager' in kwargs:
        project_review.approved_by_manager = kwargs.get('approved_by_manager')

    project_review.save()
    return project_review


def get_all_project_reviews(user):
    if not user.is_authenticated:
        return ProjectReview.objects.none()
    if is_at_phase(Phase.SELF_REVIEW):
        return ProjectReview.objects.filter(round=get_active_round(), reviewee=user)
    if is_at_phase(Phase.MANAGER_ADJUSTMENT):
        qs = ProjectReview.objects.filter(round=get_active_round())
        return filter_query_set_for_manager_review(user, qs, 'reviewee')
    if is_at_phase(Phase.PEER_REVIEW):
        return ProjectReview.objects.filter(round=get_active_round(), reviewers=user)
    if is_at_phase(Phase.MANAGER_REVIEW):
        qs = ProjectReview.objects.filter(round=get_active_round())
        return filter_query_set_for_manager_review(user, qs, 'reviewee')
    if is_at_phase(Phase.RESULTS):
        return ProjectReview.objects.filter(round=get_active_round(), reviewee=user)
    return ProjectReview.objects.none()


def get_user_project_reviews(user, reviewee):
    return get_all_project_reviews(user).filter(reviewee=reviewee)


def get_project_review(user, id):
    try:
        return get_all_project_reviews(user).get(id=id)
    except ProjectReview.DoesNotExist:
        return None


def delete_project_review(user, project_review):
    if not can_alter_project_review(user, project_review):
        return None

    project_review_id = project_review.id
    project_review.delete()
    return project_review_id


def get_users_to_review(user):
    if not user.is_authenticated:
        return User.objects.none()
    if is_at_phase(Phase.MANAGER_REVIEW) or is_at_phase(Phase.MANAGER_ADJUSTMENT):
        qs = User.objects.filter(round=get_active_round())
        return filter_query_set_for_manager_review(user, qs)
    if is_at_phase(Phase.PEER_REVIEW):
        return User.objects.filter(
            projectreview__reviewers=user,
            projectreview__round=get_active_round()
        ).distinct()
    return User.objects.none()


def get_project_review_reviewers(project_review):
    if is_at_phase(Phase.SELF_REVIEW) or is_at_phase(Phase.MANAGER_ADJUSTMENT) or \
            is_at_phase(Phase.MANAGER_REVIEW) or is_at_phase(Phase.RESULTS):
        return project_review.reviewers.all()
    return User.objects.none()


def get_project_review_rating(project_review):
    # We may decide to not show reviewee's rating in peer review to their peers
    return project_review.rating


def get_project_review_answers(project_review):
    if is_at_phase(Phase.PEER_REVIEW):
        return project_review.answers.filter(question__private_answer_to_peer_reviewers=False)
    return project_review.answers.all()
