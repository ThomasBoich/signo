from django.contrib import admin

# Register your models here.
from documents.models import Document, DocumentType


class DocumentAdmin(admin.ModelAdmin):
    exclude = ('sender', 'sender_status', 'recipient_status')
    list_display = ('type', 'sender', 'recipient', 'send_date', 'sender_status', 'recipient_status')
    search_fields = ('type', 'sender', 'recipient', 'send_date', 'sender_status', 'recipient_status')
    list_editable = ('sender_status', 'recipient_status')
    readonly_fields = ('id', 'document', 'sender_status', 'recipient_status')

    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:
    #         obj.sender = request.user
    #     super().save_model(request, obj, form, change)


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentType)