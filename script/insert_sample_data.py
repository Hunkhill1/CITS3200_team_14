"""
insert_sample_data.py

This script populates the degree database with sample data for units and their prerequisites.

Contents:
- Connection to the database defined in constants.py
- Insertion of sample data into the Unit and UnitRelationship tables.

Usage:
1. Run this script to insert sample data into the degree database.
2. It populates the database with units and their prerequisites.
3. This sample data is used for testing and demonstration purposes.
"""

import sqlite3
import constants as constants  # Import configuration constants

# Rest of your code...



import sqlite3
import constants as constants

# Connect to the database
connection = sqlite3.connect(constants.degree_db_address)
cursor = connection.cursor()

# Insert sample data into the Unit table with the "core" category_id
unit_data = [
    # Mechanical
    # Unit name, unit code, semester, unit_points, category_id (for "core")
    # Year 1 Semester 1
    ('MATH1011', 'Multivariable Calculus',  12, 0, 1),  # "core"
    ('GENG1010', 'Introduction to Engineering',  12, 0, 1),  # "core"
    ('PHYS1001', 'Physics for Scientists & Engineers',  12, 0, 1),  # "core"
    ('CITS2401', 'Computer Analysis & Visualisation', 12, 0, 1),  # "core"
    # Year 1 Semester 2
    ('MATH1012', 'Mathematical Theory & Methods',  12, 0, 1),  # "core"
    ('ENSC1004', 'Engineering Materials',  2, 0, 1),  # "core"
    ('ENSC2004', 'Engineering Mechanics',  12, 0, 1),  # "core"
    ('GENG1101', 'Engineering Drawings',  2, 0, 1),  # "core"
    # Year 2 Semester 1
    ('GENG2003', 'Fluid Mechanics',  1, 0, 1),  # "core"
    ('GENG2004', 'Solid Mechanics',  1, 0, 1),  # "core"
    ('MECH2002', 'Engineering Materials 2',  1, 0, 1),  # "core"
    ('ENSC2003', 'Eng. Electrical Fundamentals',  12, 0, 1),  # "core"
    # Year 2 Semester 2
    ('MATH3023', 'Adv. Mathematics Applications',  2, 0, 1),  # "core"
    ('MECH2004', 'Engineering Dynamics',  2, 0, 1),  # "core"
    ('MECH3024', 'Engineering Thermodynamics',  2, 0, 1),  # "core"
    # Year 3 Semester 1
    ('MECH3002', 'Manufacturing', 1, 0, 1),  # "core"
    ('MECH4429', 'Applied Eng. Thermodynamics',  1, 0, 1),  # "core"
    # Year 3 Semester 2
    ('GENG3405', 'Numerical Methods & Modelling',  2, 0, 1),  # "core"
    ('MECH3001', 'Mechanisms & Machines',  2, 0, 1),  # "core"
    ('MECH3424', 'Measurement & Instrumentation',  2, 0, 1),  # "core"
    ('MECH4502', 'Analysis and Design of Machine Components',  2, 0, 1),  # "core"
    # Year 4 Semester 1
    ('MECH5551', 'Mechanical Eng Design Project 1',  1, 0, 1),  # "core"
    ('MECH4426', 'Dynamics, Vibration & Sound',  1, 0, 1),  # "core"
    # Year 4 Semester 2
    ('GENG5507', 'Risk, Reliability and Safety',  12, 120, 1),  # "core" with unit_points = 120
    ('GENG3402', 'Control Engineering',  2, 0, 1),  # "core"
    
    #Group A
    ('GENG4411', 'Engineering Research Project Part 1',  12, 144, 4),  # "Group A" with unit_points = 144
    ('GENG4412', 'Engineering Research Project Part 2',  12, 0, 4),  # "Group A"
    ('MECH5552', 'Mechanical Engineering Design Project',  2, 0, 4),  # "Group A"
    
    # Group B
    ('GENG5504', 'Petroleum Engineering',  2, 0, 5),  # "Group B"
    ('GENG5505', 'Project Management & Engineering Practice',  12, 120, 5),  # "Group B" with unit_points = 120
    ('CHPR3405', 'Particle Technology',  1, 0, 5),  # "Group B"
    ('MECH5504', 'Design and Failure Analysis of Materials',  2, 120, 5),  # "Group B" with unit_points = 120
    ('GENG5514', 'Finite Element Method',  1, 120, 5),  # "Group B" with unit_points = 120
    ('MECH4428', 'Degradation of Materials',  1, 96, 5),  # "Group B" with unit_points = 96
    
    # BROADENING
    ('BROAD001', 'BROADENING',  2, 0, 2),
    ('BROAD002', 'BROADENING',  1, 0, 2),
    ('BROAD003', 'BROADENING',  1, 0, 2),
    ('BROAD004', 'BROADENING',  1, 0, 2),

    # Civil
    ('GENG1014', 'Earth Systems Engineering',  2, 0, 1),  # "core"
    ('GENG2012', 'Data Collection and Analysis',  2, 0, 1),  # "core"
    ('CIVL2551', 'Civil Engineering Practice',  1, 0, 1),  # "core"
    ('CIVL2008', 'Structual Analysis',  2, 0, 1),  # "core"
    ('GENG2010', 'Principles of Hydraulics',  2, 0, 1),  # "core"
    ('GENG2009', 'Principles of Geomechanics',  1, 0, 1),  # "core"
    ('CIVL3403', 'Structual Concrete Design',  2, 0, 1),  # "core"
    ('CIVL4430', 'Transportation and Pavement Engineering',  2, 96, 1),  # "core"
    ('CIVL3401', 'Applied Geomechanics',  1, 0, 1),  # "core"
    ('CIVL5552', 'Civil Structual Design Project',  2, 120, 4),  # "Option Group A"
    ('CIVL3404', 'Structual Steel Design',  1, 0, 1),  # "core"
    ('CIVL5550', 'Civil Infrastrucuture Design Project',  12, 120, 4),  # "Option Group A"
    ('CIVL3402', 'Hydraulics for Civil Engineers',  1, 0, 1),  # "core"

]

