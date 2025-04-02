"""class to create groups"""

import logging

from app.database.schemas import Schema
from app.database.schemas_users import UserSchema
from app.database.db import DB
from app.utils.data import Data

logger = logging.getLogger("group")

class Relations:
    """class to create relations"""
    def __init__(self) -> None:
        self.schema = Schema()
        self.schema_users = UserSchema()
        self.data = Data()
        self.db = DB()
        self.match_team: bool = False
        self.relations_users: list = []
        self.users_without_shered_grups: list = []
        self.relation_users_dict: dict = {}
        self.dict_arch_type = {
            "archetype_hard":   "score_hard",
            "archetype_medium": "score_medium",
            "archetype_soft":   "score_soft"
        }

    def verify_position_user(self, users_sorted: dict, group: dict) -> dict:
        """verify postions"""
        # Verificamos si el usuario tiene la posición 0 si no la tiene se la cambiamos a 0.
        rectified_users = {}
        for user in users_sorted.values():
            us = user.split("_")
            if us[4] != "0":
                # Borramos el elemento en la lista "Group.date_add_users"
                delete_user = {"uid": group["uid"], "Group.date_add_users": user}
                self.db.delete_data(delete_user)
                # Cambiamos el valor en el elemanto y lo guardamos en la db.
                user = user.replace(f"_{us[4]}_", "_0_")
                # Actualizamos el elemento que indica el estado del usuario
                # dentro de la lista date_add_user.
                group["Group.date_add_users"][0] = user
                add_user = {"uid": group["uid"], "Group.date_add_users": user}
                self.db.create_data(add_user)
                # Guardamos el usuario rectificado.
                rectified_users[0] = user
            else:
                return users_sorted
        return rectified_users


    def get_relations(
            self,
            user: dict,
            country: str = None,
            second_user: dict = None,
            sector: str = None
        ) -> dict:
        """Obtenemos los usuarios relacionados con el usuario principal"""
        print(f"\nPRIMARY_USER: {user["User.name"]}")
        save_relation_users: dict = {}
        self.relation_users = {}
        self.users_without_shered_grups = []
        for archetype, score in self.dict_arch_type.items():
            print("\nDentro del bucle get_relations\n")
            print("ARCHETYPE:",archetype,"\n")
            if country and sector:
                query_user = self.schema.query_user_country_sector(archetype, score)
                save_relation_users[archetype] = self.db.query_data(
                    query_user,
                    {"$uid": user["uid"], "$country": country, "$sector": sector}
                )
            elif country and not second_user:
                query_user = self.schema.query_user_country(archetype, score)
                save_relation_users[archetype] = self.db.query_data(
                    query_user,
                    {"$uid": user["uid"], "$country": country}
                )
            elif country and second_user:
                query_user = self.schema_users.query_user_country_user(archetype, score)
                save_relation_users[archetype] = self.db.query_data(
                    query_user,
                    {"$uid": user["uid"], "$country": country, "$uid_second": second_user["uid"]}
                )
                print(query_user)
                input()
            else:
                query_user = self.schema.query_user_one(archetype, score)
                save_relation_users[archetype] = self.db.query_data(
                    query_user,
                    {"$uid": user["uid"]}
                )

            relations = [relations[0]["~relations"]
                        for relations in [user[archetype]
                        for user in list(save_relation_users[archetype]['user'])]]

            relations = relations[0] if relations else []

            print("RELATIONS:", relations)
            print("-----------------------------------")
            input()

            self.optimize_result(relations, archetype)

        return self.relation_users


    def optimize_result(self, relations: list, archetype: str) -> None:
        """
        Parsea las relaciones de los usuarios
        """
        # Construimos la key que irá como primer key del dict.
        print("Dentro de optimize\n")
        print("\nUSUARIOS DEL POOL:", archetype)
        users_list = []
        for pool_user in relations:
            if f'~{archetype}' in pool_user:
                for user in pool_user[f'~{archetype}']:
                    print("USER:", user)
                    users_list.append(user)
                    self.relation_users[archetype] = users_list
        print("\nUSUARIOS:",self.relation_users)
        print("\nUSUARIOS_OPTIMIZADOS:")
        for arch in self.relation_users.items():
            print(arch)
        input("----------------------------------------")


    def check_user_is_in_group(self, primary_user: dict,  users: dict) -> dict:
        """
        Verifica que el usuario primario no tiene el usuario 
        secundario ya en un grupo suyo.
        """
        print(primary_user)
        print(users)
        print("\nDentro de check_user_is_in_group\n")
        for archetype, user in users.items():
            print("\nARCHETYPE:",archetype)
            print("USUARIO PRIMARIO:",primary_user)
            print("USUARIOS:",user,"\n")
            for use in user:
                print("USUARIO:",use)
                if "groups" in use and "groups" in primary_user:
                    for group in use["groups"]:
                        print("GRUPOS:", group)
                        input()
                        if group in primary_user["groups"]:
                            user.remove(use)
        input("----------------------------------------")
        return users


    def get_users(self, users: dict, positon_user_in_list: int, num_users: int, grp: list) -> dict:
        """Split users"""
        # Obtenemos los usuarios que necesitamos.
        print("\nDentro de get_users")
        list_users = []
        for archetype, user in users.items():
            print("\nARCHETYPE:",archetype)
            print("\nUSERS:",user)
            user = self.check_user_is_in_tmp_group(user, grp)
            if len(user) >= 1:
                print("\nUSUARIO ELEGIDO:",user[:positon_user_in_list][0])
                list_users.append(user[:positon_user_in_list][0])
                print(len(list_users))
                print(num_users)
                input("...........")
            if len(list_users) >= num_users:
                print("\nLISTA DE USUARIOS FINAL",list_users)
                input("----------------------------------------")
                return list_users
        print("\nLISTA DE USUARIOS FINAL",list_users)
        input("----------------------------------------")
        return list_users


    def find_primary_user_in_tertiary_user(
            self,
            primary_user: dict,
            user_tertiary: dict,
            users: dict,
            grp_tertiary: list
        ) -> list:
        """Find primary user in users from tertary user"""
        # Buscamos entre los usuarios relacionados con los
        # usuarios terciarios si tienen el usuario primario.
        for arch, users in users.items():
            print("\nDentro de find_primary_user_in_tertiary_user\n")
            print("=====Final User======\n")
            print("ARCHETYPE:",arch)
            print("USERS:",users)
            for user in users:
                print(user["uid"])
                print(primary_user["uid"])
                input(":::::::::::::::::::::")
                if primary_user["uid"] == user["uid"]:
                    print("MATCH")
                    print(user)
                    if user_tertiary not in grp_tertiary:
                        grp_tertiary.append(user_tertiary)
                    else:
                        print(grp_tertiary)
                        print("USER REPEAT:", user_tertiary)
                        input("\n")
                    print("COUNT")
                    print("GRP_TERTIARY:",len(grp_tertiary))
                    print(grp_tertiary)
                    input("grp_tertiary")
                    input("\n")
        return grp_tertiary


    def check_user_is_in_tmp_group(self, users: list, group_tmp: list) -> list:
        """Check user in temporal grupo"""
        print("\nDentro de check_user_is_in_tmp_group\n")
        # Verificamos que el usuario seleccionado no esta ya
        # en la lista de usuarios seleccionados para formar
        # el grupo.
        for user in users:
            for user_group in group_tmp:
                print("USER",user["uid"])
                print("USER FROM GROUP",user_group["uid"])
                print()
                if user["uid"] == user_group["uid"]:
                    print()
                    print("MATCH:", user)
                    users.remove(user)
                    print()
        print("USUARIOS_NO_REPETIDOS")
        print(users)
        input("------------------------------------")
        return users

    def change_user_status(self, users: dict) -> str:
        """
        Comprueba el estado del usuario:
        - Finding => Busca un grupo y unirte ya.
        - Standby => Esta a la espera de que le notifiquen si desea entrar en un grupo.
        - OnHold =>  Ha recibido una notificación de unirse al grupo pero todavía no ha aceptado.
        - Blocked => No quiere entrar en ningún grupo porque ya está en uno.
        """
        user_send_mail_onhold = []
        user_send_mail_blocked = []
        group_status: str = None
        for user in users:
            print(user)
            input("Change Status")

            if user["join_to_team"] == "StandBy":
                change_status_join = {
                    "uid": user["uid"], 
                    "join_to_team": "OnHold"
                }
                print(change_status_join)
                self.db.create_data(change_status_join)
                user["join_to_team"] = "OnHold"

                user_send_mail_onhold.append(user["User.email"])
                group_status = "Pending"
                print(user)
                input("Change Status 2")

            if user["join_to_team"] == "Finding":
                change_status_join = {
                    "uid": user["uid"], 
                    "join_to_team": "Blocked"
                }
                self.db.create_data(change_status_join)
                user["join_to_team"] = "Blocked"
                user_send_mail_blocked.append(user["User.email"])

        return group_status, user_send_mail_onhold, user_send_mail_blocked

    def manage_registry_group(self, registry: str, group: dict) -> list:
        """manage regitry group"""

        # Administramos los cambios que se producen en el registro del grupo.
        # No SE Esta Usando.
        users = group["Group.date_add_users"]
        reg = registry.split("_")

        for user in users:
            use = user.split("_")

            if reg[1] in use[1]:
                users.remove(user)
                users.append(registry)

                delete_user = {
                    "uid": group["uid"],
                    "Group.date_add_users": user
                }
                self.db.delete_data(delete_user)

                update_date_add_users = {
                    "uid": group["uid"],
                    "Group.date_add_users": registry
                }
                self.db.create_data(update_date_add_users)
        return users
