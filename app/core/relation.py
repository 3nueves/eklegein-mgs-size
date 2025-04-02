"""Module to get four users"""
# Configuración de logging
import logging
from abc import ABC, abstractmethod


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("worker-four")


class Relations(ABC):
    """class process"""

    @abstractmethod
    def relations(
        self,
        db: object,
        name: str, operation: object, query: str, env: dict = None
    ) -> dict:
        """get relations"""


class GetRelationUser(Relations):
    """class to get relatioins"""
    def relations(
            self,
            db: object,
            name: str,
            operation: object,
            query: str,
            env: dict = None
        ) -> dict:
        """get relations from a lot of users"""
        db.select_action(name, operation)
        if env:
            return db.execute(name, query, env)
        return db.execute(name, query)


class ManageRelations:
    """init relations"""
    def __init__(self) -> None:
        self.operations = {}

    def load_class(self, name: str,  operation: Relations):
        """get relations"""
        self.operations[name] = operation

    def execute(
            self,
            operation_db_manage: object,
            name_operation_db: str,
            operation: object,
            name_operation_relation: Relations,
            query: str,
            env: dict
        ) -> dict:
        """execute query"""
        return self.operations[name_operation_relation].relations(
            operation_db_manage,
            name_operation_db,
            operation,
            query,
            env
        )
