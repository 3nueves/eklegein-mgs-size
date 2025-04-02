"""Module to get four users"""
# Configuración de logging
import logging
from datetime import datetime, timezone

from app.utils.utils import Utils
from app.database.db import DB
from app.database.schemas import Schema
from app.database.schemas_users import UserSchema
from app.core.relations.relations_to_four_users import Relations

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("worker-four")

date = datetime.now(timezone.utc)
date = date.isoformat()


class GetFourUsers:
    """class process"""

    def __init__(self, users_sorted: dict) -> None:
        self.users_sorted = users_sorted
        self.db = DB()
        self.schema = Schema()
        self.schema_users = UserSchema()
        self.utils = Utils("templates")
        self.relations = Relations()
        self.group_userst = []
        self.date_add_users = []
        self.primary_user = ""


    def get_users(self, group: dict) -> bool:
        """Groups one users"""
        # Obtener 4 usuarios.

        grp = []
        grp_tertiary = []

        # Comprobamos que la posición del usuario sea 0 si no es así se la cambiamos.
        self.users_sorted = self.relations.verify_position_user(self.users_sorted, group)
        # print(self.users_sorted)
        # input()

        # Buscamos dos usuarios secundarios
        user = group["Group.users"][0]
        print(user)
        input()
        self.primary_user = user
        print("uid:", user["uid"])
        print("email:", user["User.email"])
        print("country:", user["country"])

        # Añadirmos el usuario principal a la lista de usuarios.
        grp.append(user)

        users = self.relations.get_relations(user, user["country"])
        print("\nUSUARIO PRIMARIO: ",user["uid"])
        print("\nUSUARIOS1:",users)
        input("#######################################")

        users = self.relations.check_user_is_in_group(user["uid"], users)
        print("\nPRIMARY USER: ",user["uid"])
        print("\nUSERS2 ====> ",users)
        input("##################################")

        if not user:
            return False

        # Buscamos los usuarios terciarios.
        users_secundary = self.relations.get_users(users, 1, 2, grp)
        grp = grp + users_secundary
        print("\nGRUPO TMP CON EL USUARIO PRIMARIO Y SECUNDARIOS:")
        print(grp)
        input()

        count = 0

        for user_secundary in users_secundary:

            count += 1

            print("uid:", user_secundary["uid"])
            print("email:", user_secundary["User.email"])
            print("country:", user_secundary["country"])

            users = self.relations.get_relations(user_secundary, user_secundary["country"])
            print("\nPRIMARY USER: ",user_secundary)
            print("\nUSERS4 ====> ",users)
            input("##################################")
            users = self.relations.check_user_is_in_group(user_secundary, users)
            print("\nPRIMARY USER: ",user_secundary)
            print("\nUSERS5 ====> ",users)
            input("##################################")


            if not users:
                return False

            users_tertiary = self.relations.get_users(users, 1, 8, grp)

            # Buscamos si los usuarios terciarios tienen afinidad con el usuario primario.
            for user_tertiary in users_tertiary:
                user_primary_verified = self.relations.get_relations(
                    user_tertiary,
                    user_tertiary["country"],
                    self.primary_user
                    )

                print("\nPRIMARY USER: ",user_tertiary)
                print("\nUSERS6 ====> ",user_primary_verified)
                input("##################################")
                input()

                if user_primary_verified:
                    grp_tertiary.append(user_tertiary)

                    print("COUNT", count)
                    print("GRP_TERTIARY:",len(grp_tertiary))
                    print(grp_tertiary)
                    if len(grp_tertiary) > 1 and count == 1:
                        print("Mas de 1 usuario")
                        grp_tertiary = grp_tertiary[:1]
                        print(grp_tertiary)
                    if len(grp_tertiary) > 2 and count == 2:
                        print("Mas de 2 usuario")
                        grp_tertiary = grp_tertiary[:2]
                        print(grp_tertiary)
                    input("final_user\n")

        grp = grp + grp_tertiary
        print(grp)

        # Si algún usuario está en estado "OnHold" el grupo todavía
        # no está completado hasta que todos los usuarios esten en modo Blocked.
        # Si el grupo no alcanza los 5 usuarios también lo colocaremos en Pending.
        grupo_status, mails_users_on_hold, mails_users_on_blocked = self.relations.change_user_status(grp)

        # if grupo_status != "Pending":
        #     grupo_status = "Complete"

        if len(grp) < 5:
            grupo_status = "Pending"

        # # Añadimos una lista de diccionarios al grupo que vamos a crear
        # # con la fecha y el orden en la que se añadieron los usuarios.
        list_date_users: list = []

        for num, us_gr in enumerate(grp):
            print(us_gr)
            # input("US_GR")
            user_dict = us_gr["User.email"] + "_" + us_gr["uid"] + "_" + us_gr["join_to_team"] + "_" + date + "_" + str(num) + "_" + us_gr["country"]
            print(user_dict)
            # Verificamos que el usuario no sea el usuario 0.
            use = user_dict.split("_")
            if use[4] != "0":
                list_date_users.append(user_dict)
            print("LISTA DE date_add_users",list_date_users)
            input()


        if len(grp) >= 1:
            # grupo_status = "Completed"
            update_group = {
                "uid": group["uid"],
                "Group.name": "Sin Nombre",
                "Group.status": grupo_status,  
                "Group.users": grp,
                "Group.date_add_users": list_date_users
                }
            print(update_group)
            input("UPDATE_GROUP")
            self.db.create_data(update_group)

        team = self.db.query_data(self.schema.query_group, {"$uid": group["uid"]})
        logger.info("Grupo actualizado: %s", team)

        # Enviamos las notificaciones por email.
        for mail_user_on_hold in mails_users_on_hold:
            self.utils.send_email(mail_user_on_hold, "mail.html", update_group)

        join_all_user = []
        join_all_user.append(user["uid"])
        join_all_user = [join_all_user["uid"] for join_all_user in grp]
        print(join_all_user)
        input("JOIN")

        for user_uid in join_all_user:
            user = {"uid": user_uid, "groups": update_group}
            self.db.create_data(user)

        print(users)
        input("Pause_1")
        return True
