import logging
import psycopg2
import os


class PostalCodeDB():

    HOST = os.environ.get("POSTGRES_HOST", "localhost")
    PORT = os.environ.get("POSTGRES_PORT", "5432")
    DATABASE = os.environ.get("POSTGRES_DB", "bia")
    TABLE = "coordinates"
    USER = os.environ.get("POSTGRES_USER", "admin")
    PASSWORD = os.environ.get("POSTGRES_PASSWORD", "admin")

    def copy_file_to_db(self, uuid):
        logging.debug("Copying file to Postgres database")
        file = open(f'./stage/{uuid}.csv')
        con = psycopg2.connect(database=self.DATABASE, user=self.USER, password=self.PASSWORD, host=self.HOST, port=self.PORT)
        cursor = con.cursor()
        cursor.copy_from(file, self.TABLE, sep=",")
        con.commit()
        con.close()
