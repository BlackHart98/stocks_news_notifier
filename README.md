# Stock News Bot
This listens for new update and notifies you via telegram


## Prerquisites
1. Install [docker](https://docs.docker.com/get-started/get-docker/)
2. Install Python3 (python 3.12 preferably)

## How to use this
1. Create a `.env` file to keep your credentials, which are
```env
OPEN_AI_KEY=
TELEGRAM_TOKEN=
TELEGRAM_API_ID=
TELEGRAM_API_HASH=
MISTRAL_AI_KEY=
```
> [!Note]
> I am currently using Mistral API

2. Create a virtual environment 
```sh
python -m venv env
```
then activate the virtual environment, by running this 
> for unix-based systems (linux and macOS)
```sh
source activate
```
3. Install the necessary requirements with
```sh
pip install -r requirements.txt
```

4. Spin up Selenium grid container by running this
```sh
docker compose up -d
```
5. Run this on the terminal
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
MISTRAL_AI_KEY=
```
2. Open the terminal and run this for linux and macOS
```sh
sh ./bin/start_notifier -u <user_id>
```


## Issues and future considerations
1. Only works for single user, although it can easily be extended to support multi-user, channels etc.
2. I haven't tested for Windows yet
3. I intend to use OpenAI API