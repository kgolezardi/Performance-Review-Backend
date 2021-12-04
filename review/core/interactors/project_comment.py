from core.enums import Phase
from core.interactors.authorization import can_comment_on_project_review, can_view_project_comment_reviewer
from core.interactors.person_review import save_person_review
from core.interactors.settings import is_at_phase, get_active_round
from core.interactors.utils import filter_query_set_for_manager_review
from core.models import ProjectComment, MAX_TEXT_LENGTH


def save_project_comment(project_review, reviewer, **kwargs):
    project_comment = get_or_create_project_comment(project_review=project_review, reviewer=reviewer)

    if project_comment is None:
        return None

    fields = ['text', 'rating']
    for field in fields:
        if field in kwargs:
            value = kwargs.get(field)
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
        return ProjectComment.objects.filter(
            project_review__round=get_active_round(),
            reviewer=user)
    if is_at_phase(Phase.MANAGER_REVIEW):
        qs = ProjectComment.objects.filter(project_review__round=get_active_round())
        return filter_query_set_for_manager_review(user, qs, 'project_review__reviewee')
    if is_at_phase(Phase.RESULTS):
        return ProjectComment.objects.filter(
            project_review__round=get_active_round(),
            project_review__reviewee=user
        )
    return ProjectComment.objects.none()


def get_project_review_comments(user, project_review):
    return get_all_project_comments(user).filter(project_review=project_review)


def get_project_comment(user, id):
    try:
        return get_all_project_comments(user).get(id=id)
    except ProjectComment.DoesNotExist:
        return None


def get_or_create_project_comment(project_review, reviewer):
    if not can_comment_on_project_review(reviewer, project_review):
        return None
    project_comment, created = ProjectComment.objects.get_or_create(
        project_review=project_review,
        reviewer=reviewer
    )
    return project_comment


def get_project_comment_reviewer(user, project_comment):
    if not can_view_project_comment_reviewer(user, project_comment):
        return None
    return project_comment.reviewer
