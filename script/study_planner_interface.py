import sqlite3
import datetime
import script.constants as constants
from script.database_interface import get_unit_semester, get_prerequisites
from typing import List, Tuple, Union

from script.constants import completed_units 

def extract_unit_codes(study_units):
    """Extract unit codes from the study_units list, filtering out None, single integers, and semester strings.

    Args:
        study_units (List[Tuple]): A list of study units where each item is a tuple containing unit information.

    Returns:
        set: A set of unit codes extracted from study_units.
    """
    unit_codes = set()

    for row in study_units:
        for value in row[2:]:
            if isinstance(value, str) and not value.startswith('Semester '):
                unit_codes.add(value)

    return unit_codes


# Function to create the database and the study_units table
def create_database()->None:
    """Create the SQLite database and the study_units table if they don't exist."""
    conn = sqlite3.connect(constants.study_planner_db_address)
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
    conn.close()
# Function to retrieve study units from the database
def get_study_units() -> List[str]:
    """ Retrieve study units from the database.

    Returns:
        List[str]:  A list of study units.
    """    
    conn = sqlite3.connect(constants.study_planner_db_address)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM study_units')
        study_units = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error executing SQL query: {e}")
        study_units = []
    finally:
        conn.close()
    return study_units
   

# Function to update the semester column in the database
def update_semester_column() -> None:
    """ Update the semester column in the database.
    """
    clear_table()    
    conn = None  # Initialize conn outside the try block
    try:
        today = datetime.date.today()
        current_year = today.year  # Change this to the desired starting year

        conn = sqlite3.connect(constants.study_planner_db_address)
        cursor = conn.cursor()

        # Add the semester column to the database if it doesn't exist      
        for semester in range(1, constants.number_of_semesters+1):
            # Alternate between 1 and 2 for the semester number
            semester_number = 1 if semester % 2 == 1 else 2

            cursor.execute('''
                INSERT INTO study_units (id, semester)
                VALUES (?, ?)
            ''', (semester, f"Semester {semester_number}, {current_year}"))
            if semester % 2 == 0:
                current_year += 1
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating semester column: {e}")
    finally:
        if conn:
            conn.close()

# Function to get the next available semester in future years
def get_next_available_semester(semester_type: str, year: int, study_units: List[str])-> Union[Tuple[int, int, str], None]:
    """ Get the next available semester in future years.

    Args:
        semester_type (str):  The type of semester to check for.
        year (int):  The year to start checking from.
        study_units (List[str]):  The list of study units.

    Returns:
        Union[Tuple[int, int, str], None]:  
    """    
    for index, row in enumerate(study_units):
        if row[1].startswith(f"{semester_type}, {year}"):
            for i in range(2, 6):
                if not row[i]:
                    return (index, i, f"{semester_type}, {year}")
    return None 

