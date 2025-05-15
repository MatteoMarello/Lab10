from database.DB_connect import DBConnect
from model.country import Country
from model.arco import Arco


class DAO():
    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = {}
        query = """select * 
                    from countries.country c """

        cursor.execute(query)

        for row in cursor:
            result[row["CCode"]] = Country(**row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(anno_selezionato):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """SELECT DISTINCT c.state1no as s1, c.state2no as s2
                       FROM countries.contiguity c 
                       WHERE c.conttype = 1 AND c.year <= %s"""

        cursor.execute(query, (int(anno_selezionato),))

        for row in cursor:
            result.append(Arco(row["s1"], row["s2"]))

        cursor.close()
        conn.close()
        return result
