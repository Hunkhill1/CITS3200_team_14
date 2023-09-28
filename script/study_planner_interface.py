import sqlite3
import datetime
import script.constants as constants
from script.database_interface import get_unit_semester, get_prerequisites
from typing import List, Tuple, Union,Dict

def extract_unit_codes(study_units):
    """Extract unit codes from the study_units list, filtering out None, single integers, and semester strings.

    Args:
        study_units (List[Tuple]): A list of study units where each item is a tuple containing unit information.

    Returns:
        List[str]: A list of unit codes extracted from study_units as strings.
    """
    unit_codes = []

    for row in study_units:
        for value in row[2:]:
            if isinstance(value, str) and not value.startswith('Semester '):
                unit_codes.append(str(value))

    return unit_codes

def check_prerequisite_completed(current_semester: int, prerequisite_completion_dates: Dict[str, List[int]]) -> bool:
    """ Check if prerequisites have been completed based on completion dates.

    Args:
        current_semester (int): Current semester.
        prerequisite_completion_dates (Dict[str, List[int]]): Dictionary of prerequisite completion dates.

    Returns:
        bool: True if current semester is later than all prerequisite semesters, False otherwise.
    """
    for prereq_semesters in prerequisite_completion_dates.values():
        if not all(current_semester > prereq_semester for prereq_semester in prereq_semesters):
            return False
    return True

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

def get_next_available_semester(semester_type: str, year: int, study_units: List[str])-> Union[Tuple[int, int], None]:
    """ Get the next available semester in future years.

    Args:
        semester_type (str):  The type of semester to check for.
        year (int):  The year to start checking from.
        study_units (List[str]):  The list of study units.

    Returns:
        Union[Tuple[int, int], None]:  A tuple containing the semester available, cell index. Otherwise, None.
    """    
    for semester, row in enumerate(study_units):
        if row[1].startswith(f"{semester_type}, {year}"):
            for cell_index in range(2, 6):
                if not row[cell_index]:
                    return (semester, cell_index)
    return None 

