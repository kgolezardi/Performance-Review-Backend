from core.models import Settings


def get_settings():
    return Settings.load()


def is_at_phase(phase):
    return get_settings().active_round.phase == phase.value
