# Django URL Shortener

A pure-Django URL shortener with click tracking, custom aliases, link expiration,
and a per-user dashboard. No DRF, no frontend framework — server-rendered templates only.

## Features
- Shorten any URL anonymously (no account required)
- Optional custom alias (validated against length, charset, and reserved words)
- Optional expiration date/time — expired links show a 410 page instead of redirecting
- Click tracking: timestamp, IP, user agent, referrer per click
- Dashboard (login required) listing your own links with click counts, enable/disable, delete
- Per-link stats page with recent click history
- Django built-in auth: signup, login, logout
- Django admin wired up for ShortURL and ClickEvent

## Project layout
```
urlshortener/
├── manage.py
├── requirements.txt
├── urlshortener/        # project settings, root urls
├── shortener/            # ShortURL + ClickEvent models, shorten/redirect/dashboard views
│   ├── models.py
│   ├── forms.py
│   ├── utils.py          # short code generation + alias validation
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/base.html + templates/shortener/*.html
│   └── static/shortener/css/style.css
└── accounts/             # signup view + Django's built-in LoginView/LogoutView
    ├── forms.py
    ├── views.py
    ├── urls.py
    └── templates/accounts/*.html
```

## Setup
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd urlshortener
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## Notes / next steps if you extend this
- `SITE_DOMAIN` in `settings.py` controls the domain used to build the full
  shareable short link (`get_absolute_short_url`) — update it for production.
- Short codes are 7 random alphanumeric characters; change `SHORT_CODE_LENGTH`
  in `shortener/utils.py` if you want shorter/longer codes.
- Reserved words that can't be used as custom aliases live in
  `RESERVED_CODES` in `shortener/utils.py` — add to this set if you add new
  top-level URL routes.
- `DEBUG = True` and the `SECRET_KEY` in `settings.py` are dev-only; replace
  both (and set `ALLOWED_HOSTS`) before deploying.
  
