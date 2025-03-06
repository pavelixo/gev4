#!/bin/bash

npm install
npm run build

pip3 install -r requirements.txt
python3 manage.py collectstatic --noinput