def update_study_unit(unit_id:int, cell:int, unit_code:str):
    """
    Update the study unit in the database with the given unit code.

    Args:
        conn (sqlite3.Connection): The SQLite database connection.
        unit_id (int): The ID of the study unit to update.
        semester (str): The semester in which to add the unit.
        cell (int): The cell (1 to 5) within the semester.
        unit_code (str): The unit code to add.
    """
    try:
        conn = sqlite3.connect(constants.study_planner_db_address)
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE study_units
            SET unit_{cell - 1} = ?
            WHERE id = ? ''', (unit_code, unit_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error updating study unit: {e}")

def get_prerequisite_completion_dates(study_units:List[str], prerequisites:List[str]):
    """
    Get prerequisite completion dates for each prerequisite unit.

    Args:
        study_units (List[str]): List of study unit rows.
        prerequisites (List[str]): List of prerequisite unit codes.

    Returns:
        Dict[str, List[int]]: A dictionary where keys are prerequisite unit codes
        and values are lists of row indices where the prerequisites are completed.
    """
    prerequisite_completion_dates = {}
    
    for prereq in prerequisites:
        indexes = []
        for index, row in enumerate(study_units):
            for i in range(1, 6):
                if row[i] == prereq:
                    indexes.append(index)
        
        prerequisite_completion_dates[prereq] = indexes
    
    return prerequisite_completion_dates


def find_available_semesters(study_units:List[str], semester:int,unit_type:str,start_sem:int):
    """
    Find available semesters in the study_units list.

    Args:
        study_units (List[str]): List of study unit rows.
        semester (int): The semester to search for (e.g., 1, 2).

    Returns:
        Dict[int, List]: A dictionary where keys are row indices and
        values are study unit rows for available semesters.
    """
    available_semesters = {}
    current_year = datetime.date.today().year
    if unit_type == 'completed':
        for index, row in enumerate(study_units):

            semester_str = f"Semester {semester}, {current_year}"

            if row[1] == semester_str:
                available_semesters[index] = row
    else:
        for index, row in enumerate(study_units):
            if start_sem % 2 == 1:
             if row[1] == f"Semester {semester}, {current_year}":
                available_semesters[index] = row
            else:
                if semester == 1:
                 if row[1] == f"Semester {semester}, {current_year}":
                  available_semesters[index] = row
                else:
                    if row[1] == f"Semester {semester}, {current_year-1}":
                     available_semesters[index] = row

    return available_semesters

def add_completed_unit_to_planner(unit_code: str) -> None:
    """ Add a unit to the study matrix based on prerequisites and semester availability.

    Args:
        unit_code (str):  The unit code to add to the study matrix.
    """    
    
    conn = None  # Initialize conn outside the try block
    try:    
        study_units = get_study_units()       
        semester = get_unit_semester(unit_code)
        completed_units = extract_unit_codes(study_units)
        prerequisites = get_prerequisites(unit_code)
        prerequisite_completion_dates = get_prerequisite_completion_dates(study_units, prerequisites)
        available_semesters = find_available_semesters(study_units, semester,'completed',0)
        first_year_of_degree = datetime.date.today().year

        # Check if there are available semesters
        if available_semesters:
            for index, row in available_semesters.items():
                semester_to_be_updated:int = int(row[0])
                if all(prereq in completed_units for prereq in prerequisites):
                    for i in range(1, 6):
                        if not row[i] and check_prerequisite_completed(semester_to_be_updated, prerequisite_completion_dates):
                            update_study_unit(semester_to_be_updated,i, unit_code)                      
                            return None # Exit the function after adding the unit code

       # If no suitable cell is found in the current semester, check for future semesters of the same type
        status_commited = False
        if semester == 12:
            # Check for the first empty slot in semester 1 in current year
            for year in range(first_year_of_degree, first_year_of_degree + (int)(constants.number_of_semesters/2)):
                for index, row in enumerate(study_units):
                    semester_to_be_updated:int = index+1
                    if row[1] == f"Semester 1, {year}":
                        for i in range(1, 6):
                            if not row[i] and check_prerequisite_completed(semester_to_be_updated, prerequisite_completion_dates):
                                # Check if the prerequisites have been completed
                                if all(prereq in completed_units for prereq in prerequisites):
                                    status_commited = True
                                    update_study_unit(semester_to_be_updated,i, unit_code)    
                                    return None
                                
                if status_commited == False:      
                    # Check for the first empty slot in semester 2 in current year          
                    for index, row in enumerate(study_units):
                        semester_to_be_updated:int = index+1
                        if row[1] == f"Semester 2, {year}":
                            for i in range(1, 6):
                                if not row[i] and check_prerequisite_completed(semester_to_be_updated, prerequisite_completion_dates):
                                    # Check if the prerequisites have been completed
                                    if all(prereq in completed_units for prereq in prerequisites):
                                        update_study_unit(semester_to_be_updated,i, unit_code)  
                                        return None
                                

        # If no suitable semester is found in the current year, check for future years
        if semester in [1, 2]:
            for year in range(first_year_of_degree, first_year_of_degree + (int)(constants.number_of_semesters/2)):
                next_available_semester = None
                if semester == 1:
                    next_available_semester = get_next_available_semester("Semester 1", year, study_units)
                elif semester == 2:
                    next_available_semester = get_next_available_semester("Semester 2", year, study_units)

                if next_available_semester:
                    semester_to_be_updated, cell_index = next_available_semester  # Unpack the tuple            
                    if search_strings_in_list(constants.summer_units, prerequisites) and check_summer_units_index(constants.summer_units, semester):
                        temp_list = completed_units + constants.summer_units
                        if all(prereq in temp_list for prereq in prerequisites):
                            update_study_unit(semester_to_be_updated,cell_index, unit_code)  
                            return None  # Exit the function after adding the unit code  
                    else :
                        if all(prereq in completed_units for prereq in prerequisites) and check_prerequisite_completed(semester+1, prerequisite_completion_dates):
                            update_study_unit(semester_to_be_updated,cell_index, unit_code) 
                            return None  # Exit the function after adding the unit code

        # If no suitable semester is found, print a message
        print(f"Unit {unit_code} cannot be added for semester {semester}.")
        print("Matrix is full for this semester and future semesters of the same type. Cannot add more units.")
    except sqlite3.Error as e:
        print(f"Error adding unit to planner: {e}")
    finally:
        if conn:
            conn.close()


def add_incompleted_unit_to_planner(unit_code: str,start_sem: int) -> None:
    """ Add a unit to the study matrix based on prerequisites and semester availability.

    Args:
        unit_code (str):  The unit code to add to the study matrix.
    """    
    
    conn = None  # Initialize conn outside the try block
    try:
        study_units = get_study_units()
         # Dictionary to store available semesters and their row indices
        first_year_of_degree = datetime.date.today().year
        current_year = first_year_of_degree + start_sem//2
        # Retrieve the semester of the unit
        semester = get_unit_semester(unit_code)
        conn = sqlite3.connect(constants.study_planner_db_address)
        cursor = conn.cursor()
        available_semesters = find_available_semesters(study_units,semester,'incompleted',start_sem)
        completed_units = extract_unit_codes(study_units)
        prerequisites = get_prerequisites(unit_code)
        prerequisite_completion_dates = get_prerequisite_completion_dates(study_units, prerequisites)
        
        # Check if there are available semesters
        if available_semesters:
            for index, row in available_semesters.items():
                # Check if the prerequisites have been completed
                if all(prereq in completed_units for prereq in prerequisites):
                    for i in range(1, 6): 
                        # if current semester >>> start_sem
                        semester_to_be_updated:int = int(row[0])
                        if not row[i] and check_prerequisite_completed(semester_to_be_updated, prerequisite_completion_dates):
                            # Calculate the semester and year for placing the unit code
                            update_study_unit(semester_to_be_updated,i, unit_code)
                            # cursor.execute(f'''
                            #     UPDATE study_units
                            #     SET unit_{i - 1} = ?
                            #     WHERE id = ?
                            # ''', (unit_code, semester_to_be_updated))   
                            # conn.commit()
                            return None  # Exit the function after adding the unit code

       # If no suitable cell is found in the current semester, check for future semesters of the same type
        status_commited = False
        if semester == 12:
            # Check for the first empty slot in semester 1 in current year
            if start_sem%2 == 1:
             for year in range(current_year, current_year+ (int)(constants.number_of_semesters/2)):
                for index, row in enumerate(study_units):
                    if row[1] == f"Semester 1, {year}":
                        for i in range(1, 6):
                            if not row[i] and check_prerequisite_completed(index+1, prerequisite_completion_dates):
                                # Check if the prerequisites have been completed
                                if all(prereq in completed_units for prereq in prerequisites):
                                    status_commited = True
                                    semester_to_be_updated:int = int(row[0])
                                    update_study_unit(semester_to_be_updated,i, unit_code)
                                    # cursor.execute(f'''
                                    #     UPDATE study_units
                                    #     SET unit_{i - 1} = ?
                                    #     WHERE id = ?
                                    # ''', (unit_code, row[0]))
                                    # conn.commit()
                                    return None
                                
                if status_commited == False:      
                    # Check for the first empty slot in semester 2 in current year          
                    for index, row in enumerate(study_units):
                        if row[1] == f"Semester 2, {year}":
                            for i in range(1, 6):
                                if not row[i] and check_prerequisite_completed(index+1, prerequisite_completion_dates):
                                    # Check if the prerequisites have been completed
                                    semester_to_be_updated:int = int(row[0])
                                    if all(prereq in completed_units for prereq in prerequisites):
                                        update_study_unit(semester_to_be_updated,i, unit_code)
                                #         cursor.execute(f'''
                                #             UPDATE study_units
                                #             SET unit_{i - 1} = ?
                                #  `           WHERE id = ?
                                #         ''', (unit_code, row[0]))
                                #         conn.commit()
                                        return None
            else: 
             for year in range(current_year, current_year+ (int)(constants.number_of_semesters/2)):
                for index, row in enumerate(study_units):
                    if row[1] == f"Semester 1, {year}":
                        for i in range(1, 6):
                            if not row[i] and check_prerequisite_completed(index+1, prerequisite_completion_dates):
                                # Check if the prerequisites have been completed
                                if all(prereq in completed_units for prereq in prerequisites):
                                    status_commited = True
                                    semester_to_be_updated:int = int(row[0])
                                    update_study_unit(semester_to_be_updated,i, unit_code)
                                    # cursor.execute(f'''
                                    #     UPDATE study_units
                                    #     SET unit_{i - 1} = ?
                                    #     WHERE id = ?
                                    # ''', (unit_code, row[0]))
                                    # conn.commit()
                                    return None
               # SEMESTER 2 HERE                  
                if status_commited == False:      
                    # Check for the first empty slot in semester 2 in current year          
                    for index, row in enumerate(study_units):
                        if row[1] == f"Semester 2, {year-1}":
                            for i in range(1, 6):
                                if not row[i] and check_prerequisite_completed(index+1, prerequisite_completion_dates):
                                    # Check if the prerequisites have been completed
                                    if all(prereq in completed_units for prereq in prerequisites):
                                        semester_to_be_updated:int = int(row[0])
                                        update_study_unit(semester_to_be_updated,i, unit_code)
                                        # cursor.execute(f'''
                                        #     UPDATE study_units
                                        #     SET unit_{i - 1} = ?
                                        #     WHERE id = ?
                                        # ''', (unit_code, row[0]))
                                        # conn.commit()
                                        return None

                                

        # If no suitable semester is found in the current year, check for future years
        if semester in [1, 2]:
            if start_sem%2 == 1:
             for year in range(current_year, current_year + (int)(constants.number_of_semesters/2)):
                next_available_semester = None
                if semester == 1:
                    next_available_semester = get_next_available_semester("Semester 1", year, study_units)
                elif semester == 2:
                    next_available_semester = get_next_available_semester("Semester 2", year, study_units)

                if next_available_semester:
                    index, i = next_available_semester  # Unpack the tuple                   
                    if search_strings_in_list(constants.summer_units, prerequisites) and check_summer_units_index(constants.summer_units, index):
                        temp_list = completed_units + constants.summer_units
                        if all(prereq in temp_list for prereq in prerequisites):
                            semester_to_be_updated:int = int(study_units[index][0])
                            update_study_unit(semester_to_be_updated,i, unit_code)
                            # cursor.execute(f'''
                            #     UPDATE study_units
                            #     SET unit_{i - 1} = ?
                            #     WHERE id = ?
                            # ''', (unit_code, study_units[index][0]))
                            # conn.commit()
                            return None  # Exit the function after adding the unit code
                        
                                     
                    else :
                        if all(prereq in completed_units for prereq in prerequisites) and check_prerequisite_completed(index+1, prerequisite_completion_dates):
                            semester_to_be_updated:int = int(study_units[index][0])
                            update_study_unit(semester_to_be_updated,i, unit_code)
                            # cursor.execute(f'''
                            #     UPDATE study_units
                            #     SET unit_{i - 1} = ?
                            #     WHERE id = ?
                            # ''', (unit_code, study_units[index][0]))
                            # conn.commit()
                            return None  # Exit the function after adding the unit code
            else: 
             for year in range(current_year, current_year + (int)(constants.number_of_semesters/2)):
                next_available_semester = None
                if semester == 1:
                    next_available_semester = get_next_available_semester("Semester 1", year, study_units)
                elif semester == 2:
                    next_available_semester = get_next_available_semester("Semester 2", year-1, study_units)

                if next_available_semester:
                    index, i = next_available_semester  # Unpack the tuple                   
                    if search_strings_in_list(constants.summer_units, prerequisites) and check_summer_units_index(constants.summer_units, index):
                        temp_list = completed_units + constants.summer_units
                        if all(prereq in temp_list for prereq in prerequisites):
                            semester_to_be_updated:int = int(study_units[index][0])
                            update_study_unit(semester_to_be_updated,i, unit_code)
                            # cursor.execute(f'''
                            #     UPDATE study_units
                            #     SET unit_{i - 1} = ?
                            #     WHERE id = ?
                            # ''', (unit_code, study_units[index][0]))
                            # conn.commit()
                            return None  # Exit the function after adding the unit code        
                    else :
                        if all(prereq in completed_units for prereq in prerequisites) and check_prerequisite_completed(index+1, prerequisite_completion_dates):
                            semester_to_be_updated:int = int(study_units[index][0])
                            update_study_unit(semester_to_be_updated,i, unit_code)
                            # cursor.execute(f'''
                            #     UPDATE study_units
                            #     SET unit_{i - 1} = ?
                            #     WHERE id = ?
                            # ''', (unit_code, study_units[index][0]))
                            # conn.commit()
                            return None  # Exit the function after adding the unit code   

        # If no suitable semester is found, print a message
        print(f"Unit {unit_code} cannot be added for semester {semester}.")
        print("Matrix is full for this semester and future semesters of the same type. Cannot add more units.")
    except sqlite3.Error as e:
        print(f"Error adding unit to planner: {e}")
    finally:
        if conn:
            conn.close()
            
