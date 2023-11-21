from django.apps import AppConfig


class StoreConfig(AppConfig):
    name = 'store'

    def ready(self):
        # Import and register your custom template tags or filters
        from templatetags import custom_filter
