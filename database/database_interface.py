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

# Example usage
unit_code = "GENG2003"
prerequisites = get_prerequisites(unit_code)
print(f"Prerequisites for unit {unit_code}: {prerequisites}")
