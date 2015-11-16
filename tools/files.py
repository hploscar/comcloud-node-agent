import settings as s
import os
import shutil

class FileExistsError(Exception):
    pass

def initDocker():
    _createFile('docker/log', content='>> Installing docker')
    _createFile('docker/status', content='installing')
    _createFile('docker/info', content='Docker is being installed')


def initCrane():
    _createFile('crane/log', content='>> Installing crane')
    _createFile('crane/status', content='installing')
    _createFile('crane/info', content='Crane is being installed')


def _createFile(relativepath, content='', replace=False):
    path = os.path.join(s.APP_DATA_DIR, relativepath)

    if os.path.exists(path):
        if replace:
            os.unlink(path)
        else:
            raise FileExistsError()

    fo = open(path, "wb")
    fo.write(content);
    fo.close()

def writeDockerStatus(status, information=''):
    _createFile('docker/status', content=status, replace=True)
    _createFile('docker/info', content=information, replace=True)

def writeCraneStatus(status, information=''):
    _createFile('crane/status', content=status, replace=True)
    _createFile('crane/info', content=information, replace=True)

def readDockerStatus():
    status, description = None, None
    with open(os.path.join(s.APP_DATA_DIR, 'docker/status'), "r") as aux:
        status=aux.read().replace('\n', '')
    with open(os.path.join(s.APP_DATA_DIR, 'docker/info'), "r") as aux:
        description=aux.read().replace('\n', '')

    return status, description


def readCraneStatus():
    status, description = None, None
    with open(os.path.join(s.APP_DATA_DIR, 'crane/status'), "r") as aux:
        status=aux.read().replace('\n', '')
    with open(os.path.join(s.APP_DATA_DIR, 'crane/info'), "r") as aux:
        description=aux.read().replace('\n', '')

    return status, description

def getLogPath(component):
    path = os.path.join(s.APP_DATA_DIR, component)
    return os.path.join(path, 'log')
