#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  python3 -m celery --app=train.delay_c:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  python3 -m celery --app=train.delay_c:celery flower --basic_auth=novahub:admin
elif [[ "${1}" == "beat" ]]; then
  python3 -m celery --app=train.delay_c.celery beat -l INFO 
fi