from core.enums import Phase
from core.interactors.authorization import can_view_manager_project_comment, can_write_manager_project_comment
from core.interactors.settings import is_at_phase, get_active_round
from core.interactors.utils import filter_query_set_for_manager_review
from core.models import ManagerProjectComment


def save_manager_project_comment(project_review, manager, **kwargs):
    manager_project_comment = get_or_create_manager_project_comment(project_review=project_review, manager=manager)

    if manager_project_comment is None:
        return None

    if not can_write_manager_project_comment(manager, project_review):
        return None

    rating = kwargs.get('rating', None)
    if rating is not None:
        manager_project_comment.rating = rating

    manager_project_comment.save()
    return manager_project_comment


def get_all_manager_project_comments(user):
    if not user.is_authenticated:
        return ManagerProjectComment.objects.none()
    if is_at_phase(Phase.MANAGER_REVIEW):
        qs = ManagerProjectComment.objects.filter(project_review__round=get_active_round())
        return filter_query_set_for_manager_review(user, qs, 'project_review__reviewee')
    return ManagerProjectComment.objects.none()


def get_or_create_manager_project_comment(project_review, manager):
    if not can_view_manager_project_comment(manager, project_review):
        return None
    project_comment, _ = ManagerProjectComment.objects.get_or_create(project_review=project_review)
    return project_comment


def get_manager_project_comment(user, id):
    try:
        return get_all_manager_project_comments(user).get(id=id)
    except ManagerProjectComment.DoesNotExist:
        return None
