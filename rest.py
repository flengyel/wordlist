#!/usr/bin/python
import json
from   flask import Flask
from   reverseproxied import ReverseProxied
from   string import rstrip
from   random import sample

# load the wordlist
wordset = set()
with open('wordlist/wordlist') as fp:
      for line in fp:
	line = line.rstrip()
	if len(line) == 0:
	  continue
        wordset.add(line) 

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

@app.route('/')
def randomWord():
    return json.dumps({'Word': sample(wordset,1)[0]})

if __name__ == '__main__':
    #app.debug=True
    app.run(host='0.0.0.0')
