from accounts.interactors.user import is_manager_of_user_or_hr, is_manager_or_hr
from core.enums import Phase
from core.interactors.settings import is_at_phase, get_active_round
from core.models import ProjectReview


def can_participate(user, review_round=None):
    review_round = review_round or get_active_round()
    return user in review_round.participants.all() or user.is_hr


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


def can_create_project_review(user):
    if not user.is_authenticated:
        return False

    if not can_participate(user, get_active_round()):
        return False

    if not is_at_phase(Phase.SELF_REVIEW):
        return False
    return True


def can_alter_project_review(user, project_review):
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


def can_view_manager_person_review(user, reviewee):
    if not user.is_authenticated:
        return False

    if not can_participate(user, get_active_round()):
        return False
    if not can_participate(reviewee, get_active_round()):
        return False

    if is_at_phase(Phase.MANAGER_REVIEW):
        if is_manager_of_user_or_hr(manager=user, user=reviewee):
            return True
    return False


def can_write_manager_person_review(user, reviewee):
    if not can_view_manager_person_review(user, reviewee):
        return False

    if reviewee.manager != user:
        return False
    return True


def can_view_manager_project_comment(user, project_review):
    if not user.is_authenticated:
        return False

    if not is_at_phase(Phase.MANAGER_REVIEW):
        return False

    if not can_participate(user, get_active_round()):
        return False

    if project_review.round != get_active_round():
        return False

    if not is_manager_of_user_or_hr(manager=user, user=project_review.reviewee):
        return False
    return True


def can_write_manager_project_comment(user, project_review):
    if not can_view_manager_project_comment(user, project_review):
        return False

    if project_review.reviewee.manager != user:
        return False
    return True


def can_view_ranking(manager, user):
    if not user.is_authenticated:
        return False

    if not is_at_phase(Phase.MANAGER_REVIEW):
        return False

    if not is_manager_of_user_or_hr(manager=manager, user=user):
        return False
    return True


def can_view_manager_overall_review_text(user):
    if not user.is_authenticated:
        return False

    if not is_at_phase(Phase.MANAGER_REVIEW):
        return False

    if not is_manager_or_hr(user):
        return False
    return True


def can_view_reviewer(user, reviewee):
    if not is_at_phase(Phase.MANAGER_REVIEW):
        return False
    if not is_manager_of_user_or_hr(manager=user, user=reviewee):
        return False
    return True


def can_view_person_review_reviewer(user, person_review):
    return can_view_reviewer(user, person_review.reviewee)


def can_view_project_comment_reviewer(user, project_comment):
    return can_view_reviewer(user, project_comment.project_review.reviewee)
