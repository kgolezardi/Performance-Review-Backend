from accounts.interactors.user import is_manager_of_user_or_hr, is_manager_or_hr
from core.enums import Phase
from core.interactors.settings import is_at_phase, get_active_round
from core.models import ProjectReview


def can_participate(user, review_round=None):
    review_round = review_round or get_active_round()
    return user in review_round.participants.all() or user.is_hr


def can_view_self_person_review(user, reviewee):
    if not user.is_authenticated:
        return False

    if not can_participate(user, get_active_round()):
        return False
    if not can_participate(reviewee, get_active_round()):
        return False

    if is_at_phase(Phase.SELF_REVIEW) or is_at_phase(Phase.RESULTS):
        if user == reviewee:
            return True
        return False

    if is_at_phase(Phase.MANAGER_ADJUSTMENT) or is_at_phase(Phase.MANAGER_REVIEW):
        if user == reviewee.manager:
            return True
        return False
    return False


def can_view_peer_person_review(user, reviewee):
    if not user.is_authenticated:
        return False

    if not can_participate(user, get_active_round()):
        return False
    if not can_participate(reviewee, get_active_round()):
        return False

    if is_at_phase(Phase.PEER_REVIEW):
        if ProjectReview.objects.filter(round=get_active_round(), reviewee=reviewee, reviewers=user).exists():
            return True
        return False
    return False


def can_write_person_review(user, reviewee):
    if is_at_phase(Phase.SELF_REVIEW):
        if can_view_self_person_review(user, reviewee) and user == reviewee:
            return True
        return False

    if is_at_phase(Phase.PEER_REVIEW):
        if can_view_peer_person_review(user, reviewee):
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

    active_round = get_active_round()
    if ProjectReview.objects.filter(round=active_round, reviewee=user).count() >= active_round.max_project_reviews:
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


def can_adjust_project_review(user, project_review):
    if not user.is_authenticated:
        return False

    if project_review.reviewee.manager != user:
        return False

    if project_review.round != get_active_round():
        return False

    if not is_at_phase(Phase.MANAGER_ADJUSTMENT):
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
        if not is_manager_of_user_or_hr(manager=user, user=reviewee):
            return False
        return True

    if is_at_phase(Phase.RESULTS):
        if user != reviewee:
            return False
        return True
    return False


def can_write_manager_person_review(user, reviewee):
    if not can_view_manager_person_review(user, reviewee):
        return False

    if not is_at_phase(Phase.MANAGER_REVIEW):
        return False

    if reviewee.manager != user:
        return False
    return True


def can_view_manager_project_comment(user, project_review):
    if not user.is_authenticated:
        return False

    if not can_participate(user, get_active_round()):
        return False

    if project_review.round != get_active_round():
        return False

    if is_at_phase(Phase.MANAGER_REVIEW):
        if not is_manager_of_user_or_hr(manager=user, user=project_review.reviewee):
            return False
        return True

    if is_at_phase(Phase.RESULTS):
        if user != project_review.reviewee:
            return False
        return True
    return False


def can_write_manager_project_comment(user, project_review):
    if not can_view_manager_project_comment(user, project_review):
        return False

    if not is_at_phase(Phase.MANAGER_REVIEW):
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


def can_view_reviewer(user, reviewee, round):
    if round.reviewers_are_anonymous:
        if not is_at_phase(Phase.MANAGER_REVIEW):
            return False
        if not is_manager_of_user_or_hr(manager=user, user=reviewee):
            return False
        return True
    return True


def can_view_person_review_reviewer(user, person_review):
    return can_view_reviewer(user, person_review.reviewee, person_review.round)


def can_view_project_comment_reviewer(user, project_comment):
    return can_view_reviewer(user, project_comment.project_review.reviewee, project_comment.project_review.round)
