# text-utils

[![License](https://img.shields.io/badge/license-Unlicensed-lightgrey.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2.3-green)](https://www.djangoproject.com/)

**text-utils** (textutils.np) is a lightweight Django web application that provides an easy-to-use interface for cleaning and transforming text. It was created to address a common need: many students, writers, and professionals frequently work with blocks of text containing unwanted characters, inconsistent formatting, or excessive spaces. Instead of relying on multiple tools or manual edits, text-utils consolidates these operations into a single, accessible web interface.

This project demonstrates a full-stack Django deployment, integrating frontend components (Bootstrap-based layout, modals) with backend logic (form handling, email notifications) and deploy-friendly practices (environment-based configuration, SendGrid integration). It's especially useful for learners who want to understand how to build and deploy simple utility apps using Python and Django, as well as a practical tool for anyone needing quick text manipulation.

Built and maintained by **Dipesh Dhaurali**, it also includes informational About and Contact pages so visitors can reach out.

---

## 🚀 Features

- **Text manipulation tools**: remove punctuation, change case, strip newlines/whitespace, count characters.
- **About page**: personal and academic details rendered with responsive Bootstrap cards.
- **Contact page**: modal form that sends visitor messages via email or stores them for review.

---

## ✉️ Contact form behavior

Form submissions are processed server-side and handled according to environment configuration:

1. **SendGrid HTTP API** (preferred) when `SENDGRID_API_KEY` is defined. Messages are delivered to `CONTACT_RECIPIENT_EMAIL` (default `hrjobportal.system@gmail.com`) and sent from `DEFAULT_FROM_EMAIL` (must be a verified sender).
2. **Fallback** to Django's email backend when no SendGrid key is available. The default backend prints the email to the console (ideal for local development).

> 🔁 You can also bypass emailing altogether by persisting submissions in the database and reviewing them in Django Admin.

---

## 🛠️ Setup & Local Development

```bash
# clone repository
git clone https://github.com/<yourusername>/text-utils.git
cd text-utils

# install dependencies (includes gunicorn for production)
github.com/<yourusername>/text-utils.git
cd text-utils

# create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS / Linux

# install dependencies
pip install -r requirements.txt

# when deploying to Render or similar, ensure a Procfile is present (already added) which uses gunicorn:
#   web: gunicorn textAnalyazer.wsgi --workers 3

# apply database migrations
python manage.py migrate

# create admin user (optional but recommended)
python manage.py createsuperuser

# start development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/contactus` to exercise the contact form. With no external email provider configured, messages appear in the terminal.

---

## ⚙️ Environment Variables

| Variable                | Description                                                           | Default                             |
|-------------------------|-----------------------------------------------------------------------|-------------------------------------|
| `SENDGRID_API_KEY`      | SendGrid API key for HTTP mail delivery                               | *none*                              |
| `DEFAULT_FROM_EMAIL`    | Sender email address (verify in SendGrid if using API)                | `no-reply@textutils.np`             |
| `CONTACT_RECIPIENT_EMAIL` | Receiver address for contact form messages                         | `hrjobportal.system@gmail.com`      |
| `DJANGO_EMAIL_BACKEND`  | Override Django email backend (e.g. SMTP backend)                     | `django.core.mail.backends.console.EmailBackend` |

---

## 📦 Deployment Notes

Ready to deploy on [Render.com](https://render.com) or similar platforms:

- `ALLOWED_HOSTS = ['*']` allows all hosts.
- `DEBUG = True` — toggle to `False` in settings if needed for production.
- Static files handled by WhiteNoise (automatic).
- Optional: Set `SENDGRID_API_KEY` for email notifications.

---

## 📋 GitHub Usage (Optional)

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:<yourusername>/text-utils.git
git push -u origin main
```

A `.gitignore` is included to exclude Python caches, database file, virtual environments, etc.

---

## 🔮 Future Improvements

- Store contact submissions in a `ContactSubmission` model and expose via admin interface.
- Add client-side form validation, reCAPTCHA, and rate limiting.
- Extend text analyzer with more transformation options and a REST API.

---

## 📝 License

This repository is provided **without a formal license**. Use and modify at your own risk.

---

*Created with ❤️ by Dipesh Dhaurali*