#!/bin/bash

. .venv/bin/activate

cd frontend
npm run build

cd ../ui
python manage.py collectstatic --noinput