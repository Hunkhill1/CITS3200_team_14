import tkinter as tk
from tkinter import ttk
import sqlite3

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

# Function to add a study unit to the database
def add_study_unit(semester, unit_1, unit_2, unit_3, unit_4):
    cursor.execute('''
        INSERT INTO study_units (semester, unit_1, unit_2, unit_3, unit_4)
        VALUES (?, ?, ?, ?, ?)
    ''', (semester, unit_1, unit_2, unit_3, unit_4))
    conn.commit()

# Function to retrieve study units from the database
def get_study_units():
    cursor.execute('SELECT * FROM study_units')
    return cursor.fetchall()

# Function to display the study matrix in a GUI window
def display_study_matrix_gui():
    study_units = get_study_units()

    if not study_units:
        print("No study units added yet.")
        return

    # Create a tkinter window
    window = tk.Tk()
    window.title("Study Matrix")

    # Create a treeview widget (table) to display the data
    tree = ttk.Treeview(
        window,
        columns=["Semester", "Unit 1", "Unit 2", "Unit 3", "Unit 4"],
        show="headings",
    )
    tree.heading("Semester", text="Semester")
    tree.heading("Unit 1", text="Unit 1")
    tree.heading("Unit 2", text="Unit 2")
    tree.heading("Unit 3", text="Unit 3")
    tree.heading("Unit 4", text="Unit 4")

    # Insert the data into the treeview
    for row in study_units:
        tree.insert("", "end", values=row[1:])

    # Pack the treeview
    tree.pack()

    # Start the tkinter main loop
    window.mainloop()

# Function to update the semester column in the database
def update_semester_column():
    current_year = 2023  # Change this to the desired starting year
    for semester in range(1, 7):
        cursor.execute('''
            UPDATE study_units
            SET semester = ?
            WHERE id = ?
        ''', (f"Semester {semester}, {current_year}", semester))
        if semester % 2 == 0:
            current_year += 1
    conn.commit()

def run():
    # Example usage:
    update_semester_column()

    # Example usage:
    add_study_unit("Semester 1, 2023", "PHYS1001", "MATH1011", "CITS2401", "ENSC1001")
    add_study_unit("Semester 1, 2023", "Test1", "Test2", "Test3", "Test4")
    add_study_unit("Semester 2, 2023", "Test5", "Test6", "Test7", "Test8")

    # Display the study matrix in a GUI window
    display_study_matrix_gui()

run()

# Close the database connection when done
conn.close()
