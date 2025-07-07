import os
import random
import sys
import time
import typing as t
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import compare_moments_ago, check_updates, purge_all_selenium_sessions
import asyncio
import logging
from dotenv import load_dotenv, find_dotenv
from jinja2 import Environment, FileSystemLoader
from telethon import TelegramClient, events
from dataclasses import dataclass
from external_api_wrappers import AIAgent, TelegramAPIWrapper
from observer import NasdaqNewsObserver
from reader import PlainTextReader


REMOTE_URL = "http://localhost:4444/wd/hub"
APP_DATA_PATH = ".app_data"
DOT_ENV_PATH = find_dotenv()

load_dotenv(DOT_ENV_PATH)

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")



async def main(argv: t.List[str]):
    if len(argv) != 3:
        logging.error("Invalid command parameter, expect `python main.py -u <telegram_user_id>`")
        sys.exit()
    if argv[1] != "-u":
        logging.error("Invalid command parameter, expect `python main.py -u <telegram_user_id>`")
        sys.exit()
    
    user_id = argv[2]
    
    logging.info(f"Fetching ticks")
    ticks = PlainTextReader("stock_ticks.txt").get_tick_symbols()
    previous_state = {item : [] for item in ticks}
    
    logging.info(f"Fetched {len(ticks)} stock ticks")
    ai_bot: AIAgent = AIAgent("", "")
    telegram_bot:TelegramAPIWrapper = TelegramAPIWrapper(TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_TOKEN)
    
    # Set up Chromium options
    chrome_options : Options = Options()
    # chrome_options.add_argument("--headless") # commented for debugging purposes
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    capabilities = {
        "browserName": "chrome",
        "platformName": "ANY",
    }
    
    directory_name = APP_DATA_PATH
    try:
        os.mkdir(directory_name)
        logging.info(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        logging.info(f"Directory '{directory_name}' already exists.")
        with open(directory_name + "/session_ids.txt", "r") as f:
            logging.info(f"Fetching stale sessions '{directory_name}/session_ids.txt'.")
            session_ids = [line.strip() for line in f.readlines()]
            purge_all_selenium_sessions(REMOTE_URL, session_ids)
            f.close()
    except PermissionError:
        logging.warning(f"Permission denied: Unable to create '{directory_name}', application might not behave properly.")
    except Exception as e:
        logging.info(f"An error occurred: {e}")
    driver: t.Optional[webdriver.Remote] = None
    
    while True:
        with open(directory_name + "/session_ids.txt", "w") as f:
            driver : webdriver.Remote = webdriver.Remote(
                command_executor=REMOTE_URL,
                options=chrome_options,
            )
            f.write(driver.session_id)
            f.close()
        sample = NasdaqNewsObserver(driver)
        for item in ticks:
            try:
                temp_ = sample.observe_tick(item, ai_bot)
                logging.info(f"Current page {temp_}")
                updates = None
                if len(previous_state[item]) == 0:
                    updates = check_updates(None, temp_)
                    logging.info(check_updates(None, temp_))
                    logging.info(updates)
                else:
                    updates = check_updates(previous_state[item], temp_)
                    logging.info(check_updates(previous_state[item], temp_))
                    logging.info(updates)
                if updates is not None:
                    logging.info(f"Sending notification for {item}")
                    result = await telegram_bot.send_news_notification(user_id, updates)
                    logging.info(f"Telegram send result for {item}: {result}")
                    previous_state[item] = temp_
                else:
                    logging.info(f"No updates to send for {item}")
            except Exception as e:
                logging.error(f"Error processing {item}")
        await telegram_bot.disconnect()
        driver.quit()
        time.sleep(600)
        




if __name__ == "__main__":
    logging.basicConfig(
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
    asyncio.run(main(sys.argv))