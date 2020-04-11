import shelve
from typing import Any

class Save:
    def __init__(self) -> None:
        self.file = shelve.open('data') # открывем файлик. туда с помощью shelve ка в словарь данные записываются

    def __del__(self):
        self.file.close()

    def add_data(self, field: str, value: Any) -> None:
        self.file[field] = value # добавить данные

    def get_data(self, field) -> Any:
        try: # достать инфу
            return self.file[field]
        except:
            pass
