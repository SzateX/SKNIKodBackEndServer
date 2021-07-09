from dynamic_preferences.types import BooleanPreference, StringPreference, IntegerPreference, ChoicePreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry

general = Section('general')


@global_preferences_registry.register
class SiteTitle(StringPreference):
    section = general
    name = 'title'
    default = 'Studenckie Koło Naukowe Informatyków \"KOD\"'
    required = False


@global_preferences_registry.register
class RegistrationMode(BooleanPreference):
    section = general
    name = 'registration_mode'
    default = False


@global_preferences_registry.register
class DefaultPaginationCount(IntegerPreference):
    section = general
    name = 'default_items_on_page'
    default = 5
    required = False


@global_preferences_registry.register
class DefaultPageColor(ChoicePreference):
    section = general
    name = 'default_page_color'
    choices = [
        ('primary', 'primary'),
        ('secondary', 'secondary'),
        ('accent', 'accent'),
        ('success', 'success'),
        ('warning', 'warning'),
        ('error', 'error'),
        ('info', 'info'),
    ]
    default = 'primary'