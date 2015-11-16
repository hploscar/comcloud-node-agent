import settings as s
from tools import files

class Check():
    @staticmethod
    def general():
        docker, crane = ['waiting', 'waiting'], ['waiting', 'waiting']
        try:
            docker = files.readDockerStatus()
            crane = files.readCraneStatus()
        except:
            pass

        status, description = 'installing', 'Components are being installed'

        if docker[0] is None:
            docker[0] = 'error'
        if crane[0] is None:
            crane[0] is 'error'

        if docker[0] == 'running' and crane[0] == 'running':
            status, description = 'done', 'The host is provisioned and ready to deploy services.'
        elif docker[0] == 'error' or crane[0] == 'error':
            status, description = 'error', 'There are some error which need to be solved manually. See application log at \''+s.APP_DATA_DIR+'\''

        return {
            'status': status,
            'description': description,
            'agent': 'running',
            'docker': docker[0],
            'crane': crane[0]
        }

    @staticmethod
    def docker():
        status = files.readDockerStatus()

        return {
            'status': status[0],
            'description': status[1]
        }

    @staticmethod
    def crane():
        status = files.readCraneStatus()

        return {
            'status': status[0],
            'description': status[1]
        }
