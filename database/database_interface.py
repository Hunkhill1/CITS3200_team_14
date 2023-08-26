import sqlite3

def get_prerequisites(unit_code):
    # Connect to the database
    connection = sqlite3.connect('database/degree_database.db')
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

def insert_unit_data():
    unit_data = []

    while True:
        unit_code = input("Enter unit code (or 'exit' to finish): ")
        if unit_code.lower() == 'exit':
            break

        unit_name = input("Enter unit name: ")
        semester = int(input("Enter semester: "))

        unit_data.append((unit_code, unit_name, semester, 'incomplete'))

    # Connect to the database
    connection = sqlite3.connect('database/degree_database.db')
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

def update_unit_status():
    unit_code = input("Enter the unit code to update status: ")
    new_status = input("Enter the new status: ")

    # Connect to the database
    connection = sqlite3.connect('database/degree_database.db')
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

def insert_prerequisite():
    unit_code = input("Enter the unit code to add a prerequisite for: ")
    pre_requisite = input("Enter the prerequisite unit code: ")

    # Connect to the database
    connection = sqlite3.connect('database/degree_database.db')
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

def test_run():
    # Example usage
    # unit_code = "GENG2003"
    # prerequisites = get_prerequisites(unit_code)
    # print(f"Prerequisites for unit {unit_code}: {prerequisites}")
    if __name__ == "__main__":
        update_unit_status()

test_run()

