CELERY_RESULT_BACKEND = "mongodb"

BROKER_HOST = "localhost"
BROKER_PORT = 27017
BROKER_TRANSPORT = 'mongodb'
BROKER_VHOST = 'to3d'
CELERY_IMPORTS = ('tasks',)
CELERY_MONGODB_BACKEND_SETTINGS = {
    'host': 'localhost',
    'port': 27017,
    'database': 'to3d',
    'user': "root",
    'password': "mongo",
    'taskmeta_collection': 'tasks',
    "ssl": True
}
