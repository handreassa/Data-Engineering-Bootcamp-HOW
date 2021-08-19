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

from ingestors import DaySummaryIngestor
from writers import DataWriter

if __name__ == "__main__":
    daysummaryingestor = DaySummaryIngestor(
        writer=DataWriter,
        coins=["BTC", "ETH", "LTC"],
        default_start_date=datetime.date(2021, 6, 1),
    )

    @schedule.repeat(schedule.every(1).seconds)
    def job():
        daysummaryingestor.ingest()

    while True:
        schedule.run_pending()
        time.sleep(0.5)
