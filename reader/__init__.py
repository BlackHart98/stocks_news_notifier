import os
import random
import sys
import time
import typing as t
import logging
from dataclasses import dataclass

class FileReader:
    _content: t.List[str] = []
    _file_path: t.Optional[str] = None 
    def __init__(self, file_path: str):
        pass

    def get_tick_symbols(self) -> t.List[str]:
        pass


class PlainTextReader(FileReader):
    _content: t.List[str] = []
    _file_path: t.Optional[str] = None 
    
    def __init__(self, file_path: str):
        self._file_path = file_path
        pass
    
    def get_tick_symbols(self) -> t.List[str]:
        try:
            with open(self._file_path, "r") as f:
                result: t.List[str] = [line.strip() for line in f.readlines()]
                return result
        except Exception as e:
            logging.error(f"Error occurred attempting to fetch ticks due to {e}")
            return []


class ExcelReader(FileReader):
    _content: t.List[str] = []
    _file_path: t.Optional[str] = None 
    
    def __init__(self, file_path: str):
        pass
    
    def get_tick_symbols(self) -> t.List[str]:
        return []