from django.apps import AppConfig


class AdminDattaProConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_datta_pro'

    def ready(self):
        import admin_datta_pro.signals