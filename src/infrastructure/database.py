import logging
import psycopg2


class PostalCodeDB():

    HOST = "localhost"
    PORT = 5432
    DATABASE = "bia"
    TABLE = "coordinates"

    def copy_file_to_db(self, uuid):
        logging.debug("Copying file to Postgres database")
        file = open(f'./stage/{uuid}.csv')
        con = psycopg2.connect(database=self.DATABASE, user="admin", password="admin", host=self.HOST, port=self.PORT)
        cursor = con.cursor()
        cursor.copy_from(file, self.TABLE, sep=",")
        con.commit()
        con.close()
