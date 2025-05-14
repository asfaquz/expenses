from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        print("----- UsersConfig.ready() called -----")  # Debug line
        import user.signals
        # Ensure that the signals are imported and connected
        # when the app is ready. This is important for signal handling.
        # This will ensure that the signal handlers are registered
        # when the app is loaded, allowing them to respond to events.
        # For example, if you have a signal handler in signals.py,
        # it will be connected to the appropriate signal when the app is ready.


