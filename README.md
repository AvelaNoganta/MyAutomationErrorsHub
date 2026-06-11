# Automation Errors Hub

## Overview

A small web application to store common errors that automation students/instructors encounter on a daily basis.

### Goal

To help automation students/instructors to solve issues quicker

## Pre-requisites

* Python 3.10+
* pip
* Git
* PyCharm or any Python IDE
* sqlite

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

To view the application: Open http://127.0.0.1:5000 

### To view the database

* Download db browser for sqlite mac https://sqlitebrowser.org/dl/  
* Open the `error_hub.db` file to view the database tables and data

### Common Issues 

If you get this error Access to 127.0.0.1 was denied 
* Paste this on browser `chrome://net-internals/#sockets` 
* Click on "Flush socket pools" 
* Try again to access http://127.0.0.1:5000 
