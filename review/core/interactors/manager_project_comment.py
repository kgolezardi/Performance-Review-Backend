from core.enums import Phase
from core.interactors.authorization import can_view_manager_project_comment, can_write_manager_project_comment
from core.interactors.settings import is_at_phase, get_active_round
from core.interactors.utils import filter_query_set_for_manager_review, set_review_answers
from core.models import ManagerProjectComment


def save_manager_project_comment(project_review, manager, **kwargs):
    manager_project_comment = get_or_create_manager_project_comment(project_review=project_review, user=manager)

    if manager_project_comment is None:
        return None

    if not can_write_manager_project_comment(manager, project_review):
        return None

    if 'rating' in kwargs:
        rating = kwargs.get('rating')
        manager_project_comment.rating = rating

    answers = kwargs.get('answers', None)
    set_review_answers(manager_project_comment, answers,
                       manager_project_comment.project_review.round.manager_review_project_questions.all())

    manager_project_comment.save()
    return manager_project_comment


def get_all_manager_project_comments(user):
    if not user.is_authenticated:
        return ManagerProjectComment.objects.none()
    if is_at_phase(Phase.MANAGER_REVIEW):
        qs = ManagerProjectComment.objects.filter(project_review__round=get_active_round())
        return filter_query_set_for_manager_review(user, qs, 'project_review__reviewee')
    if is_at_phase(Phase.RESULTS):
        return ManagerProjectComment.objects.filter(
            project_review__round=get_active_round(),
            project_review__reviewee=user,
        )
    return ManagerProjectComment.objects.none()


def get_or_create_manager_project_comment(project_review, user):
    if not can_view_manager_project_comment(user, project_review):
        return None
    try:
        project_comment = ManagerProjectComment.objects.get(project_review=project_review)
    except ManagerProjectComment.DoesNotExist:
        if not can_write_manager_project_comment(user, project_review):
            return None
        project_comment = ManagerProjectComment.objects.create(project_review=project_review)
    return project_comment


def get_manager_project_comment(user, id):
    try:
        return get_all_manager_project_comments(user).get(id=id)
    except ManagerProjectComment.DoesNotExist:
        return None


def get_manager_project_comment_answers(manager_project_comment):
    # We may decide in the future to show some answers only to the manager or only to the reviewee
    if is_at_phase(Phase.MANAGER_REVIEW):
        return manager_project_comment.answers.all()
    return manager_project_comment.answers.filter(question__private_answer_to_reviewee=False)
