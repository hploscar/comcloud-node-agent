import os
GENERAL_DEBUG = (True if os.environ.get('DEBUG')=='true' else False)

# API endpoint
WS_BIND_IP='0.0.0.0'
WS_BIND_PORT=5050

# Application data
APP_DATA_DIR='./var/comcloud-agent'
#APP_DATA_DIR='/var/comcloud-agent'
