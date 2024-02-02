from django.forms import ModelForm
from .models import Event
from django.contrib.auth.models import User

from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


from django.forms import ModelForm
from .models import Event
from django.contrib.auth.models import User

from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class EventForm(forms.Form):

    ev_topic = forms.CharField(
        max_length=100,
        label="Topic",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    ev_description = forms.CharField(
        max_length=500,
        label="Description",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        ),
    )
    ev_date = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            },
        ),
    )
    ev_start_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",
                "type": "time",
            },
        ),
    )
    ev_end_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",
                "type": "time",
            },
        ),
    )
