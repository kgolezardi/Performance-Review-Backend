from core.enums import Phase, State
from core.interactors.authorization import can_participate
from core.interactors.person_review import get_all_person_reviews, get_user_person_reviews
from core.interactors.project_review import get_all_project_reviews, get_users_to_review
from core.interactors.settings import is_at_phase
from core.models import PersonReview


def get_person_review_progress(person_review):
    fields = ['sahabiness_rating', 'sahabiness_comment', 'problem_solving_rating', 'problem_solving_comment',
              'execution_rating', 'execution_comment', 'thought_leadership_rating', 'thought_leadership_comment',
              'leadership_rating', 'leadership_comment', 'presence_rating', 'presence_comment']
    empty_fileds, total_fields = 0, 0
    for field in fields:
        if not person_review.__getattribute__(field):
            empty_fileds += 1
        total_fields += 1

    performance_competencies = (total_fields - empty_fileds) / total_fields * 100
    dominant_characteristics = (len(person_review.strengths or []) + len(person_review.weaknesses or [])) / \
                               (PersonReview.strengths.field.size + PersonReview.weaknesses.field.size) * 100
    return {'performance_competencies': performance_competencies,
            'dominant_characteristics': dominant_characteristics}


def get_project_review_progress(project_review):
    text = 1 if project_review.text else 0
    rating = 1 if project_review.rating else 0
    reviewers = 1 if project_review.reviewers.all() else 0
    return (1 * rating + 6 * text + 3 * reviewers) / 10 * 100


def get_user_progress(user):
    if not can_participate(user):
        return None
    if is_at_phase(Phase.SELF_REVIEW):
        person_reviews = get_all_person_reviews(user)
        project_reviews = get_all_project_reviews(user)
        res = {'performance_competencies': 0,
               'dominant_characteristics': 0}
        if len(person_reviews) > 0:
            res = get_person_review_progress(person_reviews[0])

        project_reviews_progress = []
        for project_review in project_reviews:
            project_reviews_progress.append(get_project_review_progress(project_review))
        res['projects'] = project_reviews_progress

        return res
    if is_at_phase(Phase.PEER_REVIEW):
        res = []
        for peer in get_users_to_review(user):
            person_review_qs = get_user_person_reviews(user=user, reviewee=peer)
            if not person_review_qs:
                res.append((peer, State.TODO))
            else:
                res.append((peer, State(person_review_qs.get().state)))
        return res
    return None
