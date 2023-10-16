"""
create_database.py

This script initializes and configures a SQLite database for the study planner application.

Contents:
- Database creation and table setup for unit categories, units, and unit relationships.
- Configuration parameters imported from the constants module.

Usage:
1. Run this script to create and configure the SQLite database for the study planner.
2. It creates tables for unit categories, units, and unit relationships.
3. It inserts predefined unit categories.
4. It sets up the necessary database schema for the application.
"""

import sqlite3
import constants as constants

# Create or connect to the database
connection = sqlite3.connect(constants.degree_db_address)
cursor = connection.cursor()

# Create the UnitCategory table to store unit categories
create_unit_category_table_query = """
CREATE TABLE IF NOT EXISTS UnitCategory (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL
);
"""
cursor.execute(create_unit_category_table_query)

# Insert data into the UnitCategory table for the categories
categories_data = [
    ('core',),
    ('broadening',),
    ('option',),
    ('Group A',),  # Sub-category 1 for option units
    ('Group B',),  # Sub-category 2 for option units
]

insert_category_query = """
INSERT INTO UnitCategory (category_name) VALUES (?)
"""

cursor.executemany(insert_category_query, categories_data)

# Create the Unit table with unit points and the new category_id column
create_unit_table_query = """
CREATE TABLE IF NOT EXISTS Unit (
    code TEXT PRIMARY KEY,
    name TEXT,
    unit_points_required INTEGER,
    semester INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES UnitCategory (category_id)
);
"""
cursor.execute(create_unit_table_query)

# Modify the UnitRelationship table to reference unit points and categories
create_unit_relationship_table_query = """
CREATE TABLE IF NOT EXISTS UnitRelationship (
    unit_code TEXT,
    pre_requisite TEXT,
    FOREIGN KEY (unit_code) REFERENCES Unit (code),
    FOREIGN KEY (pre_requisite) REFERENCES Unit (code),
    PRIMARY KEY (unit_code, pre_requisite)
);
"""
cursor.execute(create_unit_relationship_table_query)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database schema updated successfully.")
