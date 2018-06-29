from celery import Celery
from celery.schedules import crontab
from .views import calling_actions
app = Celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, liking_and_following.s(), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, liking_and_following.s(), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        liking_and_following.s('Happy Mondays!'),
    )


@app.task
def liking_and_following():
    calling_actions()
