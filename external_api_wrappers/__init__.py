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
    
    def _measure_impact(self, tick: str, content: str, max_attempts: int = 5, base_delay: float = 1.0) -> str:
        impact_measure_injection: str = f"""
            Your role is to act as a stock news impact rater.
            Rate how important the news is **for {tick}** and how strong the likely market impact will be, 
            using only the 🚨 siren emoji on a scale of 1–5:
            🚨 = not very relevant, 🚨🚨🚨🚨🚨 = very relevant and impactful.
            Respond with exactly 1–5 sirens, nothing else.
        """
        for attempt in range(1, max_attempts + 1):
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
                err_msg = str(e)
                # Log the error
                logging.warning(f"Attempt {attempt}: API call failed: {err_msg}")

                if "429" in err_msg or "rate" in err_msg.lower() or "capacity" in err_msg.lower():
                    sleep_time = base_delay * (2 ** (attempt - 1))
                    jitter = random.uniform(0, 0.2)
                    total_sleep = sleep_time + jitter
                    logging.info(f"Rate-limited. Sleeping for {total_sleep:.2f}s before retrying…")
                    time.sleep(total_sleep)
                    
        logging.error(f"Error rating impact: {e}")
        return "🚨"

    def measure_impact(self, content_news: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        result = {
            "tick" : content_news["tick"],
            "news" : []
        }
        for item in content_news["news"]:
            result["news"] += [{
                "article_title" : item["article_title"],
                "article_link" : item["article_link"],
                "article_summary" : item["article_summary"],
                "article_impact" : self._measure_impact(result["tick"], item["article_content"]),
                "article_content": item["article_content"],
                "article_date" : item["article_date"],
            }]
        return result


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