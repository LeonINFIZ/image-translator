from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import LANGUAGE_CHOICES


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label="Виберіть зображення для перекладу",
        help_text="Підтримуються формати PNG, JPG та ін.",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        initial="uk",
        label="Якою мовою перекласти?",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
