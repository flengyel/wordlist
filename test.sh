#!/bin/bash

# activate the virtualenv
# from outside 
#. $HOME/REST/bin/activate

# detach the REST server 
# save the pid to file descriptor 3
( python rest.py & echo $! >&3 ) 3>pid

# leave sufficient time for the server to start
sleep 2

echo $(<pid)

# run the tests
curl http://localhost:5000/


curl http://localhost:5000/

curl http://localhost:5000



# kill the server process
kill $(<pid)
