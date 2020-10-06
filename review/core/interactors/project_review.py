from accounts.models import User
from core.enums import Phase
from core.interactors.settings import is_at_phase
from core.models import ProjectReview, MAX_TEXT_LENGTH


def save_project_review(project, reviewee, **kwargs):
    project_review = get_or_create_project_review(project=project, reviewee=reviewee)

    if project_review is None:
        return None

    fields = ['text', 'rating']
    for field in fields:
        value = kwargs.get(field, None)
        if value is not None:
            if field in ['text']:
                value = value[:MAX_TEXT_LENGTH]
            project_review.__setattr__(field, value)

    reviewers = kwargs.get('reviewers', None)
    if reviewers is not None:
        if reviewee in reviewers:
            reviewers.remove(reviewee)

        project_review.reviewers.clear()
        for reviewer in reviewers:
            project_review.reviewers.add(reviewer)

    project_review.save()
    return project_review


def get_all_project_reviews(user):
    if not user.is_authenticated:
        return ProjectReview.objects.none()
    if is_at_phase(Phase.SELF_REVIEW):
        return ProjectReview.objects.filter(reviewee=user)
    if is_at_phase(Phase.PEER_REVIEW):
        return ProjectReview.objects.filter(reviewers=user)
    if is_at_phase(Phase.MANAGER_REVIEW):
        return ProjectReview.objects.filter(reviewee__manager=user)
    if is_at_phase(Phase.RESULTS):
        return ProjectReview.objects.filter(reviewee=user)
    return ProjectReview.objects.none()


def get_user_project_reviews(user, reviewee):
    return get_all_project_reviews(user).filter(reviewee=reviewee)


def get_or_create_project_review(project, reviewee):
    if not reviewee.is_authenticated:
        return None

    if not is_at_phase(Phase.SELF_REVIEW):
        return None

    project_review, created = ProjectReview.objects.get_or_create(project=project, reviewee=reviewee)
    return project_review


def get_project_review(user, id):
    try:
        return get_all_project_reviews(user).get(id=id)
    except ProjectReview.DoesNotExist:
        return None


def delete_project_review(user, project_review):
    if not user.is_authenticated:
        return None

    if project_review.reviewee != user:
        return None

    if not is_at_phase(Phase.SELF_REVIEW):
        return None

    project_review_id = project_review.id
    project_review.delete()
    return project_review_id


def get_users_to_review(user):
    if not user.is_authenticated:
        return User.objects.none()
    if is_at_phase(Phase.MANAGER_REVIEW):
        return User.objects.filter(manager=user)
    if is_at_phase(Phase.PEER_REVIEW):
        return User.objects.filter(projectreview__reviewers=user).distinct()
    return User.objects.none()


def get_project_review_reviewers(project_review):
    if not is_at_phase(Phase.SELF_REVIEW):
        return User.objects.none()
    return project_review.reviewers.all()
