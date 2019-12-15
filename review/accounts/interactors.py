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


def get_user(user, id):
    return get_all_users(user).get(id=id)
