from django.db import IntegrityError

from accounts.models import User


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
    if user is None:
        return False
    if manager_username == '-':
        manager = None
    else:
        manager = get_user_by_username(manager_username)
        if manager is None:
            return False
    user.manager = manager
    user.save()
    return True


def set_user_rankings(username, ranking1, ranking2):
    user = get_user_by_username(username)
    if user is None:
        return False
    user.ranking1 = ranking1
    user.ranking2 = ranking2
    user.save()
    return True


def is_manager(user):
    return User.objects.filter(manager=user).exists()


def is_manager_or_hr(user):
    return user.is_hr or is_manager(user)


def is_manager_of_user_or_hr(*, manager, user):
    if manager.is_hr:
        return True
    if user.manager == manager:
        return True
    return False
