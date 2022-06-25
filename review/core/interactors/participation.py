from core.enums import Phase
from core.interactors.authorization import can_participate
from core.interactors.settings import get_active_round, is_at_phase
from core.models import Participation


def get_or_create_participation(user, review_round):
    if not user.is_authenticated:
        return None
    if not can_participate(user, review_round):
        return None
    participation, _ = Participation.objects.get_or_create(user=user, round=review_round)
    return participation


def has_user_started(user):
    participation = get_or_create_participation(user, get_active_round())
    if participation is None:
        return None
    if is_at_phase(Phase.SELF_REVIEW):
        return participation.has_started_self_review
    if is_at_phase(Phase.MANAGER_ADJUSTMENT):
        return participation.has_started_manager_adjustment
    if is_at_phase(Phase.PEER_REVIEW):
        return participation.has_started_peer_review
    if is_at_phase(Phase.MANAGER_REVIEW):
        return participation.has_started_manager_review
    if is_at_phase(Phase.RESULTS):
        return participation.has_started_results
    return False


def start_review(user):
    participation = get_or_create_participation(user, get_active_round())
    if participation is None:
        return False
    if is_at_phase(Phase.SELF_REVIEW):
        participation.has_started_self_review = True
    if is_at_phase(Phase.MANAGER_ADJUSTMENT):
        participation.has_started_manager_adjustment = True
    elif is_at_phase(Phase.PEER_REVIEW):
        participation.has_started_peer_review = True
    elif is_at_phase(Phase.MANAGER_REVIEW):
        participation.has_started_manager_review = True
    elif is_at_phase(Phase.RESULTS):
        participation.has_started_results = True
    participation.save()
    return True
