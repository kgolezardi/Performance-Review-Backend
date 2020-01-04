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


def start_review(user):
    if user.is_authenticated:
        user.has_started = True
        user.save()
        return True
    return False


def add_user(username, password, first_name, last_name, email, employee_id, manager=None):
    print('adding', username)
    user = User(username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                employee_id=employee_id,
                manager=manager)
    user.set_password(password)

    try:
        user.save()
        return True
    except IntegrityError:
        return False

