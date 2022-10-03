from django.contrib import admin

from .models import Chat,Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display=('__str__','get_last_message',)
@admin.register(Message)

class MessageAdmin(admin.ModelAdmin):
    list_display=('__str__','is_read','sender','get_sent_time','chat')
