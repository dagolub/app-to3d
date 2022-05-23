from celery import Celery

celery = Celery('EOD_TASKS',broker='mongodb://root:mongo@localhost:27017/to3d?authSource=admin&retryWrites=true&w=majority')
celery.config_from_object('app.core.celeryconfig')