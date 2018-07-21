# -*- coding: utf-8 -*-


class AttModel(object):

    def __init__(self, connection):
        self.connection = connection

    def create_tmp_table_att(self):
        """ Create temporary att table on Database """
        query_tmp = """ CREATE TEMPORARY TABLE tmp_att
                    ( pin character varying
                     , marcacion timestamp without time zone
                     , nombre character varying
                    ) """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query_tmp)
        except Exception as e:
            self.connection.rollback()
            raise Exception("Fail on create tmp att, ", e)

    def insert_data_to_tmp_table_att(self, rows):
        """ Insert data from rows to att tmp table """
        insert_query = """ INSERT INTO tmp_att
                         ( pin
                          , marcacion
                          , nombre
                         )
                          VALUES
                         (
                             %s
                            ,%s
                            ,%s
                          )
        """
        try:
            cursor = self.connection.cursor()
            for row in rows:
                cursor.execute(insert_query, (row))
        except Exception as e:
            self.connection.rollback()
            raise Exception(" Fail on insert data to tmp_att table,  ", e)

    def insert_diff_data_from_tmp_to_att(self):
        """ Insert diff data from tmp_att to att table """
        diff_query = """
                        INSERT INTO att
                        (SELECT pin, marcacion, nombre
                          FROM tmp_att

                        EXCEPT

                        SELECT pin, marcacion, nombre
                         FROM att
                        )
                    """
        try:
            cursor = self.connection.cursor()
            cursor.execute(diff_query)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            raise Exception("Fail on insert diff tmp_att to att, ", e)


class AttReloj(object):

    def __init__(self, connection, nombre="", ip=""):

        self.nombre = nombre
        self.ip = ip
        self.connection = connection

    def get_cursor_reloj(self):
        """ Get all records from Database """

        list_query = """
            SELECT id, nombre, ip
              FROM reloj
        """
        cursor = None

        try:
            cursor = self.connection.cursor()
            cursor.execute(list_query)
            self.connection.commit()

        except Exception as e:
            self.connection.rollback()
            raise Exception("Fail to load records (Reloj) from Database, ", e)

        return cursor
