import datetime
import logging
from abc import ABC, abstractmethod
from typing import Dict, List
import requests
import json
import os
import schedule
import time


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MercadoBitcoinApi:
    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass
        # return f"{self.base_endpoint}/{self.coin}/day-summary/2021/6/22"

    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()


# class BtcApi(MercadoBitcoinApi):
#     def _get_endpoint(self) -> str:
#         return "a"


class DaySummaryApi(MercadoBitcoinApi):
    type = "day-summary"

    def _get_endpoint(self, date: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"


class TradesApi(MercadoBitcoinApi):
    type = "trades"

    def _get_unix_epoch(self, date: datetime.datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(
        self, date_from: datetime.datetime = None, date_to: datetime.datetime = None
    ) -> str:
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        elif date_from and date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"

        return endpoint


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

    def write(self, data: [List, dict]) -> None:
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)


# print(MercadoBitcoinApi(coin="BTC").get_data())
# print(MercadoBitcoinApi(coin="LTC").get_data())

# BtcApi(coin="BTC")

# print(DaySummaryApi(coin="BTC").get_data(date=datetime.date(2021,6,22)))

# print(TradesApi(coin="BTC").get_data())
# print(TradesApi(coin="BTC").get_data(date_from= datetime.datetime(2021,6,21)))
# print(TradesApi(coin="BTC").get_data(date_from= datetime.datetime(2021,6,9), date_to=datetime.datetime(2021,6,10)))

# data = DaySummaryApi("BTC").get_data(date=datetime.date(2021, 6, 23))
# writer = DataWriter("day_summary.json")
# writer.write(data)

# data = TradesApi("BTC").get_data()
# writer = DataWriter("trades.json")
# writer.write(data)


class DataIngestor(ABC):
    def __init__(
        self, writer: DataWriter, coins: List[str], default_start_date: datetime.date
    ) -> None:
        self.default_start_date = default_start_date
        self.coins = coins
        self.writer = writer
        self._checkpoint = None

    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            return self._checkpoint

    def _update_checkpoint(self, value):
        self._chekcpoint = value

    @abstractmethod
    def ingest(self) -> None:
        pass


class DaySummaryIngestor(DataIngestor):

    # def __init__(self, writer:DataWriter, coins: List[str], default_start_date: datetime.date):
    #     super().__init__(writer, coins, default_start_date)
    #     self.writer = writer(coins)

    def ingest(self) -> None:
        date = self._get_checkpoint()
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
            self._update_checkpoint(data + datetime.timedelta(days=1))


# writer = DataWriter('day_summary.json')
ingestor = DaySummaryIngestor(
    writer=DataWriter,
    coins=["BTC", "ETH", "LTC"],
    default_start_date=datetime.date(2021, 6, 1),
)

# @repeat(every(1).seconds)
# def job():
#     ingestor.ingest()

# while True:
#     schedule.run_pending()
#     time.sleep(0.5)
