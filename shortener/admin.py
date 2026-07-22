from django.contrib import admin

from .models import ClickEvent, ShortURL


class ClickEventInline(admin.TabularInline):
    model = ClickEvent
    extra = 0
    readonly_fields = ["clicked_at", "ip_address", "user_agent", "referrer"]
    can_delete = False
    max_num = 20


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ["short_code", "original_url", "owner", "click_count", "is_active", "is_expired", "created_at"]
    list_filter = ["is_active", "is_custom_alias"]
    search_fields = ["short_code", "original_url", "owner__username"]
    readonly_fields = ["created_at"]
    inlines = [ClickEventInline]


@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ["short_url", "clicked_at", "ip_address"]
    list_filter = ["clicked_at"]
    search_fields = ["short_url__short_code", "ip_address"]
