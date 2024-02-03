from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-indigo-500",
                "rows": "4",
                "placeholder": "Edit your bio...",
            }
        ),
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = ["bio"]
