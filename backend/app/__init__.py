from django.conf import settings

from .celery import app as celery_app

if settings.CELERY_RUN:
    __all__ = ("celery_app",)
