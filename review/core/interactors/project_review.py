from core.models import ProjectReview


def save_project_review(project, reviewee, **kwargs):
    project_review, created = get_or_create_project_review(project=project, reviewee=reviewee)

    if project_review is None:
        return None

    fields = ['text', 'rating']
    for field in fields:
        value = kwargs.get(field, None)
        if value is not None:
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
    # TODO: need improvement based on current phase
    # TODO: all project reviews include the ones the user is mentioned in [| Q(reviewers=user)]
    # TODO: needs integration with front-end
    return ProjectReview.objects.filter(reviewee=user)


def get_or_create_project_review(project, reviewee):
    # TODO: need improvement based on current phase
    if not reviewee.is_authenticated:
        return None
    project_review, created = ProjectReview.objects.get_or_create(project=project, reviewee=reviewee)
    return project_review


def get_project_review(user, id):
    try:
        return get_all_project_reviews(user).get(id=id)
    except ProjectReview.DoesNotExist:
        return None
