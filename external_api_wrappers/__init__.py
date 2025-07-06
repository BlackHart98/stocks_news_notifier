import os
import random
import sys
import time
import typing as t
import requests
from utils import compare_moments_ago, check_updates, purge_all_selenium_sessions
import asyncio
import logging
from dotenv import load_dotenv, find_dotenv
from jinja2 import Environment, FileSystemLoader
from telethon import TelegramClient, events
from dataclasses import dataclass


class AIAgent:
    _summary_injection = None
    _impact_measure_injection = None
    
    def __init__(self, summary_injection: str, impact_measure_injection: str):
        self._summary_injection = summary_injection
        self._impact_measure_injection = impact_measure_injection

    def summarize(self, content: str) -> str:
        return ""
    
    def measure_impact(self, content: str) -> int:
        return 0


class TelegramAPIWrapper:
    _client = None
    _bot_token = None
    
    def __init__(self, api_id: str, api_hash: str, bot_token: str):
        self._client = TelegramClient("bot", api_id, api_hash)
        self._bot_token = bot_token
    
    async def send_news_notification(self, user: str, tick_news_list: t.Dict[str, t.Any]) -> None:
        await self._client.start(bot_token=self._bot_token)
        environment = Environment(loader=FileSystemLoader("templates/"))
        template = environment.get_template('telegram_message.txt')
        logging.info(tick_news_list)
        await self._client.send_message(user, template.render(tick_news_list))
    
    async def disconnect(self) -> None:
        await self._client.disconnect()