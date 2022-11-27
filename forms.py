from django import forms

from documents.models import Document
from users.models import CustomUser


class SendDocumentForm(forms.ModelForm):
    # title = forms.EmailField(label='Название документа', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # document = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # recipient = forms.SelectMultiple()
    # type = forms.SelectMultiple()

    class Meta:
        model = Document
        # fields = '__all__''sender',
        fields = ['document', 'recipient', 'type', 'sender', 'founder']
        exclude = ['sender_status', 'recipient_status']