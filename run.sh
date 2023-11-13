#!/bin/bash

source .env
source venv/bin/activate
pip install -r requirements.txt
python floatmap/main.py