from celery import shared_task


@shared_task
def send_hello():
    print("Hello World")
