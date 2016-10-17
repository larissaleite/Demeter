import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'app/static')

MONGODB_SETTINGS = {'DB': "demeter"}
SECRET_KEY = "KeepThisS3cr3t"
