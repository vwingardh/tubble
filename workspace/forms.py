from django import forms
from .models import Destination


class DestinationCreateForm(forms.ModelForm):
    """
    Form for creating a Destination
    """
    user = forms.IntegerField(required=False)
    city = forms.CharField(max_length=150, required=True)
    country = forms.CharField(max_length=150, required=True)
    adventure_type = forms.CharField(
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-check",
                "name": "adventure_type"
            }
        )
    )
    climate = forms.CharField(
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-check",
                "name": "climate"
            }
        )
    )
    flight = forms.CharField(
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-check",
                "name": "flight"
            }
        )
    )
    notes = forms.Textarea()
    activity1 = forms.TextInput()
    activity2 = forms.TextInput()
    activity3 = forms.TextInput()
    activity4 = forms.TextInput()
    image = forms.ImageField(required=False)
    has_user_visited = forms.CheckboxInput()

    class Meta:
        model = Destination
        fields = [ 
            'city', 
            'country', 
            'adventure_type', 
            'climate', 
            'flight', 
            'notes',
            'activity1',
            'activity2',
            'activity3',
            'activity4', 
            'image',
            'has_user_visited'
        ]
        
     
class NextAdventureFilterForm(forms.Form):
    """
    Form for filtering destinations that meet the three
    criteria below.
    """
    adventure = forms.CharField(max_length=80, required=True)
    climate = forms.CharField(max_length=80, required=True)
    flight = forms.CharField(max_length=80, required=True)  

    class Meta:
        fields = [
            'adventure',
            'climate',
            'flight'
        ]
