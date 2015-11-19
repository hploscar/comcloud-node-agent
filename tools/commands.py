import os
import subprocess

def execute(command, cwd="./", stdout='/dev/null', errout='/dev/null', background=False):
    command2 = command+' 1> '+ stdout +' 2> '+ errout
    p = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)

    if not background:
        response = ''
        for line in p.stdout.readlines():
            response+=line+os.linesep

        if p.wait() == 0:
            return True
        else:
            return False
    else:
        return True
