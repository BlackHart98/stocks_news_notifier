# Stock News Bot (Incomplete readme)
This listens for new update and notifies you via telegram

## How to use this
1. Create a `.env` file to keep your credentials, which are
```env
OPEN_AI_KEY=
TELEGRAM_TOKEN=
TELEGRAM_API_ID=
TELEGRAM_API_HASH=
```
2. Install Python3 (python 3.12 preferably)
3. Create a virtual environment 
```sh
python -m venv env
```
then activate the virtual environment, by running this 
> for unix-based systems (linux and macOS)
```sh
source activate
```
4. Install the necessary requirements with
```sh
pip install -r requirements.txt
```

9. Spin up Selenium grid container by running this
```sh
docker compose up -d
```
10. Run this on the terminal
```sh
python main.py -u <user_id>
```

## Too many steps? Do this instead
1. 1. Create a `.env` file to keep your credentials, which are
```env
OPEN_AI_KEY=
TELEGRAM_TOKEN=
TELEGRAM_API_ID=
TELEGRAM_API_HASH=
```
2. Open the terminal and run this for linux and macOS
```sh
sh ./bin/start_notifier -u <user_id>
```


## Issues
1. Only works for single user, although it can easily be extended to support multi-user, channels etc.