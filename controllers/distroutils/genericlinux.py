import subprocess
import os

from tools import files
import settings


def installDocker():
    # docker engine
    command = 'curl https://get.docker.com/ | bash'+' 1> '+ files.getLogPath('docker') +' 2> '+ files.getLogPath('docker')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/tmp')

    response = ''
    for line in p.stdout.readlines():
        response+=line+os.linesep

    p.wait()

    command = 'docker ps '+' 1> '+ files.getLogPath('docker') +' 2> '+ files.getLogPath('docker')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/tmp')

    response = ''
    for line in p.stdout.readlines():
        response+=line+os.linesep

    if p.wait() == 0:
        pass
    else:
        return False

    # docker compose
    command = 'curl -L https://github.com/docker/compose/releases/download/1.5.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose '+' 1> '+ files.getLogPath('docker') +' 2> '+ files.getLogPath('docker')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/tmp')

    response = ''
    for line in p.stdout.readlines():
        response+=line+os.linesep

    if p.wait() == 0:
        return True
    else:
        return False


def installCrane():
    # download
    command = 'wget -O crane.tar.gz '+settings.CRANE_ORIGIN+' 1> '+ files.getLogPath('crane') +' 2> '+ files.getLogPath('crane')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/tmp/')

    response = ''
    for line in p.stdout.readlines():
        response+=line+os.linesep

    if p.wait() == 0:
        pass
    else:
        return False

    # extract
    command = 'tar xzvf crane.tar.gz && mv ./docker-crane-* '+settings.CRANE_INSTALL_FOLDER+' 1> '+ files.getLogPath('crane') +' 2> '+ files.getLogPath('crane')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/tmp/')

    response = ''
    for line in p.stdout.readlines():
        response+=line+os.linesep

    if p.wait() == 0:
        pass
    else:
        return False

    # generate certificates
    command = 'genCerts.sh'+' 1> '+ files.getLogPath('crane') +' 2> '+ files.getLogPath('crane')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=settings.CRANE_INSTALL_FOLDER)

    response = ''
    for line in p.stdout.readlines():
        response+=line+os.linesep

    if p.wait() == 0:
        pass
    else:
        return False

    # execute
    command = 'docker-compose -f production.yml up -d'+' 1> '+ files.getLogPath('crane') +' 2> '+ files.getLogPath('crane')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=settings.CRANE_INSTALL_FOLDER)

    response = ''
    for line in p.stdout.readlines():
        response+=line+os.linesep

    if p.wait() == 0:
        return True
    else:
        return False
