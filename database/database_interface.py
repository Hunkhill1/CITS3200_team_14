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

# Example usage
# unit_code = "GENG2003"
# prerequisites = get_prerequisites(unit_code)
# print(f"Prerequisites for unit {unit_code}: {prerequisites}")
if __name__ == "__main__":
    insert_unit_data()
