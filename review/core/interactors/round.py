from core.models import Round


def get_all_rounds(user):
    if not user.is_authenticated:
        return Round.objects.none()
    return Round.objects.filter(participants=user)


def get_round(user, id):
    try:
        return get_all_rounds(user).get(id=id)
    except Round.DoesNotExist:
        return None

