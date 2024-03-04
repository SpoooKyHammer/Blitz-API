
from celery import Celery, Task
from flask import Flask


def create_celery(app: Flask) -> Celery:
    """
    Creates Celery instance and sets it to `Flask.extensions["celery"]` 
    which can be later accessed anywhere within the flask app context.
    """

    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY_CONFIG"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
