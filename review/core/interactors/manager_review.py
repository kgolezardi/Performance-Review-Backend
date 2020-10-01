from core.enums import Phase
from core.interactors.settings import is_at_phase
from core.models import ManagerPersonReview, ManagerProjectComment


def can_manager_review(user, reviewee):
    if not user.is_authenticated:
        return False

    if is_at_phase(Phase.MANAGER_REVIEW):
        if user == reviewee.manager:
            return True
        return False
    return False


def save_manager_person_review(reviewee, manager, **kwargs):
    manager_person_review = get_or_create_manager_person_review(reviewee=reviewee, manager=manager)

    if manager_person_review is None:
        return None

    fields = ['sahabiness_rating', 'problem_solving_rating', 'execution_rating', 'thought_leadership_rating',
              'leadership_rating', 'presence_rating', 'overall_rating']
    for field in fields:
        value = kwargs.get(field, None)
        if value is not None:
            manager_person_review.__setattr__(field, value)

    manager_person_review.save()
    return manager_person_review


def save_manager_project_comment(project_review, manager, **kwargs):
    manager_project_comment = get_or_create_manager_project_comment(project_review=project_review, manager=manager)

    if manager_project_comment is None:
        return None

    rating = kwargs.get('rating', None)
    if rating is not None:
        manager_project_comment.rating = rating

    manager_project_comment.save()
    return manager_project_comment


def get_all_manager_person_reviews(user):
    if not user.is_authenticated:
        return ManagerPersonReview.objects.none()
    if is_at_phase(Phase.MANAGER_REVIEW):
        return ManagerPersonReview.objects.filter(manager=user)
    return ManagerPersonReview.objects.none()


def get_all_manager_project_comments(user):
    if not user.is_authenticated:
        return ManagerPersonReview.objects.none()
    if is_at_phase(Phase.MANAGER_REVIEW):
        return ManagerPersonReview.objects.filter(manager=user)
    return ManagerPersonReview.objects.none()


def get_or_create_manager_person_review(*, reviewee, manager):
    if not can_manager_review(manager, reviewee):
        return None
    manager_person_review, _ = ManagerPersonReview.objects.get_or_create(reviewee=reviewee, manager=manager)
    return manager_person_review


def get_or_create_manager_project_comment(project_review, manager):
    if not can_manager_review(manager, project_review.reviewee):
        return None
    project_comment, _ = ManagerProjectComment.objects.get_or_create(project_review=project_review, manager=manager)
    return project_comment


def get_manager_person_review(user, id):
    try:
        return get_all_manager_person_reviews(user).get(id=id)
    except ManagerPersonReview.DoesNotExist:
        return None


def get_manager_project_comment(user, id):
    try:
        return get_all_manager_project_comments(user).get(id=id)
    except ManagerProjectComment.DoesNotExist:
        return None
