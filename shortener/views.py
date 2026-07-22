from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import ShortenURLForm
from .models import ClickEvent, ShortURL
from .utils import generate_short_code


def home(request):
    """Landing page with the shorten form. Works for anonymous and logged-in users."""
    if request.method == "POST":
        form = ShortenURLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data["original_url"]
            custom_alias = form.cleaned_data["custom_alias"]
            expires_at = form.cleaned_data["expires_at"]

            short_code = custom_alias if custom_alias else generate_short_code()

            short_url = ShortURL.objects.create(
                owner=request.user if request.user.is_authenticated else None,
                original_url=original_url,
                short_code=short_code,
                is_custom_alias=bool(custom_alias),
                expires_at=expires_at,
            )
            return redirect("link_created", short_code=short_url.short_code)
    else:
        form = ShortenURLForm()

    return render(request, "shortener/home.html", {"form": form})


def link_created(request, short_code):
    """Confirmation page shown right after a link is created."""
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    return render(request, "shortener/link_created.html", {"short_url": short_url})


@require_http_methods(["GET"])
def redirect_short_url(request, short_code):
    """Resolve a short code to its original URL, logging a click on the way."""
    short_url = get_object_or_404(ShortURL, short_code=short_code)

    if not short_url.is_usable:
        return render(
            request,
            "shortener/link_unavailable.html",
            {"short_url": short_url},
            status=410 if short_url.is_expired else 404,
        )

    ClickEvent.objects.create(
        short_url=short_url,
        ip_address=_get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:512],
        referrer=request.META.get("HTTP_REFERER", "")[:1024],
    )
    return redirect(short_url.original_url)


@login_required
def dashboard(request):
    """List every link owned by the logged-in user, with click counts."""
    links = (
        ShortURL.objects.filter(owner=request.user)
        .annotate(total_clicks=Count("clicks"))
        .order_by("-created_at")
    )
    return render(request, "shortener/dashboard.html", {"links": links})


@login_required
def link_stats(request, short_code):
    """Detailed click history for a single link, owner-only."""
    short_url = get_object_or_404(ShortURL, short_code=short_code, owner=request.user)
    clicks = short_url.clicks.all()[:200]
    return render(
        request,
        "shortener/link_stats.html",
        {"short_url": short_url, "clicks": clicks},
    )


@login_required
@require_http_methods(["POST"])
def toggle_link_active(request, short_code):
    """Enable/disable a link without deleting it."""
    short_url = get_object_or_404(ShortURL, short_code=short_code, owner=request.user)
    short_url.is_active = not short_url.is_active
    short_url.save(update_fields=["is_active"])
    messages.success(
        request,
        f"Link '{short_url.short_code}' is now {'active' if short_url.is_active else 'disabled'}.",
    )
    return redirect("dashboard")


@login_required
@require_http_methods(["POST"])
def delete_link(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code, owner=request.user)
    short_url.delete()
    messages.success(request, f"Link '{short_code}' was deleted.")
    return redirect("dashboard")


def _get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
