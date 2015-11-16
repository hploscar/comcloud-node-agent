import platform
from threading import Thread

import settings as s
import tools
from tools import files
from errors import ResourceExistsError, ControllerError, PlatformNotSupportedError, InstallationError
from distroutils import genericlinux

def _installDockerThread():
    try:
        # Detect platform
        distro = platform.linux_distribution()

        if distro[0] != '':
            try:
                if not genericlinux.installDocker():
                    raise InstallationError('Installation failed. Manual action required.')
            except:
                raise ControllerError('Installator execution failure.')
        else:
            raise PlatformNotSupportedError('Could not identify linux distribution')

        files.writeDockerStatus('running', 'Docker has been installed and it must be running.')

    except PlatformNotSupportedError as e:
        files.writeDockerStatus('error', e.message)
    except Exception as e:
        files.writeDockerStatus('error', 'unspecified fatal failure')

def _installCraneThread():
    try:
        # Detect platform
        distro = platform.linux_distribution()

        if distro[0] != '':
            try:
                if not genericlinux.installDocker():
                    raise InstallationError('Installation failed. Manual action required.')
            except:
                raise ControllerError('Installator execution failure.')
        else:
            raise PlatformNotSupportedError('Could not identify linux distribution')

        files.writeDockerStatus('running', 'Docker has been installed and it must be running.')

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
            files.initCrane()
        except files.FileExistsError:
            raise ResourceExistsError("Another crane installation is in progress.")

        thread = Thread(target = _installCraneThread)
        thread.start()

        return {
            'status':'installing',
            'description':'crane is being installed in the machine'
        }