# Function to add a unit to the study matrix based on prerequisites and semester availability
def add_unit_to_planner(unit_code: str) -> None:

    """ Add a unit to the study matrix based on prerequisites and semester availability.

    Args:
        unit_code (str): Unit Code

    Returns:
        None
    """
    conn = None  # Initialize conn outside the try block
    try:
        study_units = get_study_units()
       
        # completed_units = get_completed_units(study_units)  # Function to retrieve completed units from the study matrix
        available_semesters = {}  # Dictionary to store available semesters and their row indices

        # Retrieve the semester of the unit
        semester = get_unit_semester(unit_code)

        conn = sqlite3.connect(constants.study_planner_db_address)
        cursor = conn.cursor()
        
        completed_units = extract_unit_codes(study_units)
        
        prerequisites = get_prerequisites(unit_code) 

        # Populate available_semesters with rows that match the given semester
        for index, row in enumerate(study_units):
            if row[1] == f"Semester {semester}, {datetime.date.today().year}":
                available_semesters[index] = row

        # Check if there are available semesters
        if available_semesters:
            for index, row in available_semesters.items():
                # Check if the prerequisites have been completed
                if all(prereq in completed_units for prereq in prerequisites):
                    for i in range(2, 6):
                        if not row[i]:
                            cursor.execute(f'''
                                UPDATE study_units
                                SET unit_{i - 1} = ?
                                WHERE id = ?
                            ''', (unit_code, row[0]))
                            conn.commit()
                            return None  # Exit the function after adding the unit code

        # If no suitable cell is found in the current semester, check for future semesters of the same type
        for index, row in enumerate(study_units):
            if row[1].startswith(f"Semester {semester}"):
                for i in range(2, 6):
                    if not row[i]:
                        # Check if the prerequisites have been completed
                        if all(prereq in completed_units for prereq in prerequisites):
                            cursor.execute(f'''
                                UPDATE study_units
                                SET unit_{i - 1} = ?
                                WHERE id = ?
                            ''', (unit_code, row[0]))
                            conn.commit()
                            return None  # Exit the function after adding the unit code

        # If the unit is available in both semesters (semester 12)
        if semester == 12:
            # Check for the first empty slot in semester 1
            for index, row in enumerate(study_units):
                if row[1] == f"Semester 1, {datetime.date.today().year}":
                    for i in range(2, 6):
                        if not row[i]:
                            # Check if the prerequisites have been completed
                            if all(prereq in completed_units for prereq in prerequisites):
                                cursor.execute(f'''
                                    UPDATE study_units
                                    SET unit_{i - 1} = ?
                                    WHERE id = ?
                                ''', (unit_code, row[0]))
                                conn.commit()
                                return None  # Exit the function after adding the unit code

            # If no suitable slot is found in semester 1, check for semester 2
            for index, row in enumerate(study_units):
                if row[1] == f"Semester 2, {datetime.date.today().year}":
                    for i in range(2, 6):
                        if not row[i]:
                            # Check if the prerequisites have been completed
                            prerequisites = get_prerequisites(unit_code)
                            if all(prereq in completed_units for prereq in prerequisites):
                                cursor.execute(f'''
                                    UPDATE study_units
                                    SET unit_{i - 1} = ?
                                    WHERE id = ?
                                ''', (unit_code, row[0]))
                                conn.commit()
                                return None  # Exit the function after adding the unit code

        # If no suitable semester is found in the current year, check for future years
        if semester in [1, 2]:
            current_year = datetime.date.today().year
            while True:
                next_year = current_year + 1
                next_available_semester = None
                if semester == 1:
                    next_available_semester = get_next_available_semester("Semester 1", next_year, study_units)
                elif semester == 2:
                    next_available_semester = get_next_available_semester("Semester 2", next_year, study_units)

                if next_available_semester:
                    index, i, semester_type = next_available_semester
                    # Check if the prerequisites have been completed
                    prerequisites = get_prerequisites(unit_code)
                    if all(prereq in completed_units for prereq in prerequisites):
                        cursor.execute(f'''
                            UPDATE study_units
                            SET unit_{i - 1} = ?
                            WHERE id = ?
                        ''', (unit_code, study_units[index][0]))
                        conn.commit()
                        return None  # Exit the function after adding the unit code

                current_year = next_year

        # If no suitable semester is found, print a message
        print(f"Unit {unit_code} cannot be added for semester {semester}.")
        print("Matrix is full for this semester and future semesters of the same type. Cannot add more units.")
    except sqlite3.Error as e:
        print(f"Error adding unit to planner: {e}")
    finally:
        if conn:
            conn.close()


# Function to drop the study_units table
def drop_table()->None:
    """ Drop the study_units table.
    """
    conn = sqlite3.connect(constants.study_planner_db_address)
    cursor = conn.cursor()    
    cursor.execute('DROP TABLE IF EXISTS study_units')
    conn.commit()
    print("Table 'study_units' has been dropped.")
    conn.close()
    
   
# Function to clear all data from the study_units table
def clear_table()->None:
    """Clear all data from the study_units table.
    """
    conn = sqlite3.connect(constants.study_planner_db_address)
    cursor = conn.cursor()   
    cursor.execute('DELETE FROM study_units')
    conn.commit()
    print("All data has been cleared from the 'study_units' table.")
    # Close the database connection when done
    conn.close()

def run():
    # Create the database and table
    create_database()
    # Example usage:
    update_semester_column()
run()