def search_strings_in_list(list_to_search, strings_to_check):
    """ Searches for strings in a list.

    Args:
        list_to_search (_type_):  
        strings_to_check (_type_): _description_

    Returns:
        _type_: _description_
    """    
    for item in list_to_search:
        for string_to_check in strings_to_check:
            if string_to_check in item:
                return True  # Found a match, so return True
    
    return False
        
            
def check_summer_units_index(summer_units:list[str], semester:int)->bool:
    """Checks if the summer units are in the list and the current semester is greater than the completion semester of the summer unit.

    Args:
        summer_units (list[str]):  list of summer units
        semester (int):  current semester

    Returns:
        bool:  If current semester is greater than the completion semester of the summer unit, return True. Otherwise, return False.
    """   
    # find which summer is in the list
    for unit in summer_units:
        if unit == 'GENG1000' and semester > 2:
            return True
        elif unit == 'GENG2000' and semester > 4:
            return True
        elif unit == 'GENG3000' and semester > 6:
            return True
        
    return False
    
    
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
    
def calculate_current_points(completed_units: List[str]) -> int:
    """ Calculate current points based on study units.

    Args:
        completed_units (List[str]):  List of completed units

    Returns:
        int:  Current points.
    """    
    current_points = 0
    value_of_unit = 6
    current_points = len(completed_units) * value_of_unit
    return current_points   
    
