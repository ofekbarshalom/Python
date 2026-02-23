from src.tasks import celery_app

# worker entrypoint
if __name__ == '__main__':
    celery_app.start()