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
from openai import OpenAI
from mistralai import Mistral

class AIAgent:
    _client: t.Optional[OpenAI] = None 
    _model: t.Optional[str] = None
    
    def __init__(self, api_key: str, model: str="mistral-large-latest"):
        self._model = model
        self._client = Mistral(api_key=api_key)
    
    def measure_impact(self, tick: str, content: str) -> str:
        impact_measure_injection: str = f"""
            Your role is to act as a stock news impact rater.
            Rate how important the news is **for {tick}** and how strong the likely market impact will be, 
            using only the 🚨 siren emoji on a scale of 1–5:
            🚨 = not very relevant, 🚨🚨🚨🚨🚨 = very relevant and impactful.
            Respond with exactly 1–5 sirens, nothing else.
        """
        try:
            response = self._client.chat.complete(
                model=self._model,
                messages=[
                    {"role": "system", "content": impact_measure_injection},
                    {
                        "role": "user"
                        , "content": content
                        },
                ],
            )
            result = response.choices[0].message.content.strip()
            # optionally validate result here
            return result
        except Exception as e:
            logging.error(f"Error rating impact: {e}")
            return "🚨"

    def measure_impact_(self, content_news: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        return {}


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