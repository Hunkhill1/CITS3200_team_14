import sqlite3
import constants as constants

# Create or connect to the database
connection = sqlite3.connect(constants.degree_db_address)
cursor = connection.cursor()

# Create the Unit table
create_unit_table_query = """
CREATE TABLE IF NOT EXISTS Unit (
    code TEXT PRIMARY KEY, 
    name TEXT ,
    semester INTEGER,
    status TEXT DEFAULT 'incomplete'
);
"""
cursor.execute(create_unit_table_query)

# Create the UnitRelationship table
create_unit_relationship_table_query = """
CREATE TABLE IF NOT EXISTS UnitRelationship (
    unit_code TEXT,
    pre_requisite TEXT,
    FOREIGN KEY (unit_code) REFERENCES Unit (code),
    FOREIGN KEY (pre_requisite) REFERENCES Unit (code)
);
"""
cursor.execute(create_unit_relationship_table_query)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database schema created successfully.")
