#!/bin/bash

PYTHONPATH=./gen-py FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
