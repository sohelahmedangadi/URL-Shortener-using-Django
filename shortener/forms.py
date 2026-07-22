from django import forms
from django.utils import timezone

from .utils import validate_custom_alias


class ShortenURLForm(forms.Form):
    original_url = forms.URLField(
        label="Long URL",
        max_length=2048,
        widget=forms.URLInput(attrs={"placeholder": "https://example.com/a/very/long/link"}),
    )
    custom_alias = forms.CharField(
        label="Custom alias (optional)",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "my-link"}),
    )
    expires_at = forms.DateTimeField(
        label="Expires at (optional)",
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    def clean_custom_alias(self):
        alias = self.cleaned_data.get("custom_alias", "").strip()
        error = validate_custom_alias(alias)
        if error:
            raise forms.ValidationError(error)
        return alias

    def clean_expires_at(self):
        expires_at = self.cleaned_data.get("expires_at")
        if expires_at and expires_at <= timezone.now():
            raise forms.ValidationError("Expiration must be in the future.")
        return expires_at
