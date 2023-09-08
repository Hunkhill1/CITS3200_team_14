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
    available_semesters = {}  # Dictionary to store available semesters and their row indices
    
    # Populate available_semesters with rows that match the given semester
    for index, row in enumerate(study_units):
        if row[1] == f"Semester {semester}, {datetime.date.today().year}":
            available_semesters[index] = row

    # Check if there are available semesters
    if available_semesters:
        for index, row in available_semesters.items():
            for i in range(2, 6):
                if not row[i]:
                    cursor.execute(f'''
                        UPDATE study_units
                        SET unit_{i - 1} = ?
                        WHERE id = ?
                    ''', (unit_code, row[0]))
                    conn.commit()
                    return  # Exit the function after adding the unit code
    
    # If no suitable cell is found in the current semester, check for future semesters of the same type
    for index, row in enumerate(study_units):
        if row[1].startswith(f"Semester {semester}"):
            for i in range(2, 6):
                if not row[i]:
                    cursor.execute(f'''
                        UPDATE study_units
                        SET unit_{i - 1} = ?
                        WHERE id = ?
                    ''', (unit_code, row[0]))
                    conn.commit()
                    return  # Exit the function after adding the unit code
    
    # If no suitable semester is found, print a message
    print(f"Unit {unit_code} cannot be added for semester {semester}.")
    print("Matrix is full for this semester and future semesters of the same type. Cannot add more units.")



    
# Function to drop the study_units table
def drop_table():
    cursor.execute('DROP TABLE IF EXISTS study_units')
    conn.commit()
    print("Table 'study_units' has been dropped.")
    
def add_sample_data():
    add_unit_to_matrix("PHYS1001", 1)
    add_unit_to_matrix("MATH1011", 1)
    add_unit_to_matrix("CITS2401", 1)
    add_unit_to_matrix("ENSC1001", 1)
    
    add_unit_to_matrix("TEST1", 1)
    add_unit_to_matrix("TEST2", 1)
    add_unit_to_matrix("TEST3", 1)
    add_unit_to_matrix("TEST4", 1)
    
    add_unit_to_matrix("TEST5", 1)
    add_unit_to_matrix("TEST6", 1)
    add_unit_to_matrix("TEST7", 1)
    add_unit_to_matrix("TEST8", 1)
    
    add_unit_to_matrix("TEST9", 1)
    
    
# Function to clear all data from the study_units table
def clear_table():
    cursor.execute('DELETE FROM study_units')
    conn.commit()
    print("All data has been cleared from the 'study_units' table.")

def run():
    # Example usage:
    update_semester_column()

    add_sample_data()
run()

# Close the database connection when done
conn.close()
