import os
import settings as s

def initializator():
    # create app dir if not exists
    if not os.path.exists(s.APP_DATA_DIR):
        os.makedirs(s.APP_DATA_DIR, 0775)
        os.makedirs(os.path.join(s.APP_DATA_DIR, 'downloads'), 0775)
        os.makedirs(os.path.join(s.APP_DATA_DIR, 'docker'), 0775)
        os.makedirs(os.path.join(s.APP_DATA_DIR, 'crane'), 0775)
        os.makedirs(os.path.join(s.APP_DATA_DIR, 'deploy'), 0775)
