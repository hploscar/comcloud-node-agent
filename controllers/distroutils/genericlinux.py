import subprocess

from tools import files


def installDocker():
    command = 'curl https://get.docker.com/ | bash'+' 1> '+ files.getLogPath('docker') +' 2> '+ files.getLogPath('docker')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/tmp')

    response = ''
    for line in p.stdout.readlines():
        response+=line+os.linesep

    if p.wait() == 0:
        return True
    else:
        return False
