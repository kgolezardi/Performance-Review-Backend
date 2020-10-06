from core.enums import Phase
from core.interactors.person_review import save_person_review
from core.interactors.settings import is_at_phase
from core.models import ProjectComment, MAX_TEXT_LENGTH


def can_review_project(user, project_review):
    if is_at_phase(Phase.PEER_REVIEW):
        return user in project_review.reviewers.all()
    return False


def save_project_comment(project_review, reviewer, **kwargs):
    project_comment = get_or_create_project_comment(project_review=project_review, reviewer=reviewer)

    if project_comment is None:
        return None

    fields = ['text', 'rating']
    for field in fields:
        value = kwargs.get(field, None)
        if value is not None:
            if field in ['text']:
                value = value[:MAX_TEXT_LENGTH]
            project_comment.__setattr__(field, value)

    project_comment.save()
    # save person review to update peer review state
    save_person_review(reviewee=project_review.reviewee, reviewer=reviewer)
    return project_comment


def get_all_project_comments(user):
    if not user.is_authenticated:
        return ProjectComment.objects.none()
    if is_at_phase(Phase.PEER_REVIEW):
        return ProjectComment.objects.filter(reviewer=user)
    if is_at_phase(Phase.MANAGER_REVIEW):
        return ProjectComment.objects.filter(project_review__reviewee__manager=user)
    if is_at_phase(Phase.RESULTS):
        return ProjectComment.objects.filter(project_review__reviewee=user)
    return ProjectComment.objects.none()


def get_project_review_comments(user, project_review):
    return get_all_project_comments(user).filter(project_review=project_review)


def get_project_comment(user, id):
    try:
        return get_all_project_comments(user).get(id=id)
    except ProjectComment.DoesNotExist:
        return None


def get_or_create_project_comment(project_review, reviewer):
    if not can_review_project(reviewer, project_review):
        return None
    project_comment, created = ProjectComment.objects.get_or_create(project_review=project_review, reviewer=reviewer)
    return project_comment


def get_project_comment_reviewer(user, project_comment):
    if not is_at_phase(Phase.MANAGER_REVIEW):
        return None
    if not user == project_comment.project_review.reviewee.manager:
        return None
    return project_comment.reviewer
