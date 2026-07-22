from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class ShortURL(models.Model):
    """A shortened URL, optionally owned by a logged-in user."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="short_urls",
        null=True,
        blank=True,
        help_text="Null for links created by anonymous users.",
    )
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=20, unique=True, db_index=True)
    is_custom_alias = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    @property
    def is_expired(self):
        return bool(self.expires_at and self.expires_at <= timezone.now())

    @property
    def is_usable(self):
        return self.is_active and not self.is_expired

    @property
    def click_count(self):
        return self.clicks.count()

    def get_short_path(self):
        return reverse("redirect_short_url", kwargs={"short_code": self.short_code})

    def get_absolute_short_url(self):
        from django.conf import settings as django_settings

        return f"{django_settings.SITE_DOMAIN}{self.get_short_path()}"


class ClickEvent(models.Model):
    """A single click/visit recorded against a ShortURL."""

    short_url = models.ForeignKey(
        ShortURL, on_delete=models.CASCADE, related_name="clicks"
    )
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    referrer = models.CharField(max_length=1024, blank=True)

    class Meta:
        ordering = ["-clicked_at"]

    def __str__(self):
        return f"Click on {self.short_url.short_code} at {self.clicked_at:%Y-%m-%d %H:%M}"
