from core.enums import Phase
from core.interactors.settings import is_at_phase


def can_manager_review(user, reviewee):
    if not user.is_authenticated:
        return False

    if is_at_phase(Phase.MANAGER_REVIEW):
        if user == reviewee.manager:
            return True
        return False
    return False
