#!/bin/bash

if [ "$1" != "-u" ]; then 
    echo Invalid command parameter, expect start_notifier -u <telegram_user_id> 
    exit 1
fi

if [ "$2" != "" ]; then 
    echo Invalid command parameter, expect start_notifier -u <telegram_user_id> 
    exit 1
fi

python -m venv env &&\ 
source env/bin/activate


pip install -r requirements.txt

docker compose up -d

python main.py -u $2
