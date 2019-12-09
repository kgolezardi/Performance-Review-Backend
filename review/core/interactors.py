from core.models import PersonReview, ProjectComment


def can_review(reviewer, reviewee):
    if reviewer == reviewee:
        return True
    try:
        ProjectComment.objects.get(project_review__reviewee=reviewee, reviewer=reviewer)
    except ProjectComment.DoesNotExist:
        return False
    return True


def save_person_review(reviewee, reviewer, **kwargs):
    if not can_review(reviewer, reviewee):
        return None

    person_review, created = PersonReview.objects.get_or_create(reviewee=reviewee, reviewer=reviewer)

    fields = ['sahabiness_rating', 'sahabiness_comment', 'problem_solving_rating',
              'problem_solving_comment', 'execution_rating', 'execution_comment', 'thought_leadership_rating',
              'thought_leadership_comment', 'leadership_rating', 'leadership_comment', 'presence_rating',
              'presence_comment', 'strengths', 'weaknesses']
    for field in fields:
        value = kwargs.get(field, None)
        if value is not None:
            if field in ['strengths', 'weaknesses']:
                value = value[:3]

            person_review.__setattr__(field, value)

    person_review.save()
    return person_review
