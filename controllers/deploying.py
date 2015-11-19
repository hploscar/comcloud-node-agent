import os
import tarfile

import settings
from tools import files, commands
from errors import ControllerError

class Deploy():
    @staticmethod
    def new(package):
        try:
            files.initDeploy()
        except:
            raise ControllerError("Deploy already started")

        try:
            # save
            path = os.path.join(settings.APP_DATA_DIR, 'deploy')
            archivepath = os.path.join(path, 'package.tar')
            package.save(archivepath)
            # extract
            archive = tarfile.open(name=archivepath)
            archive.extractall(path=os.path.join(path, 'package'))
            #compose up
            try:
                if not commands.execute('docker-compose up -d', \
                                    cwd=os.path.join(path, 'package'), \
                                    stdout=os.path.join(path, 'compose_log.txt'), \
                                    errout=os.path.join(path, 'compose_err_log.txt'),
                                    background=True):
                    raise ControllerError("Compose returned !0")
            except ControllerError as e:
                raise e
            except Exception as e:
                raise ControllerError("Error with compose. "+e.message)
        except Exception as e:
            #files.removeDeploy()
            raise e

        return {'response':'ok'}
