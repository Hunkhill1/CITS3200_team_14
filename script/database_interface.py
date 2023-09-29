import sqlite3
import script.constants as constants


def get_prerequisites(unit_code:str)->list[str]:
    """ Get the prerequisites for a unit

    Args:
        unit_code (str):  Unit code to search for

    Returns:
        list[str]:  List of prerequisites for the unit
    """    
    # Connect to the database
    connection = sqlite3.connect(constants.degree_db_address)
    cursor = connection.cursor()

    # Query prerequisites based on unit code
    query = """
    SELECT pre_requisite
    FROM UnitRelationship
    WHERE unit_code = ?
    """
    
    cursor.execute(query, (unit_code,))
    prerequisites = [row[0] for row in cursor.fetchall()]

    # Close the connection
    connection.close()

    return prerequisites


def insert_unit_data(unit_data: list[tuple]) -> None:
    """Insert unit data into the database.

    Args:
        unit_data (list[tuple]): List of tuples containing unit data.
    """
    with sqlite3.connect(constants.degree_db_address) as connection:
        cursor = connection.cursor()

        insert_unit_query = """
        INSERT INTO Unit (code, name, semester) VALUES (?, ?, ?)
        """
        cursor.executemany(insert_unit_query, unit_data)


def get_unit_semester(unit_code:str)->int:
    """ Get the semester of a unit

    Args:
        unit_code (str):  Unit code to search for

    Returns:
        int:  Semester of the unit
    """ 
    # Connect to the database
    connection = sqlite3.connect(constants.degree_db_address)
    cursor = connection.cursor()

    # Query the semester based on unit code
    query = """
    SELECT semester
    FROM Unit
    WHERE code = ?
    """

    cursor.execute(query, (unit_code,))
    result = cursor.fetchone()

    # Close the connection
    connection.close()

    if result:
        return result[0]  # Extract the semester from the result
    else:
        raise Exception("Unit not found in the database")

def insert_prerequisite(unit_code: str, pre_requisite: str) -> None:
    """Insert a prerequisite for a unit into the database.

    Args:
        unit_code (str): Unit code to add a prerequisite for.
        pre_requisite (str): Prerequisite unit code.
    """
    with sqlite3.connect(constants.degree_db_address) as connection:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO UnitRelationship (unit_code, pre_requisite) VALUES (?, ?)
        """
        cursor.execute(insert_query, (unit_code, pre_requisite))
    # Close the connection
    connection.close()


def get_all_units() -> list[str]:
    """ Get all units from the database

    Returns:
        list[str]:  List of units
    """    
    conn = sqlite3.connect(constants.degree_db_address)
    cursor = conn.cursor()
    cursor.execute("SELECT code, name, semester FROM Unit")
    data_from_database = cursor.fetchall()
    conn.close()
    return data_from_database
