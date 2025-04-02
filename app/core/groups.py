"""Module Groups"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.database.db import DB
from app.core.database import QueryData, ManageDataBaseEnv
from app.core.schemas import ManageSchemas, QueryUserCountry, QueryUserCountryUser
from app.core.utils import ManageOperations, CheckUsersInGroup, NormalizeResult, GetUsers
from app.core.relation import ManageRelations, GetRelationUser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("worker-four")

schema = ManageSchemas()
relations = ManageRelations()
operations = ManageOperations()

arch_score = {
    "archetype_hard":   "score_hard",
    "archetype_medium": "score_medium",
    "archetype_soft":   "score_soft"
}

@dataclass
class MainValues:
    """class generic env"""
    group: dict
    user: dict
    grp: list

@dataclass
class UserToUserValues(MainValues):
    """class with values"""
    primary_user: dict

@dataclass
class UserWithUserValues(MainValues):
    """class with values"""
    num_members: int
    score: str

class Group(ABC):
    """class to create groups"""

    @abstractmethod
    def create(self) -> list:
        """create group"""

class GetRelationUserToUser(Group, UserToUserValues):
    """class to find relation one to one"""

    def create(self) -> list:

        schema.load_querys("QueryUserCountryUser", QueryUserCountryUser())
        relations.load_class("GetRelationUser", GetRelationUser())

        # Obtenemos las relaciones del usuario.
        print("\nPrimary_user:",self.primary_user,"\n")
        for arch, score in arch_score.items():
            p_user = relations.execute(
                ManageDataBaseEnv(),
                "QueryData",
                QueryData(DB()),
                "GetRelationUser", 
                schema.exec_query("QueryUserCountryUser", arch, score),
                {
                    "$uid": self.user["uid"],
                    "$country": self.user["country"],
                    "$uid_second": self.primary_user["uid"]
                }
            )

            print("primary_user_1:",p_user["user"][0][arch][0])
            input("\n")
            print("primary_user_2:",p_user["user"][0][arch][0]["~relations"])
            input()
            for user in p_user["user"][0][arch][0]["~relations"]:
                if "~archertype_hard" in p_user["user"][0][arch][0]["~relations"]:
                    print(user)
                    input()
            if self.primary_user["uid"] in p_user:
                print("VERIFIED_USER:", self.user)
                return p_user
        return None

class GetRelationUsersWithUser(Group, UserWithUserValues):
    """class to create group to four members"""

    def create(self) -> list:

        users_list = []
        relation_user = {}

        schema.load_querys("QueryUserCountry", QueryUserCountry())
        relations.load_class("GetRelationUser", GetRelationUser())

        # Obtenemos las relaciones del usuario.
        for arch, score in arch_score.items():
            print(self.user)
            input()
            relation_user[arch] = relations.execute(
                ManageDataBaseEnv(),
                "QueryData",
                QueryData(DB()),
                "GetRelationUser", 
                schema.exec_query("QueryUserCountry", arch, score),
                {"$uid": self.user["uid"], "$country": self.user["country"]}
            )

            # Obtimizamos la salida.
            operations.select_operation(
                "NormalizeResult", 
                NormalizeResult(arch, relation_user)
            )
            users_list.append(operations.execute("NormalizeResult"))

        users = users_list[0] + users_list[1] + users_list[2]

        operations.select_operation(
            "CheckUsersInGroup",
            CheckUsersInGroup(users, self.user)
        )
        users = operations.execute("CheckUsersInGroup")

        operations.select_operation(
            "GetUsers", 
            GetUsers(users, self.num_members, self.score, self.grp)
        )
        users = operations.execute("GetUsers")
        return users


class ManageGruop:
    """Manage members of group"""
    def __init__(self) -> None:
        self.operation = {}

    def load_class(self, name: str, operation: Group):
        """check"""
        self.operation[name] = operation

    def execute(self, name: str):
        """execute"""
        if name not in self.operation:
            raise ValueError("check not found")
        else:
            # print(name)
            return self.operation[name].create()
