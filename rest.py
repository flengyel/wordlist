#!/usr/bin/python
import json
from flask import (Flask, make_response, send_file)
from reverseproxied import ReverseProxied
from random import sample
import os
import traceback
import requests
import re

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
    definitions, source = get_definitions(word)
    response = make_response(json.dumps({'Word': word, 'Definitions': definitions, 'Source': source}, ensure_ascii=False))
    response.headers['Cache-Control'] = 'no-store'
    return response


def get_definitions(word):
    """Fetch all dictionary definitions for the given word and indicate the source API used."""
    definitions = []
    source = ""
    try:
        # Primary dictionary API call (using Free Dictionary API for example purposes)
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        if response.status_code == 200:
            data = response.json()
            # Extract all definitions from the response
            if data and isinstance(data, list):
                for meaning in data[0].get('meanings', []):
                    for definition in meaning.get('definitions', []):
                        definitions.append(definition.get('definition', ''))
                if definitions:
                    source = "dictionaryapi.dev"
        
        # Fallback to another dictionary API if primary fails or no definitions are available
        if not definitions:
            fallback_response = requests.get(f'https://api.datamuse.com/words?sp={word}&md=d')
            if fallback_response.status_code == 200:
                fallback_data = fallback_response.json()
                if fallback_data and isinstance(fallback_data, list) and len(fallback_data) > 0 and 'defs' in fallback_data[0]:
                    raw_definitions = fallback_data[0]['defs']
                    for raw_definition in raw_definitions:
                        # Replace 'n\t' with 'N: ', 'adj\t' with 'Adj: ', and 'adv\t' with 'Adv: '
                        cleaned_definition = re.sub(r'^n\t', 'N: ', raw_definition)
                        cleaned_definition = re.sub(r'^adj\t', 'Adj: ', cleaned_definition)
                        cleaned_definition = re.sub(r'^adv\t', 'Adv: ', cleaned_definition)
                        definitions.append(cleaned_definition.strip())
                    if definitions:
                        source = "datamuse.com"
        
        if not definitions:
            return ["Definition not available"], "None"
        return definitions, source
    except Exception as e:
        print(f"Error fetching definitions for word '{word}': {e}")
        print(traceback.format_exc())
        return ["Definition not available"], "None"

if __name__ == '__main__':
  app.run(host='0.0.0.0')
