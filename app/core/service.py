"""Service to create groups"""

import os
import time
import logging
from typing import Any, Dict
from datetime import datetime, timezone

from app.database.db import DB
from app.database.schemas import Schema
from app.core.process import Init

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mgs")
date = datetime.now(timezone.utc)
date = date.isoformat()


class ManageGrupsService:
    """Class to monitoring join status"""
    def __init__(self, interval: int = 60):
        self.db = DB()
        # self.relations = Relations()
        self.schema = Schema()
        self.interval = interval
        self.last_value = None


    def query_groups(self) -> Dict[str, Any]:
        """Buscamos todos los usuarios"""
        return self.db.query_data(self.schema.query_all_groups)


    def process_value(self, group: Dict[str, Any]):
        """Administramos los estados de los grupos"""
        check = Init(group)

        if check:
            # process.change_state_join()
            print("----------END PROCESS----------")

    def run(self):
        """Ejecuta el servicio de monitoreo."""
        logger.info("Service MGS Started...")

        try:
            while True:
                try:
                    result = self.query_groups()
                    # print("\n\nRESULT",result,"\n\n")

                    # Procesa cada valor encontrado
                    for group in result.get('group', []):
                        # print("----------INIT PROCESS----------")
                        print(group["uid"])
                        current_value = group["Group.status"]
                        current_group = group["uid"]

                        # Si el valor ha cambiado
                        print(group)
                        if current_value == "Pending" or current_value == "Open":
                            logger.info("Group %s status : %s", current_group, current_value)
                            # Procesamos el grupo.
                            self.process_value(group)

                        time.sleep(self.interval)
                        # logger.info("Working...")

                except Exception as e:
                    logger.error("Error en el servicio: %s", str(e))
                    raise
                    # self.db.close_connection()

        except KeyboardInterrupt:
            logger.info("Deteniendo el servicio...")
            self.db.close_connection()

def main():
    """
    main
    """
    # Configuración desde variables de entorno
    interval = int(os.getenv("MONITOR_INTERVAL", "1"))

    # Iniciar el servicio
    service = ManageGrupsService(
        interval=interval
    )

    service.run()
