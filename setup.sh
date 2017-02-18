#!/usr/bin/env bash

# Install required libs
sudo pip install -r requirements.txt

# Create database migrations
python manage.py migrate