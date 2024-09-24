# Flask SSE demo Project

This is a Flask project managed with Poetry.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Running the Application](#running-the-application)

## Installation

### Prerequisites

Make sure you have [Poetry](https://python-poetry.org/docs/#installation) installed on your machine. You can install it using the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```
### Running the Application
```bash
poetry install
export FLASK_APP=app.py
poetry run flask run
```

### Other poetry commands
```bash
poetry init
poetry add flask
poetry update package
poetry shell
poetry run python app.py
```