# Define an SQL query to insert data into the Unit table (with category_id)
insert_unit_query = """
INSERT INTO Unit (code, name, semester, unit_points_required, category_id) VALUES (?, ?, ?, ?, ?)
"""

# Execute the insert_unit_query using executemany() to insert multiple rows of data
cursor.executemany(insert_unit_query, unit_data)

# Insert sample data into the UnitRelationship table
unit_relationship_data = [
    # Unit code, pre_requisite
    # Year 1 Semester 2
    ("ENSC2004", "MATH1011"),
    # Year 2 Semester 1
    ("GENG2003", "MATH1011"),
    ("GENG2003", "MATH1012"),
    ("GENG2003", "PHYS1001"),
    ("GENG2004", "MATH1011"),
    ("GENG2004", "MATH1012"),
    ("GENG2004", "ENSC2004"),
    ("MECH2002", "ENSC1004"),
    ("ENSC2003", "MATH1011"),
    ("ENSC2003", "MATH1012"),

    # Year 2 Semester 2
    ("MATH3023", "MATH1011"),
    ("MATH3023", "MATH1012"),
    ("MECH2004", "ENSC2004"),
    ("MECH2004", "MATH1011"),
    ("MECH2004", "MATH1012"),
    ("MECH3024", "CITS2401"),
    ("MECH3024", "ENSC2004"),

    # Year 3 Semester 1
    ("MECH3002", "GENG2000"),
    ("MECH3002", "MECH2002"),
    ("MECH4429", "MECH3024"),

    # Year 3 Semester 2
    ("GENG3405", "MATH1012"),
    ("GENG3405", "CITS2401"),
    ("MECH3001", "CITS2401"),
    ("MECH3001", "MECH2004"),
    ("MECH3424", "CITS2401"),
    ("MECH3424", "ENSC2004"),
    ("MECH3424", "MATH1012"),
    ("MECH3424", "GENG2000"),
    ("MECH4502", "CITS2401"),
    ("MECH4502", "GENG2004"),
    ("MECH4502", "MECH2004"),
    ("MECH4502", "MECH3002"),
    ("MECH4502", "GENG3000"),

    # Year 4 Semester 1
    ("MECH5551", "MECH4502"),
    ("MECH5551", "GENG3000"),
    ("MECH4426", "MECH2004"),

    # Year 4 Semester 2
    ("GENG3402", "MATH1011"),
    ("GENG3402", "MATH1012"),
    
    # Group A
    #("GENG4411", "GENG3000"),
    ("GENG4412", "GENG4411"),
    ("MECH5552", "MECH5551"),
    
    # Group B
    ("GENG5504", "MATH1011"),
    ("GENG5504", "MATH1012"),
    ("CHPR3405", "GENG2003"),
    ("MECH5504", "MECH2002"),
    ("MECH5504", "GENG2004"),
    ("GENG5514", "GENG2003"),
    ("GENG5514", "GENG2004"),
    ("GENG5514", "GENG3405"),
    ("MECH4428", "MECH2002"),
    
    # Civil 
    ("CIVL2008", "MATH1011"),
    ("CIVL2008", "ENSC2004"),
    
    ("GENG2009", "MATH1011"),
    ("GENG2009", "MATH1012"),
    ("GENG2009", "PHYS1001"),
    
    ("GENG2010", "MATH1011"),
    ("GENG2010", "MATH1012"),
    
    ("GENG2012", "MATH1012"),
    ("GENG2012", "CITS2401"),
    
    ("CIVL3401", "GENG2009"),
    
    ("CIVL3402", "GENG2010"),
    
    ("CIVL3403", "GENG2004"),
    ("CIVL3403", "GENG1000"),
    
    ("CIVL3404", "GENG2004"),
    
    ("CIVL4430", "MATH1011"),
    ("CIVL4430", "CITS2401"),
    
    #("CIVL5550", "GENG3000"),
    ("CIVL5550", "CIVL4430"),
    
    #("CIVL5552", "GENG3000"),
    ("CIVL5552", "CIVL3404"),
]

# Define an SQL query to insert data into the UnitRelationship table
insert_relationship_query = """
INSERT INTO UnitRelationship (unit_code, pre_requisite) VALUES (?, ?)
"""

# Execute the insert_relationship_query using executemany() to insert multiple rows of data
cursor.executemany(insert_relationship_query, unit_relationship_data)

# Commit the changes and close the connection
connection.commit()
connection.close()

# Print a message indicating that the sample data has been inserted successfully.
print("Sample data inserted successfully.")
