#!/bin/bash
pip3 install -r requirements.txt
python3 manage.py collectstatic --noinput
npm install
npm run build
