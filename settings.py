import os
GENERAL_DEBUG = (True if os.environ.get('DEBUG')=='true' else False)

# API endpoint
WS_BIND_IP='0.0.0.0'
WS_BIND_PORT=5050

# Application data
APP_DATA_DIR='./var/comcloud-agent'
#APP_DATA_DIR='/var/comcloud-agent'

# Crane
CRANE_ORIGIN='https://github.com/wtelecom/docker-crane/archive/0.9.5.tar.gz'
CRANE_INSTALL_FOLDER='/usr/src/crane'
CRANE_CON_ATT=15 # Number of connection attempts while waiting crane to come up
CRANE_TIMEBETWEENATT=30 # Number of seconds between attempts
