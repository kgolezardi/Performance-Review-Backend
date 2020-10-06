from core.enums import Phase
from core.interactors.authorization import can_manager_comment_on_project_review
from core.interactors.settings import is_at_phase
from core.models import ManagerProjectComment


def save_manager_project_comment(project_review, manager, **kwargs):
    manager_project_comment = get_or_create_manager_project_comment(project_review=project_review, manager=manager)

    if manager_project_comment is None:
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
        return ManagerProjectComment.objects.filter(manager=user)
    return ManagerProjectComment.objects.none()


def get_or_create_manager_project_comment(project_review, manager):
    if not can_manager_comment_on_project_review(manager, project_review):
        return None
    project_comment, _ = ManagerProjectComment.objects.get_or_create(
        project_review=project_review,
        manager=manager
    )
    return project_comment


def get_manager_project_comment(user, id):
    try:
        return get_all_manager_project_comments(user).get(id=id)
    except ManagerProjectComment.DoesNotExist:
        return None
