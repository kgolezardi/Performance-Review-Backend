def filter_query_set_for_manager_review(viewer, query_set, reviewee_field=None):
    if viewer.is_hr:
        return query_set
    manager_field = '%s__manager' % reviewee_field if reviewee_field else 'manager'
    return query_set.filter(**{manager_field: viewer})


def set_review_answers(review, answers, valid_questions):
    if answers is not None:
        for question, value in answers:
            if question not in valid_questions:
                continue
            answer, _ = review.answers.get_or_create(question=question)
            answer.value = value
            answer.save()

        # Remove unwanted answers
        answered_questions = [question for question, _ in answers]
        review.answers.exclude(question__in=answered_questions).delete()
