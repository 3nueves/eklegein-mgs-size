"""Module to process groups"""

# Configuración de logging
import logging
from datetime import datetime, timezone
from abc import ABC, abstractmethod

from app.core.groups import ManageGruop, GetRelationUsersWithUser, GetRelationUserToUser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mgs-group")

date = datetime.now(timezone.utc)
date = date.isoformat()

groups = ManageGruop()

class InterfaceToSelectUsers(ABC):
    """class to select users"""
    @abstractmethod
    def select_users(self, group: dict, users: dict) -> None:
        """select users"""


class InterfaceCheckGroup(ABC):
    """class process"""
    @abstractmethod
    def check_group(self, group) -> dict:
        """init procress to manage teams"""


class GetRelationUsers(InterfaceToSelectUsers):
    """class to realtions users"""
    def select_users(self, group: dict, users: dict) -> bool:
        """select users"""

        grp = []
        sort_users = {}
        users_secundary = ""

        # Obtenemos el número de usuarios del grupo.
        size_group = len(group["Group.users"])

        # Ordenamos el usuario según sea primary, secundary o tertiary.
        # Para ello usamos el número de su posición.
        for position, user in users.items():
            use = user.split("_")
            us = [us for us in group["Group.users"] if use[1]]
            sort_users[position] = us

        # Recorremos los usuarios.
        for position, user in sort_users.items():

            grp.append(user[0])

            # Obtenemos las relaciones según el número de usuarios del grupo
            # y su tipo, primary, secundary, tertiary.
            # Obtenemos los usuarios secundarios
            if position == 0 and size_group == 1:

                # Obtenemos los usuarios secundarios del usuario primario.
                groups.load_class(
                    "GetRelationUsersWithUser",
                    GetRelationUsersWithUser(group, user[0], grp, 2, "score_hard"))
                users_secundary = groups.execute("GetRelationUsersWithUser")
                print("USERS_SECUNDARY:",users_secundary)

                if len(users_secundary) == 1 and "score_hard" in users_secundary[0]:
                    groups.load_class(
                        "GetRelationUsersWithUser",
                        GetRelationUsersWithUser(group, user[0], grp, 1, "score_medium"))
                    users_secundary = users_secundary + groups.execute("GetRelationUsersWithUser")

                elif len(users_secundary) == 0:
                    groups.load_class(
                        "GetRelationUsersWithUser",
                        GetRelationUsersWithUser(group, user[0], grp, 2, "score_medium"))
                    users_secundary = users_secundary + groups.execute("GetRelationUsersWithUser")

                if len(users_secundary) == 1 and "score_medium" in users_secundary[0]:
                    groups.load_class(
                        "GetRelationUsersWithUser",
                        GetRelationUsersWithUser(group, user[0], grp, 1, "score_soft"))
                    users_secundary = users_secundary + groups.execute("GetRelationUsersWithUser")

                elif len(users_secundary) == 0:
                    groups.load_class(
                        "GetRelationUsersWithUser",
                        GetRelationUsersWithUser(group, user[0], grp, 2, "score_soft"))
                    users_secundary = users_secundary + groups.execute("GetRelationUsersWithUser")


                grp = grp + users_secundary

                # Obtenemos los usuarios terciarios de los usuarios secundarios.
                for user_secundary in users_secundary:
                    groups.load_class(
                        "GetRelationUsersWithUser",
                        GetRelationUsersWithUser(group, user_secundary, grp, 50, "score_hard")
                    )
                    users_tertiary = groups.execute("GetRelationUsersWithUser")
                print("USERS_TERTIARY:",users_tertiary)

                # Verificamos que el usuario terciario tiene relación con el usuario primario.
                user_tertiary_verified = []
                for user_tertiary in users_tertiary:
                    groups.load_class(
                        "GetRelationUserToUser",
                        GetRelationUserToUser(group, user_tertiary, grp, user[0])
                    )
                    user_tertiary_verified.append(groups.execute("GetRelationUserToUser"))
                print("USER_TERTIARY:",user_tertiary_verified)


        # # return relation_users

class SortGroup(InterfaceCheckGroup):
    """
    check type of member: Primary, Secundary and Tertiary
    """
    # Nos devuelve un diccionario ordenado por el tipo de usuario.
    def check_group(self, group) -> dict:
        """check type member"""        
        users = {}
        for user in group["Group.date_add_users"]:
            use = user.split("_")
            if int(use[4]) == 0:
                users[0] = user
            elif int(use[4]) == 1:
                users[1] = user
            elif int(use[4]) == 2:
                users[2] = user
            elif int(use[4]) == 3:
                users[3] = user
            else:
                users[4] = user
        input()
        return users


class ManageMembersGroup:
    """Manage members of group"""

    def __init__(self) -> None:
        self.operations = {}

    def add_check(self, name: str, operation: InterfaceCheckGroup):
        """check"""
        self.operations[name] = operation

    def execute(self, name: str, group: dict):
        """execute"""
        if name not in self.operations:
            raise ValueError("check not found")
        else:
            return self.operations[name].check_group(group)

class ManageRelationsMembersGroup:
    """Manage members of group"""

    def __init__(self) -> None:
        self.operations = {}

    def select_relations(self, name: str, operation: InterfaceToSelectUsers):
        """check"""
        self.operations[name] = operation

    def execute(self, name: str, group: dict, users: dict):
        """execute"""
        if name not in self.operations:
            raise ValueError("check not found")
        else:
            return self.operations[name].select_users(group, users)

class Init:
    """Init checks"""
    def __init__(self, group) -> None:
        self.group = group
        self.mmg = ManageMembersGroup()
        self.mrmg = ManageRelationsMembersGroup()
        self.init_checks()

    def init_checks(self):
        """init"""
        self.mmg.add_check("SortGroup", SortGroup())
        self.mrmg.select_relations("GetRelationUsers", GetRelationUsers())

        sort_members = self.mmg.execute("SortGroup", self.group)
        return self.mrmg.execute("GetRelationUsers", self.group, sort_members)
