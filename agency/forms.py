from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from agency.models import Newspaper, Redactor, Topic, Commentary


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = "__all__"


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=64,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"}),
    )


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=64,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ("content",)