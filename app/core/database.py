"""Module to manage DataBase"""

import logging
from abc import ABC, abstractmethod

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("worker-four")


class DataBase(ABC):
    """access database"""

    @abstractmethod
    def action(self, data: object) -> object:
        """query data"""


class DataBaseEnv(ABC):
    """access database"""

    @abstractmethod
    def action_env(self, query: dict, env: dict) -> object:
        """query data"""


class QueryData(DataBase, DataBaseEnv):
    """class insert"""

    def __init__(self, database: object) -> None:
        self.db = database

    def action(self, data: object) -> object:
        return self.db.query_data(data)

    def action_env(self, query: dict, env: dict) -> object:
        return self.db.query_data(query, env)


class InsertData(DataBase):
    """class insert"""

    def __init__(self, database: object) -> None:
        self.db = database

    def action(self, data: object) -> object:
        return list(self.db.create_data(data).values())


class DeleteData(DataBase):
    """class insert"""

    def __init__(self, database: object) -> None:
        self.db = database

    def action(self, data: object) -> object:
        return self.db.delete_data(data)


class ManageDataBaseEnv:
    """manage data"""

    def __init__(self) -> None:
        self.queries = {}

    def select_action(self, name: str, operation: DataBaseEnv) -> None:
        """execute action"""
        self.queries[name] = operation

    def execute(self, name: str, data: dict, env: dict = None) -> str:
        """execute insert"""
        if env:
            return self.queries[name].action_env(data, env)
        return self.queries[name].action(data)


class ManageDataBase:
    """manage data"""

    def __init__(self) -> None:
        self.queries = {}

    def select_action(self, name: str, operation: DataBase) -> None:
        """execute action"""
        self.queries[name] = operation

    def execute(self, name: str, data: dict) -> str:
        """execute insert"""
        return self.queries[name].action(data)
