from requests import get
from pymongo import MongoClient

from pymongo.collection import Collection

from config import *


def fetch_forecast_data(query: str):
    response = get(
        f'https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={query}&days=3'
    )

    return response.json() if response.status_code == 200 else ERROR_MESSAGE


def connect_to_db() -> Collection:
    client = MongoClient(DB_URI)

    return client['favorites']['items']
