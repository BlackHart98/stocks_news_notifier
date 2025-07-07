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
from utils import compare_moments_ago
import asyncio
import logging
from external_api_wrappers import AIAgent


class StockNewsObserver:
    def observe_tick(self, tick: str, ai_agent: AIAgent, wait_time: t.Any = 10) -> t.Optional[t.Dict[str, t.Any]]:
        ...


# TODO: Handle time conversion
class NasdaqNewsObserver(StockNewsObserver):
    _driver: t.Optional[webdriver.Remote] = None
    _earliest_time: t.Optional[str] = None
    
    def __init__(self, driver: webdriver.Remote, earliest_time: str = "7 hours ago"):
        self._driver = driver
        self._earliest_time = earliest_time
    
    def observe_tick(self, tick: str, wait_time: t.Any = 10, seen_article: t.Dict[str, t.Any]={}) -> t.Optional[t.Dict[str, t.Any]]:
        try:
            wait = WebDriverWait(self._driver, wait_time)
            self._driver.get(f"https://www.nasdaq.com/market-activity/stocks/{tick.lower()}/news-headlines") 
            page_source: str = self._driver.page_source
            soup : BeautifulSoup = BeautifulSoup(page_source, "html.parser")
            article_list = soup.find_all("li", {"class" : "jupiter22-c-article-list__item article"})
            temp_ = []
            for article in article_list:
                article_date = ''.join(article.find('span', class_='jupiter22-c-article-list__item_timeline').contents).strip()
                if not compare_moments_ago(self._earliest_time, article_date): 
                    break
                else:
                    article_title = ''.join(article.find('span', class_='jupiter22-c-article-list__item_title').contents).strip()
                    article_link = (f"https://www.nasdaq.com{article.find('a', class_='jupiter22-c-article-list__item_title_wrapper')['href']}").strip()
                    article_content = ""
                    if article_link not in seen_article:
                        self._driver.get(article_link) 
                        page_source_: str = self._driver.page_source
                        soup_ : BeautifulSoup = BeautifulSoup(page_source_, "html.parser")
                        
                        article_content = soup_.find("div", class_="body__content").get_text()
                    else:
                        article_content = seen_article[article_link]
                    article_summary = (article_content.split(sep=".")[0]).strip() + "."
                    
                    temp_ += [{
                        "article_title" : article_title,
                        "article_link" : article_link,
                        "article_summary" : article_summary,
                        "article_impact" : "",
                        "article_content": article_content,
                        "article_date" : article_date,
                    }]
                    
            if len(temp_) == 0:
                 return None
            else:
                return {
                    "tick" : tick,
                    "news" : temp_
                }
                    
        except Exception as e:
            logging.error(f"shit! {e}")
            return []