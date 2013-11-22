#!/bin/bash

# control script to start and stop rest server
# NOTE: activate the virtualenv from outside this script
#. $HOME/REST/bin/activate

case  $1 in
	start)
           if [ -f ./pid ]; then
   		echo pid exists, not starting
   		exit -1
	   fi
           ( python rest.py & echo $! >&3 ) 3>pid
	;;
	stop)
	   if [ ! -f ./pid ]; then
	      echo "No pid file. Exiting."
	      exit -1
           fi
	   echo "stopping $(<pid)"
           kill $(<pid)
           rm ./pid
	;;
	*)
	echo "usage $0 start | stop"
	exit 0
	;;
esac
