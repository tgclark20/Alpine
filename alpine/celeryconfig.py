from celery import Celery
from celery.schedules import crontab
def make_celery(app, name):
    celery = Celery(
        name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.beat_schedule = {
        # Executes Sunday-Thursday Evening at 8:00 p.m.
        'run-algorithm': {
            'task': 'app.runAlgorithm',
            'schedule': crontab(hour=00, minute=00, day_of_week="0-3"),
        },
        # Executes Monday-Friday Evening at 8:00 a.m
        'post-transaction':{
            'task': 'app.postTransactions',
            'schedule': crontab(hour=10, minute=00, day_of_week="1-4"),
        },
    }
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery