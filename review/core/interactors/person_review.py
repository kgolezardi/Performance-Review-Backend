from django.db.models import Q

from core.models import PersonReview, ProjectReview


def can_review_person(user, reviewee):
    # TODO: need improvement based on current phase
    if not user.is_authenticated:
        return False

    if user == reviewee:
        return True

    try:
        ProjectReview.objects.get(reviewee=reviewee, reviewers=user)
    except ProjectReview.DoesNotExist:
        return False
    return True


def save_person_review(reviewee, reviewer, **kwargs):
    person_review = get_or_create_person_review(reviewee=reviewee, reviewer=reviewer)

    if person_review is None:
        return None

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


def get_all_person_reviews(user):
    # TODO: need improvement based on current phase
    # TODO: all project reviews include the ones the user is mentioned in [| Q(reviewee=user)]
    return PersonReview.objects.filter(reviewer=user)


def get_or_create_person_review(*, reviewee, reviewer):
    if not can_review_person(reviewer, reviewee):
        return None

    person_review, created = PersonReview.objects.get_or_create(reviewee=reviewee, reviewer=reviewer)
    return person_review


def get_person_review(user, id):
    try:
        return get_all_person_reviews(user).get(id=id)
    except PersonReview.DoesNotExist:
        return None
