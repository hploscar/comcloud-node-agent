#/bin/bash

function launch {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo "error with $@" >&2
        exit 1
    fi
    return $status
}

case `uname` in
  Linux )
     LINUX=1
     which yum > /dev/null 2> /dev/null && { YUM=1; }
     which apt-get > /dev/null 2> /dev/null && { APT=1; }
     ;;
  Darwin )
     DARWIN=1
     >&2 echo "Darwin not supported"
     exit 1
     ;;
  * )
     # Handle AmgiaOS, CPM, and modified cable modems here.
     ;;
esac

if [[ $YUM = 1 ]];
then
echo 'Using YUM installer'

>&2 echo 'YUM installer not implemented yet'
exit 1

exit 0
elif [[ $APT = 1 ]];
then
echo 'Using APT-GET installer'

launch apt-get update -yqq
launch apt-get install -yqq python-dev python-pip libncurses-dev
launch pip install -r ./requirements.txt

echo 'Installation successful'

exit 0
fi

>&2 echo "Platform not supported"
exit 1
