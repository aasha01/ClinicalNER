import mysql.connector as mysqlCon
import mysql.connector

import pickle as pkl


def get_connection():
    conn = connect_umls('aasha', '********', 'localhost', 'umls')
    return conn


def connect_umls(uname, password, host, database):
    connection = mysqlCon.connect(user=uname, password=password,
                                  host=host, database=database)
    return connection


def close_connection(connection):
    connection.close()


def get_entity(string):
    """ get definitions/descriptions for the given string """
    try:
        # Get descritpions
        sql_select_Query = "select * from mrconso where STR like '" + string + "';"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql_select_Query)
        # get all records
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e.msg)
        return ""
    finally:
        close_connection(conn)


def symantic_type_lookup(string):
    """ get definitions/descriptions for the given string """
    """ Get Semantic Typ for a given string """
    try:
        # Get descritpions
        # sql_select_Query = "select * from mrconso where STR like '" + string + "';"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT sty FROM MRCONSO a, MRSTY b WHERE a.cui = b.cui AND str = %s; ", (string,))
        # get all records
        next_user = cursor.fetchone()
        if next_user is not None:
            user_blah = next_user[0]
        else:
            user_blah = ''
        return user_blah
    except mysql.connector.Error as e:
        print(e.msg)
        return ""
    finally:
        close_connection(conn)


def is_symantic_type_found(string):
    """ find whether any semantic type available for the given string """
    """ return True if semantic type is available otherwise return False """
    try:
        sem_type_list = symantic_type_lookup(string)
        if not sem_type_list:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False


def cui_lookup(string):
    """ get definitions/descriptions for the given string """
    """ Get Semantic Typ for a given string """
    try:
        # Get descritpions
        # sql_select_Query = "select * from mrconso where STR like '" + string + "';"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT cui FROM MRCONSO WHERE str = %s;", (string,))
        #row = cursor.fetchone()
        next_user = cursor.fetchone()
        if next_user is not None:
            user_blah = next_user[0]
        else:
            user_blah = ''
        return user_blah
    except mysql.connector.Error as e:
        print(e.msg)
        return ""
    finally:
        close_connection(conn)


def is_cui_found(string):
    """ find whether any semantic type available for the given string """
    """ return True if semantic type is available otherwise return False """
    try:
        sem_type_list = cui_lookup(string)
        if not sem_type_list:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False
