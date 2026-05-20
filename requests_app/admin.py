from django.contrib import admin
from .models import TelegramUser, Request, Feedback


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'username',
        'telegram_id',
        'created_at'
    )

    search_fields = (
        'full_name',
        'username'
    )


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'user',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'title',
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'message',
        'created_at'
    )

    search_fields = (
        'message',
    )