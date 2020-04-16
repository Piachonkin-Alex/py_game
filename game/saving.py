import shelve
import json
from typing import Any


class Save:
    def __init__(self) -> None:
        self.data = []
        with open('data.json', 'r') as f:
            self.data = json.load(f)
        # открывем файлик. туда с помощью shelve ка в словарь данные записываются

    def add_data(self, field: str, value: Any) -> None:
        with open('data.json', 'w') as f:
            json.dump(value, f)  # добавить данные

    def get_data(self, field) -> Any:
        return self.data
