import datetime
import logging
from abc import ABC, abstractmethod
from typing import Dict, List
import requests
import json
import os
import schedule
import time
import backoff
import ratelimit


class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = (
            f"Data type {type(data)} is currently not supported for ingestion."
        )
        super().__init__(self.message)


class DataWriter:
    def __init__(self, coin: str, api: str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')}.json"

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        # Open file with append mode
        with open(self.filename, mode="a") as f:
            f.write(row)

    def write(self, data) -> None:
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)
