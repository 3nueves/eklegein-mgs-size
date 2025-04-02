"""Module Utilities"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("worker-four")


@dataclass
class UtilsBase():
    """utils class"""
    users: list

@dataclass
class UtilsNormalize():
    """utils class"""
    arch: str
    relation_user: dict

@dataclass
class UtilsCheckUsers(UtilsBase):
    """utils class"""
    primary_user: dict

@dataclass
class UtilsGetUsers(UtilsBase):
    """utils class"""
    num_users: int
    score_type: str
    grp: list

@dataclass
class UtilChangeUserStatus(UtilsBase):
    """utils class"""
    db_manager_class: object
    db_name_class: str
    db_operation_class: object


class Operations(ABC):
    """class operation"""

    @abstractmethod
    def operations(self) -> dict:
        """operations"""


class NormalizeResult(Operations, UtilsNormalize):
    """class optimeze out"""
    def operations(self) -> dict:
        relation = ""
        users_list = []

        relation = [relations[0]["~relations"]
            for relations in [user[self.arch]
            for user in list(self.relation_user[self.arch]['user'])]]

        relation = relation[0] if relation else []

        for pool_user in relation:
            if f'~{self.arch}' in pool_user:
                for us in pool_user[f'~{self.arch}']:
                    users_list.append(us)
        return users_list


class CheckUsersInGroup(Operations, UtilsCheckUsers):
    """check if user is in group"""
    def operations(self) -> dict:
        for user in self.users:
            if "groups" in user and "groups" in self.primary_user:
                for group in user["groups"]:
                    if group in self.primary_user["groups"]:
                        user.remove(user)
        return self.users


class GetUsers(Operations, UtilsGetUsers):
    """get a number users"""

    # En esta clase cogemos el número de los usuarios que le pasamos en num_users.
    def operations(self) -> dict:
        list_users = []

        # Verificamos que el usuario seleccionado no esta ya
        # en la lista de usuarios seleccionados para formar
        # el grupo.
        for user in self.users:
            for user_group in self.grp:
                if user["uid"] == user_group["uid"]:
                    self.users.remove(user)

        # Buscamos usuarios de un que sean o hard o medium o soft y que además
        # esten dentre de las puntuaciones más altas.
        for user in self.users:
            if self.score_type in user and user[self.score_type] >= 2.5:
                list_users.append(user)
            elif self.score_type in user and user[self.score_type] >= 2.0:
                list_users.append(user)
            elif self.score_type in user and user[self.score_type] >= 1.5:
                list_users.append(user)
            elif self.score_type in user and user[self.score_type] >= 1.0:
                list_users.append(user)

            if len(list_users) >= self.num_users:
                return list_users
        #     list_users.append(self.users[:self.position_user_in_list][0])
        return list_users

class ChangeUserStatus(Operations, UtilChangeUserStatus):
    """change status"""

    # Verifica el estado del usuario.
    def operations(self) -> dict:
        user_send_mail_onhold = []
        user_send_mail_blocked = []
        group_status: str
        self.db_manager_class.select_action(self.db_name_class, self.db_operation_class)

        for user in self.users:
            if user["join_to_team"] == "StandBy":
                change_status_join = {
                    "uid": user["uid"],
                    "join_to_team": "OnHold"
                }
                self.db_manager_class.execute(change_status_join)
                user["join_to_team"] = "OnHold"
                user_send_mail_onhold.append(user["User.email"])
                group_status = "Pending"

            if user["join_to_team"] == "Finding":
                change_status_join = {
                    "uid": user["uid"], 
                    "join_to_team": "Blocked"
                }
                self.db_manager_class.execute(change_status_join)
                user["join_to_team"] = "Blocked"
                user_send_mail_blocked.append(user["User.email"])

        return group_status, user_send_mail_onhold, user_send_mail_blocked


class ManageOperations:
    """Manage members of group"""
    def __init__(self) -> None:
        self.operation = {}

    def select_operation(self, name: str, operation: Operations):
        """check"""
        self.operation[name] = operation

    def execute(self, name: str):
        """execute"""
        if name not in self.operation:
            raise ValueError("check not found")
        else:
            # print(name)
            return self.operation[name].operations()
