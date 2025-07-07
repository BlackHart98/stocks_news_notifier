#!/bin/bash

if [ "$1" != "-u" ]; then 
    echo "Invalid command parameter, expect start_notifier -u <telegram_user_id>" 
    exit 1
fi

if [ "$2" == "" ]; then 
    echo "Invalid command parameter, expect start_notifier -u <telegram_user_id> "
    exit 1
fi

if [ ! -d "env" ]; then 
    echo "Creating python virtual environment..."

    python -m venv env &&\ 
    source env/bin/activate
fi

docker compose up --wait

pip install -r requirements.txt && python main.py -u $2