def check_points(unit_code: str, current_points:int) -> bool:
    """ Check if the current points is greater than or equal to the unit points prerequisites.

    Args:
        unit_code (str):  Unit code to check for unit points prerequisites
        current_points (int):  Current points to check for unit points prerequisites

    Returns:
        bool:  True if current points is greater than or equal to the unit points prerequisites, False otherwise.
    """    
    unit_points = get_unit_points_prerequisites(unit_code)
    
    if unit_points == -1:
        return False
    else :
        if current_points >= unit_points:
            return True
        else:
            return False
    
def get_unit_points_prerequisites(unit_code:str)->int:
    """ Get unit points prerequisites for a given unit code.

    Args:
        unit_code (str):  Unit code to check for unit points prerequisites

    Returns:
        int: Unit points prerequisites for a given unit code
    """ 
    connection = None  # Initialize connection outside the try block
    try:
        # Connect to the database
        connection = sqlite3.connect(constants.degree_db_address)
        cursor = connection.cursor()

        # Query to retrieve unit points prerequisites for a given unit code
        query = """
        SELECT U.unit_points_required
        FROM Unit U
        WHERE U.code = ?
        """
        
        # Execute the query with the provided unit code
        cursor.execute(query, (unit_code,))
        
        # Fetch the result (unit_points_required)
        result = cursor.fetchone()

        if result:
            unit_points_prerequisites = int(result[0])  # Convert to integer
            return unit_points_prerequisites
        else:
            return -1  # Unit not found or no unit points prerequisites

    except sqlite3.Error as e:
        print("Database error:", e)
        return -1
    finally:
        # Close the database connection
        if connection:
            connection.close()

def run():
    # Create the database and table
    create_database()
    # Example usage:
    update_semester_column()
run()

