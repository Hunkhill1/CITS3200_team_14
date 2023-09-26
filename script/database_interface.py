import sqlite3
from script.dag import create_unit_graph, highlight_path, visualize_graph
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


def insert_unit_data() -> None:
    """Insert unit data into the database.

    :return: None"""
    unit_data = []

    while True:
        unit_code = input("Enter unit code (or 'exit' to finish): ")
        if unit_code.lower() == 'exit':
            break

        unit_name = input("Enter unit name: ")
        semester = int(input("Enter semester: "))

        unit_data.append((unit_code, unit_name, semester, 'incomplete'))

    # Connect to the database
    connection = sqlite3.connect(constants.degree_db_address)
    cursor = connection.cursor()

    # Insert unit data into the Unit table
    insert_unit_query = """
    INSERT INTO Unit (code,name,semester,status) VALUES (?, ?, ?, ?)
    """
    cursor.executemany(insert_unit_query, unit_data)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    print("Unit data inserted successfully.")


def update_unit_status() -> None:
    """Update the status of a unit in the database.

    :return: None"""
    unit_code = input("Enter the unit code to update status: ")
    new_status = input("Enter the new status: ")

    # Connect to the database
    connection = sqlite3.connect(constants.degree_db_address)
    cursor = connection.cursor()

    # Update the status of the unit
    update_query = """
    UPDATE Unit
    SET status = ?
    WHERE code = ?
    """
    cursor.execute(update_query, (new_status, unit_code))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    print(f"Status of unit {unit_code} updated to {new_status}.")
    
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
        raise Exception("Unit not found in the database")# Unit not found in the database

def insert_prerequisite() -> None:
    """Insert a prerequisite for a unit into the database.

    :return: None"""
    unit_code = input("Enter the unit code to add a prerequisite for: ")
    pre_requisite = input("Enter the prerequisite unit code: ")

    # Connect to the database
    connection = sqlite3.connect(constants.degree_db_address)
    cursor = connection.cursor()

    # Insert the prerequisite into the UnitRelationship table
    insert_query = """
    INSERT INTO UnitRelationship (unit_code, pre_requisite) VALUES (?, ?)
    """
    cursor.execute(insert_query, (unit_code, pre_requisite))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    print(f"Prerequisite {pre_requisite} added for unit {unit_code}.")


def get_all_units() -> list[str]:
    """ Get all units from the database

    Returns:
        list[str]:  List of units
    """    
    conn = sqlite3.connect(constants.degree_db_address)
    cursor = conn.cursor()
    # Fetch data from the Unit table
    cursor.execute("SELECT code, name, semester FROM Unit")
    data_from_database = cursor.fetchall()
    # Close the database connection
    conn.close()
    return data_from_database

def visualize_prerequisites(G) -> None:
    """Visualize the prerequisites path for a unit.

    :param G: The unit graph.
    :return: None"""
    unit_code = input("Enter the unit code: ")

    # Call the functions from graph_visualizer.py directly
    path_nodes = highlight_path(G, unit_code)
    visualize_graph(G, unit_code, path_nodes)


def main() -> None:
    G = create_unit_graph()
    while True:
        print("1. Get Prerequisites")
        print("2. Insert Unit Data")
        print("3. Update Unit Status")
        print("4. Insert Prerequisite")
        print("5. Visualize Prerequisites Path")  # New option
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            unit_code = input("Enter the unit code: ")
            prerequisites = get_prerequisites(unit_code)
            print(f"Prerequisites for unit {unit_code}: {prerequisites}")

        elif choice == '2':
            insert_unit_data()

        elif choice == '3':
            update_unit_status()

        elif choice == '4':
            insert_prerequisite()

        elif choice == '5':
            visualize_prerequisites(G)  # Call the new function

        elif choice == '6':
            break


if __name__ == "__main__":
    # Create the graph
    main()
