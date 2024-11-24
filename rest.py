#!/usr/bin/python
import json
from flask import (Flask, make_response, send_file)
from reverseproxied import ReverseProxied
from random import sample
import os
import traceback
import requests

# load the set of words 
wordset = set()
with open('wordlist') as fp:
  for line in fp:
    line = line.rstrip()
    if len(line) == 0:
      continue
    wordset.add(line) 

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

@app.route('/favicon.ico')
def favicon():
    try:
        # Get the absolute path to the favicon.ico
        current_directory = os.path.dirname(os.path.abspath(__file__))
        favicon_path = os.path.join(current_directory, 'favicon.ico')

        # Send the file with appropriate caching headers
        response = send_file(favicon_path, mimetype='image/x-icon')
        response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 1 day
        return response
    except Exception as e:
        print(f"Error serving favicon: {e}")
        print(traceback.format_exc())
        return "Error serving favicon", 500

@app.route('/')
def randomWord():
    """Return the JSON of a python map (in JavaScript, an object) 
     with the key 'Word' and value uniformly sampled from the 
     set of words from the file wordlist. The function sample 
     returns a list of length 1; we take its first element."""
    word = sample(list(wordset), 1)[0]
    definition = get_definition(word)
    response = make_response(json.dumps({'Word': word, 'Definition': definition}))
    response.headers['Cache-Control'] = 'no-store'
    return response


def get_definition(word):
    """Fetch the dictionary definition for the given word."""
    try:
        # Example dictionary API call (using Free Dictionary API for example purposes)
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        if response.status_code == 200:
            data = response.json()
            # Extract the first definition from the response
            if data and isinstance(data, list):
                meanings = data[0].get('meanings', [])
                if meanings:
                    definitions = meanings[0].get('definitions', [])
                    if definitions:
                        return definitions[0].get('definition', 'Definition not available')
        return "Definition not available"
    except Exception as e:
        print(f"Error fetching definition for word '{word}': {e}")
        print(traceback.format_exc())
        return "Definition not available"

if __name__ == '__main__':
  app.run(host='0.0.0.0')
