from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user_message', 'ai_reply')
    list_filter = ('created_at',)
    search_fields = ('user_message',)