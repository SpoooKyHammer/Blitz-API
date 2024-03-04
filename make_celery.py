"""Entry point to create celery application."""

from blitz_api import create_app

flask_app = create_app()
celery_app =  flask_app.extensions["celery"]
