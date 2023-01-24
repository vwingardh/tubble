from django import forms
from app.models import Contact


class ContactForm(forms.ModelForm):
    """
    Form for user to contact Tubble
    """
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.Textarea()

    class Meta:
        model = Contact
        fields = (
            'first_name',
            'last_name',
            'email',
            'message'
        )
