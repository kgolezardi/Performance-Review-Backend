from core.enums import Phase
from core.interactors.settings import is_at_phase, get_active_round
from core.models import ProjectReview


def can_participate(user, review_round=None):
    review_round = review_round or get_active_round()
    return user in review_round.participants.all()


def is_project_available(project, review_round=None):
    review_round = review_round or get_active_round()
    return project in review_round.projects.all()


def can_review_person(user, reviewee):
    if not user.is_authenticated:
        return False

    if not can_participate(user, get_active_round()):
        return False
    if not can_participate(reviewee, get_active_round()):
        return False

    if is_at_phase(Phase.SELF_REVIEW):
        if user == reviewee:
            return True
        return False

    if is_at_phase(Phase.PEER_REVIEW):
        if ProjectReview.objects.filter(reviewee=reviewee, reviewers=user).exists():
            return True
        return False
    return False


def can_review_project(user, project):
    if not user.is_authenticated:
        return False

    if not can_participate(user, get_active_round()):
        return False

    if not is_project_available(project, get_active_round()):
        return False

    if not is_at_phase(Phase.SELF_REVIEW):
        return False
    return True


def can_delete_project_review(user, project_review):
    if not user.is_authenticated:
        return False

    if project_review.reviewee != user:
        return False

    if project_review.round != get_active_round():
        return False

    if not is_at_phase(Phase.SELF_REVIEW):
        return False
    return True


def can_comment_on_project_review(user, project_review):
    if not user.is_authenticated:
        return False

    if not is_at_phase(Phase.PEER_REVIEW):
        return False

    if not can_participate(user, get_active_round()):
        return False

    if project_review.round != get_active_round():
        return False

    if user not in project_review.reviewers.all():
        return False
    return True


def can_manager_review_person(user, reviewee):
    if not user.is_authenticated:
        return False

    if not can_participate(user, get_active_round()):
        return False
    if not can_participate(reviewee, get_active_round()):
        return False

    if is_at_phase(Phase.MANAGER_REVIEW):
        if user == reviewee.manager:
            return True
        return False
    return False


def can_manager_comment_on_project_review(user, project_review):
    if not user.is_authenticated:
        return False

    if not is_at_phase(Phase.MANAGER_REVIEW):
        return False

    if not can_participate(user, get_active_round()):
        return False

    if project_review.round != get_active_round():
        return False

    if user != project_review.reviewee.manager:
        return False
    return True


def can_view_ranking(manager, user):
    if not user.is_authenticated:
        return False

    if not is_at_phase(Phase.MANAGER_REVIEW):
        return False

    if manager != user.manager:
        return False
    return True


def can_view_manager_overall_review_text(user):
    if not user.is_authenticated:
        return False

    if not is_at_phase(Phase.MANAGER_REVIEW):
        return False

    if not user.is_manager:
        return False
    return True
