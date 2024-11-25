# Wordlist RESTful API Server

## Overview

This project is a simple RESTful word server built using Flask. It serves random words from a word list or definitions for user-provided words via a web API. It includes a web-based search interface for users to look up words interactively.

We upgraded the server to include dictionary definitions and improved word search features. The server returns JSON objects containing word definitions and example usages.

## Features

1. **RESTful Random Word Endpoint**:

   - Provides a randomly chosen word from a word list along with definitions and example sentences, if available.

   - Returns a JSON object of the form:

     ```json

     { “Word”: “random word”, “Definitions”: [“definition 1”, “definition 2”], “Source”: “API source” }

     ```

2. **Word Definition Endpoint**:

   - Look up definitions of specific words using `/define/<word>`. If the word is not in the internal word list, the server will attempt to fetch a definition from the APIs.

3. **Autocomplete and Search Interface**:

   - Interactively search for words using an HTML form. This feature provides suggestions as users type, which are drawn from the word list.

   The `/search` page features a text box and a dropdown list of word suggestions to help you find what you’re looking for.

4. **Fallback APIs**:

   - The server uses multiple dictionary APIs to get definitions.

   - If the first dictionary cannot provide a definition, we query a second API.

## Installation

### Prerequisites

- Python 3.x

- Flask (`pip install flask`)

- Additional dependencies in `requirements.txt` (requests, etc.)

### Directory Structure

The project directories are as follows.

```bash
project_root/

│

├── app.py                          # Main Flask application script

├── wordlist                        # The file containing the list of words

├── templates/

│   └── search.html                 # HTML template for the search page

├── static/

│   ├── js/

│   │   └── jquery-3.7.1.min.js     # jQuery JavaScript file

│   ├── css/                        # CSS files (optional for custom styles)

│   └── images/

│       └── favicon.ico             # Favicon for the web interface

├── reverseproxied.py               # Python middleware script for reverse proxy

├── requirements.txt                # Dependencies for the project

└── README.md                       # Project documentation (this file)

```

## Running the Server

1. **Clone the Repository**:

   ```bash

   git clone <repository-url>

   cd project_root

   ```

2. **Install Dependencies**:

   ```bash

   pip install -r requirements.txt

   ```

3. **Run the Server**:

   ```bash

   python app.py

   ```

   The server will start on `http://localhost:5000`.

## API Endpoints

### Random Word Endpoint

- **URL**: `/`

- **Method**: GET

- **Response**: Returns a random word with definitions and source.

  ```json

  {

    “Word”: “example”,

    “Definitions”: [“N: An instance serving for illustration”],

    “Source”: “dictionaryapi.dev”

  }

  ```

### Specific Word Definition Endpoint

- **URL**: `/define/<word>`

- **Method**: GET

- **Response**: Returns definitions for the word, along with example sentences, if available.

### Search Interface

- **URL**: `/search`

- **Method**: GET

- **Description**: Provides a web-based search interface with a dropdown list of autocomplete suggestions.

## Enhancements

- **Caching**: The system caches frequently requested words to improve response times.

- **Extended Metadata**: Definitions include parts of speech and example sentences, providing more context.

- **Error Handling**: The system properly handles missing words or unavailable definitions.

## Notes

- The server serves the purpose of local use and demonstration.

- The server relies on free public dictionary APIs, subject to rate limits or constraints.
