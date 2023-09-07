import sqlite3
from typing import List
import datetime


# Create an SQLite database and a table to store study units
conn = sqlite3.connect('study_units.db')
cursor = conn.cursor()

# Create the study_units table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS study_units (
        id INTEGER PRIMARY KEY,
        semester TEXT,
        unit_1 TEXT,
        unit_2 TEXT,
        unit_3 TEXT,
        unit_4 TEXT
    )
''')
conn.commit()

# Function to retrieve study units from the database
def get_study_units()->List[str]:
    cursor.execute('SELECT * FROM study_units')
    return cursor.fetchall()

# Function to update the semester column in the database
def update_semester_column():
    today = datetime.date.today()
    current_year = today.year  # Change this to the desired starting year
    
    # Add the semester column to the database if it doesn't exist      
    for semester in range(1, 7):
        # Alternate between 1 and 2 for the semester number
        semester_number = 1 if semester % 2 == 1 else 2
        
        cursor.execute('''
            INSERT INTO study_units (id, semester)
            VALUES (?, ?)
        ''', (semester, f"Semester {semester_number}, {current_year}"))
        if semester % 2 == 0:
            current_year += 1
    conn.commit()

# Function to add a unit to the study matrix based on semester availability
def add_unit_to_matrix(unit_code: str, semester: int):
    study_units = get_study_units()
    for row in study_units:
        if not row[semester + 1]:  # Check if the cell is empty for the specified semester
            cursor.execute(f'''
                UPDATE study_units
                SET unit_{semester} = ?
                WHERE id = ?
            ''', (unit_code, row[0]))
            conn.commit()
            return  # Exit the function after adding the unit code

    # If no suitable cell is found, print a message
    print(f"Unit {unit_code} cannot be added for semester {semester}.")
    print("Matrix is full. Cannot add more units.")

def run():
    # Example usage:
    #update_semester_column()

    # Example usage:
    add_unit_to_matrix("PHYS1001", 1)
    add_unit_to_matrix("MATH1011", 1)
    add_unit_to_matrix("CITS2401", 1)
    add_unit_to_matrix("ENSC1001", 1)

run()

# Close the database connection when done
conn.close()
