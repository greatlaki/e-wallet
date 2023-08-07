import os
import faust

os.environ.setdefault("FAUST_LOOP", "eventlet")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = faust.App("wallet", autodiscover=True, origin="faustapp")


@app.on_configured.connect
def configure_from_settings(app, conf, **kwargs):
    from django.conf import settings

    conf.broker = settings.FAUST_BROKER_URL
    conf.store = settings.FAUST_STORE_URL
