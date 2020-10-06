from core.interactors.settings import get_active_round
from core.models import Project


def get_all_projects(user):
    if not user.is_authenticated:
        return Project.objects.none()
    return Project.objects.filter(round=get_active_round())


def get_project(user, id):
    try:
        return get_all_projects(user).get(id=id)
    except Project.DoesNotExist:
        return None
