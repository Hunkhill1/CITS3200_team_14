import pandas as pd
import tkinter as tk
from tkinter import ttk

# Define a matrix to hold study units (6 rows x 4 columns)
study_matrix = [[""] * 5 for _ in range(6)]

# Function to add a study unit to the matrix
def add_study_unit(row:int, semester:str, unit_1:str, unit_2:str, unit_3:str, unit_4:str)->None:
    """ A semesters worth of study units

    Args:
        row (int):  Row number in the study matrix
        semester (str):  Semester 1 or 2, and the year
        unit_1 (str):  Unit code for the first unit
        unit_2 (str):  Unit code for the second unit
        unit_3 (str):  Unit code for the third unit
        unit_4 (str):  Unit code for the fourth unit
    """    
    study_matrix[row] = [semester, unit_1, unit_2, unit_3, unit_4]

# Function to display the study matrix in a GUI window
def display_study_matrix_gui()->None:
    """ Display the study matrix in a GUI window
    """    
    if not any(study_matrix):
        print("No study units added yet.")
        return

    # Create a DataFrame from the study matrix
    df = pd.DataFrame(study_matrix, columns=["Semester", "Unit 1", "Unit 2", "Unit 3", "Unit 4"])
    
    # Create a tkinter window
    window = tk.Tk()
    window.title("Study Matrix")

    # Create a treeview widget (table) to display the data
    tree = ttk.Treeview(window, columns=["Semester", "Unit 1", "Unit 2", "Unit 3", "Unit 4"], show="headings")
    tree.heading("Semester", text="Semester")
    tree.heading("Unit 1", text="Unit 1")
    tree.heading("Unit 2", text="Unit 2")
    tree.heading("Unit 3", text="Unit 3")
    tree.heading("Unit 4", text="Unit 4")
    
    # Insert the data into the treeview
    for index, row in df.iterrows():
        tree.insert("", "end", values=tuple(row))

    # Pack the treeview
    tree.pack()

    # Start the tkinter main loop
    window.mainloop()
    
def add_unit_to_matrix(unit_code:str)->None:
    """ Add a unit to the study matrix

    Args:
        unit_code (str): Unit code to add to the matrix

    """    
    for row in range(len(study_matrix)):
        for col in range(len(study_matrix[row])):
            if not study_matrix[row][col]:
                study_matrix[row][col] = unit_code
                return  # Exit the function after adding the unit code

    # If all cells are filled, print a message
    print("Matrix is full. Cannot add more units.")
    
    
def update_semester_column()->None:
    """ Update the semester column in the study matrix
    """    
    for row in range(len(study_matrix)):
        semester = 1 if row % 2 == 0 else 2
        study_matrix[row][0] = f"Semester {semester}, 2023"  # Change the year as needed

def run():
    # Example usage:
    update_semester_column()

    # Example usage:
    add_unit_to_matrix("COMP1010")

    # Display the study matrix in a GUI window
    display_study_matrix_gui()

run()



