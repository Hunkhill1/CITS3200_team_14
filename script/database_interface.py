"""
database_interface.py

This module serves as the interface for managing unit data within the study planner application's SQLite database.

Contents:
- Functions to interact with the database, including retrieving unit prerequisites, semesters, and all available units.
- Functions to insert unit data and prerequisites into the database.

Usage:
1. This module is responsible for handling interactions with the study planner's database, such as querying and inserting unit-related data.
2. It offers functions for accessing prerequisites, semesters, and unit details.
3. Functions for inserting new unit data and prerequisites are available.
4. The database connection parameters are imported from the constants module.
"""


import sqlite3
import script.constants as constants


def get_prerequisites(unit_code: str) -> list[str]:
    """Get the prerequisites for a unit

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
        
def add_unit(unit_code: str, name: str, unit_points_required: int, semester: int, category_id: int) -> None:
    
    with sqlite3.connect(constants.degree_db_address) as connection:
        cursor = connection.cursor()

        insert_unit_query = """
        INSERT INTO Unit (code, name, unit_points_required, semester, category_id) VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(insert_unit_query, (unit_code, name, unit_points_required, semester, category_id))
    connection.close()
        
def delete_unit_by_code(unit_code: str) -> None:
    """Delete a unit by its code from the database.

    Args:
        unit_code (str): Unit code to delete.
    """
    with sqlite3.connect(constants.degree_db_address) as connection:
        cursor = connection.cursor()

        # Delete the unit based on its code
        delete_query = """
        DELETE FROM Unit
        WHERE code = ?
        """
        cursor.execute(delete_query, (unit_code,))

    # Close the connection
    connection.close()

def edit_units(unit_code: str, name: str, unit_points_required: int, semester: int, category_id: int) -> None:
    """Edit unit attributes in the database.

    Args:
        unit_code (str): Unit code to identify the unit to be edited.
        name (str): New unit name.
        unit_points_required (int): New unit points required.
        semester (int): New unit semester.
        category_id (int): New category ID.

    Raises:
        Exception: If the unit does not exist in the database.
    """
    # Create or connect to the database
    connection = sqlite3.connect(constants.degree_db_address)
    cursor = connection.cursor()

    # Check if the unit exists in the database
    #cursor.execute("SELECT COUNT(*) FROM Unit WHERE code=?", (unit_code,))
    #unit_exists = cursor.fetchone()[0]
    

    #if unit_exists == 0:
        #connection.close()
        #raise Exception("Unit not found in the database.")

    # Update the unit attributes
    update_unit_query = """
    UPDATE Unit
    SET name=?, unit_points_required=?, semester=?, category_id=?
    WHERE code=?
    """
    cursor.execute(update_unit_query, (name, unit_points_required, semester, category_id, unit_code))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    print(f"Unit '{unit_code}' updated successfully.")
    
def get_unit_semester(unit_code: str) -> int:
    """Get the semester of a unit

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
    """Get all units from the database

    Returns:
        list[str]:  List of units
    """
    conn = sqlite3.connect(constants.degree_db_address)
    cursor = conn.cursor()
    cursor.execute("SELECT code, name,semester FROM Unit")
    data_from_database = cursor.fetchall()
    conn.close()
    return data_from_database


def get_all_units_everything() -> list[str]:
    """Get all units from the database

    Returns:
        list[str]:  List of units
    """
    conn = sqlite3.connect(constants.degree_db_address)
    cursor = conn.cursor()
    cursor.execute("SELECT code, name, unit_points_required, semester, category_id FROM Unit")
    data_from_database = cursor.fetchall()
    conn.close()
    return data_from_database