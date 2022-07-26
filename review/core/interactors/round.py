from core.enums import Phase
from core.interactors.settings import is_at_phase
from core.models import Round


def get_all_rounds(user):
    if not user.is_authenticated:
        return Round.objects.none()
    return Round.objects.filter(participants=user)


def get_round(user, id):
    try:
        return get_all_rounds(user).get(id=id)
    except Round.DoesNotExist:
        return None


def get_self_review_project_questions(round):
    if is_at_phase(Phase.PEER_REVIEW):
        return round.self_review_project_questions.filter(private_answer_to_peer_reviewers=False)
    return round.self_review_project_questions.all()


def get_peer_review_project_questions(round):
    return round.peer_review_project_questions.all()


def get_manager_review_project_questions(round):
    if is_at_phase(Phase.MANAGER_REVIEW):
        return round.manager_review_project_questions.all()
    return round.manager_review_project_questions.filter(private_answer_to_reviewee=False)
