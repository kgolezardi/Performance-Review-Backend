from core.models import Settings


def get_settings():
    return Settings.load()


def is_at_current_phase(phase):
    return get_settings().phase == phase.value
