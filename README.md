# Automation Errors Hub

## Overview

A small web application to store common errors that automation students/instructors encounter on a daily basis.

### Goal

To help automation students/instructors to solve issues quicker

## Technology Stack

* Python
* Flask
* SQLite

## Database

This application uses SQLite as its database.

SQLite is an embedded database engine, which means no separate database server needs to be installed or configured.
The database is stored in a single file called `error_hub.db`.

When the application starts for the first time, it automatically:

1. Creates the `error_hub.db` database file
2. Creates the required tables
3. Inserts the default categories

The database file is created in the project root directory.

## Pre-requisites

* Python 3.10+
* pip
* Git
* PyCharm or any Python IDE

## Setup Instructions

1. Create a virtual environment

```bash
python -m venv .venv
```

2. Activate the virtual environment

```bash
.\.venv\Scripts\Activate.ps1
```

3. Install everything from the `requirements.txt` file

```bash
pip install -r requirements.txt
```

## How to run?

```bash
python3 app.py
```

or

```bash
python app.py
``` 

## Development Server

Open the application in your browser:

http://127.0.0.1:5000

## Viewing the Database

To inspect the database contents:

1. Download DB Browser for SQLite:
   https://sqlitebrowser.org/dl/

2. Open the generated `error_hub.db` file.

You can then view:

* Tables
* Records
* Database structure

## Common Issues

### Access to 127.0.0.1 was denied

1. Open:

```
chrome://net-internals/#sockets
```

2. Click **Flush socket pools**

3. Refresh:

```
http://127.0.0.1:5000
``` 
