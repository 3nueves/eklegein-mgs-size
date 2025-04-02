""" Module data """

import json
import logging

import logging.config
from typing import Union

import pydgraph

from app.config.settings import Settings

settings = Settings()

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger("database")

DB_NAMESPACE = settings.db_namespace
DB_USER = settings.db_user
DB_PASS = settings.db_pass
DB_HOST = settings.db_host
DB_PORT = settings.db_port

class DB:
    """connection to db"""

    def __init__(self) -> None:

        # create connection
        self.client, self.stub = self.__create_connection()

        # check connection
        self.check = self.check_connetion()


    def __create_connection(self) -> dict:
        """create connection"""
        # Create a client stub.
        stub = pydgraph.DgraphClientStub(f"{DB_HOST}:{DB_PORT}")

        # Create a client.
        client = pydgraph.DgraphClient(stub)
        return client, stub

    def close_connection(self):
        """Cierra la conexión con Dgraph."""
        if self.stub:
            self.stub.close()
            logger.info("Conexión cerrada con Dgraph")

    def check_connetion(self) -> Union[dict, None]:
        """
        Get the current schema from Dgraph
        Returns:
            dict: Schema information
        """
        try:
            # Query to get schema information
            query: dict = """
            schema {}
            """

            response = self.client.txn(read_only=True).query(query)
            return json.loads(response.json)

        except ConnectionError as e:
            logger.error("Error getting schema: %s", str(e))
            return None

    def delete_data(self, uid: dict) -> dict:
        """delete data with uid"""

        txn = self.client.txn()

        try:
            response = txn.mutate(del_obj=uid)
            _ = txn.commit()

            return response.uids

        except pydgraph.AbortedError as error:
            logger.error("Aborted connection: %s", error)

        finally:
            # Clean up. Calling this after txn.commit() is a no-op and hence safe.
            txn.discard()

    def create_data(self, mutate: dict) -> dict:
        """create data using json"""

        # data = pydgraph.Mutation(set_json=json.dumps(mutate).encode("utf8"))

        txn = self.client.txn()

        try:
            # Run mutation.
            response = txn.mutate(set_obj=mutate)

            # Commit transaction.
            _ = txn.commit()

            return response.uids

            # Get uid of the outermost object (person named "Alice").
            # response.uids returns a map from blank node names to uids.
            # print(f'Created person named "David" with uid = {response}')

        except pydgraph.AbortedError as error:
            logger.error("Aborted connection: %s", error)

        finally:
            # Clean up. Calling this after txn.commit() is a no-op and hence safe.
            txn.discard()

    # Query for data.
    def query_data(self, query: json, ob: dict = None) -> json:
        """run query"""

        # Run query.
        txn = self.client.txn()

        try:

            if ob:
                variables = ob
                res = txn.async_query(query, variables=variables, resp_format="JSON")
                res = pydgraph.Txn.handle_query_future(res)
                return json.loads(res.json)

            else:
                res = txn.async_query(query)
                res = pydgraph.Txn.handle_query_future(res)
                return json.loads(res.json)

        except pydgraph.AbortedError as error:
            logger.error("Aborted connection: %s", error)

        finally:
            # Clean up. Calling this after txn.commit() is a no-op and hence safe.
            txn.discard()
