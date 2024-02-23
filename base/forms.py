from django.forms import ModelForm
from .models import Event
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"


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
    ev_location = forms.CharField(
        label="location",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
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


class DisplayForm(forms.Form):
    md_display = forms.ChoiceField(
        choices=[
            ("Default", "Default"),
            ("Display 2", "Display 2"),
            ("Display 3", "Display 3"),
            ("Display 4", "Display 4"),
            ("Display 5", "Display 5"),
            ("Display 6", "Display 6"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "style": "width: 40vw",
            }
        ),
    )


class LocationForm(forms.Form):
    lf_location = forms.CharField(
        label="Location",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "width: 40vw",
            }
        ),
    )


class NewsForm(forms.Form):
    nf_source = forms.ChoiceField(
        choices=[
            ("bbc_news", "BBC News"),
            ("cnn", "CNN News"),
            ("nbc_news", "NBC News"),
            ("abc_news", "ABC News"),
            ("the-washington-post", "The Washington Post"),
            ("espn", "ESPN"),
            ("associated-press", "Associated Press"),
        ],
        label="Sources",
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "style": "width: 40vw",
            }
        ),
    )
    nf_topic = forms.CharField(
        label="Topic",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "width: 40vw",
            }
        ),
    )
