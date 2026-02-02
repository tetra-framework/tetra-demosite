from django.apps import AppConfig


class DemoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "demo"

    def ready(self):
        from tetra.registry import channels_group_registry

        channels_group_registry.register("notifications.news.headline")
