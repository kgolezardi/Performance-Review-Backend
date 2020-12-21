from django.db import IntegrityError

from accounts.models import User
from core.enums import Phase, State
from core.interactors.authorization import can_participate
from core.interactors.person_review import get_all_person_reviews, get_user_person_reviews
from core.interactors.project_review import get_all_project_reviews, get_users_to_review
from core.interactors.settings import is_at_phase
from core.models import PersonReview


def change_password(user, old_password, new_password):
    # TODO validate password
    if user.is_authenticated and user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return True
    return False


def get_all_users(user):
    if user.is_authenticated:
        return User.objects.filter(is_staff=False, is_active=True)
    return User.objects.none()


def is_valid_user(user):
    return user in get_all_users(user)


def get_user(user, id):
    return get_all_users(user).get(id=id)


def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def add_user(username, password, first_name, last_name, email, employee_id):
    user = get_user_by_username(username)
    if user is not None:
        return 0
    user = User(username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                employee_id=employee_id)
    user.set_password(password)

    try:
        user.save()
        return 1
    except IntegrityError:
        return -1


def set_user_manager(username, manager_username):
    user = get_user_by_username(username)
    manager = get_user_by_username(manager_username)
    if user is None or manager is None:
        return False
    user.manager = manager
    user.save()
    return True


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
