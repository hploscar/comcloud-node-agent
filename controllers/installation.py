import platform
from threading import Thread
import time
import requests

import settings as s
import tools
from tools import files
from errors import ResourceExistsError, ControllerError, PlatformNotSupportedError, InstallationError
from distroutils import genericlinux

def _testCrane():
    try:
        r = requests.get('http://localhost:8888/extra/alive')
        if not r:
            return False
        return True
    except:
        return False

def _installDockerThread():
    try:
        # Detect platform
        distro = platform.linux_distribution()

        if distro[0] != '':
            try:
                if not genericlinux.installDocker():
                    raise InstallationError('Installation failed. Manual action required.')
            except Exception as e:
                raise ControllerError('Installator execution failure. ' + e.message)
        else:
            raise PlatformNotSupportedError('Could not identify linux distribution')

        files.writeDockerStatus('running', 'Docker has been installed and it must be running.')

    except PlatformNotSupportedError as e:
        files.writeDockerStatus('error', e.message)
    except ControllerError as e:
        files.writeDockerStatus('error', e.message)
    except Exception as e:
        files.writeDockerStatus('error', 'unspecified fatal failure')

def _installCraneThread():
    try:
        try:
            if not genericlinux.installCrane():
                raise InstallationError('Installation failed. Manual action required.')
        except:
            raise ControllerError('Installator execution failure.')

        files.writeCraneStatus('installed', 'Crane has been installed and it must be available in some minutes.')

        attempts = settings.CRANE_CON_ATT
        while not _testCrane() and attempts>0:
            time.sleep(settings.CRANE_TIMEBETWEENATT)
            attempts = attempts-1

        if attempts == 0:
            raise InstallationError('Cannot connect with Crane. Maybe a problem ocurred and was not detected.')

        files.writeCraneStatus('running', 'Crane must be running.')

    except PlatformNotSupportedError as e:
        files.writeDockerStatus('error', e.message)
    except Exception as e:
        files.writeDockerStatus('error', 'unspecified fatal failure')


class Installator():
    @staticmethod
    def docker():
        try:
            files.initDocker()
        except files.FileExistsError:
            raise ResourceExistsError("Another docker installation is in progress.")

        thread = Thread(target = _installDockerThread)
        thread.start()

        return {
            'status':'installing',
            'description':'docker is being installed in the machine'
        }

    @staticmethod
    def crane():
        try:
            files.readDockerStatus()
        except:
            raise ControllerError("Docker not installed. Install docker first.")

        try:
            files.initCrane()
        except files.FileExistsError:
            raise ResourceExistsError("Another crane installation is in progress.")

        thread = Thread(target = _installCraneThread)
        thread.start()

        return {
            'status':'installing',
            'description':'crane is being installed in the machine'
        }
