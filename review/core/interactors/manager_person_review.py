from core.enums import Phase
from core.interactors.authorization import can_view_manager_person_review, can_write_manager_person_review
from core.interactors.settings import is_at_phase, get_active_round
from core.interactors.utils import filter_query_set_for_manager_review
from core.models import ManagerPersonReview, MAX_TEXT_LENGTH


def save_manager_person_review(reviewee, manager, **kwargs):
    manager_person_review = get_or_create_manager_person_review(reviewee=reviewee, user=manager)

    if manager_person_review is None:
        return None

    if not can_write_manager_person_review(manager, reviewee):
        return None

    fields = ['overall_rating', 'strengths', 'weaknesses']
    for field in fields:
        if field in kwargs:
            value = kwargs.get(field)
            if field in ['strengths', 'weaknesses']:
                value = list(map(lambda v: v[:MAX_TEXT_LENGTH], value[:3]))
            manager_person_review.__setattr__(field, value)

    manager_person_review.save()
    return manager_person_review


def get_all_manager_person_reviews(user):
    if not user.is_authenticated:
        return ManagerPersonReview.objects.none()
    if is_at_phase(Phase.MANAGER_REVIEW):
        qs = ManagerPersonReview.objects.filter(round=get_active_round())
        return filter_query_set_for_manager_review(user, qs, 'reviewee')
    if is_at_phase(Phase.RESULTS):
        return ManagerPersonReview.objects.filter(round=get_active_round(), reviewee=user)
    return ManagerPersonReview.objects.none()


def get_or_create_manager_person_review(*, reviewee, user):
    if not can_view_manager_person_review(user, reviewee):
        return None
    try:
        manager_person_review = ManagerPersonReview.objects.get(
            round=get_active_round(),
            reviewee=reviewee,
        )
    except ManagerPersonReview.DoesNotExist:
        if not can_write_manager_person_review(user, reviewee):
            return None
        manager_person_review = ManagerPersonReview.objects.create(
            round=get_active_round(),
            reviewee=reviewee,
        )
    return manager_person_review


def get_manager_person_review(user, id):
    try:
        return get_all_manager_person_reviews(user).get(id=id)
    except ManagerPersonReview.DoesNotExist:
        return None
