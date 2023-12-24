from django.contrib import admin

from .models import MultiToken


class MultiTokenAdmin(admin.ModelAdmin):
    list_display = ["key", "user", "is_active", "created"]
    list_filter = ["is_active"]
    fields = ["user", "is_active"]
    ordering = ["-created"]


admin.site.register(MultiToken, MultiTokenAdmin)
