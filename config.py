import os

DEBUG = True
WTF_CSRF_ENABLED = True
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')