import sqlite3

# Create or connect to the database
connection = sqlite3.connect('database/degree_database.db')
cursor = connection.cursor()

# Create the Unit table
create_unit_table_query = """
CREATE TABLE IF NOT EXISTS Unit (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    semester INTEGER
);
"""
cursor.execute(create_unit_table_query)

# Create the UnitRelationship table
create_unit_relationship_table_query = """
CREATE TABLE IF NOT EXISTS UnitRelationship (
    id INTEGER PRIMARY KEY,
    unit_code TEXT NOT NULL,
    related_unit_code TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    FOREIGN KEY (unit_code) REFERENCES Unit (code),
    FOREIGN KEY (related_unit_code) REFERENCES Unit (code)
);
"""
cursor.execute(create_unit_relationship_table_query)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database schema created successfully.")
