import sqlite3

# Connect to the database
connection = sqlite3.connect('database/degree_database.db')
cursor = connection.cursor()

# Insert sample data into the Unit table
unit_data = [
    # Unit name, unit code, semester
    # Year 1 Semester 1
    ('MATH1011','Multivariable Calculus',  12),
    ('GENG1010','Introduction to Engineering',  12),
    ('PHYS1001','Physics for Scientists & Engineers',  12),
    ('CITS2401','Computer Analysis & Visualisation', 12),
    # Year 1 Semester 2
    ('MATH1012','Mathematical Theory & Methods',  12),
    ('ENSC1004','Engineering Materials',  2),
    ('ENSC2004','Engineering Mechanics',  12),
    ('GENG1101','Engineering Drawings',  2),
    # Year 2 Semester 1
    ('GENG2003','Fluid Mechanics',  1),
    ('GENG2004','Solid Mechanics',  1),
    ('MECH2002','Engineering Materials 2',  1),
    ('ENSC2003','Eng. Electrical Fundamentals',  12),
    # Year 2 Semester 2
    ('MATH3023','Adv. Mathematics Applications',  2),
    ('MECH2004','Engineering Dynamics',  2),
    ('MECH3024','Engineering Thermodynamics',  2),
    # Year 3 Semester 1
    ('MECH3002', 'Manufacturing', 1),
    ('MECH4429','Applied Eng. Thermodynamics',  1),
    # Year 3 Semester 2
    ('GENG3405','Numerical Methods & Modelling',  2),
    ('MECH3001','Mechanisms & Machines',  2),
    ('MECH3424','Measurement & Instrumentation',  2),
    ('MECH4502','Analysis and Design of Machine Components',  2),
    # Year 4 Semester 1
    ('MECH5551','Mechanical Eng Design Project 1',  1),
    ('MECH4426','Dynamics, Vibration & Sound',  1),
    # Year 4 Semester 2
    ('GENG5507','Risk, Reliability and Safety',  12),
    ('GENG3402','Control Engineering',  2),

]

insert_unit_query = """
INSERT INTO Unit (code,name,semester) VALUES (?, ?, ?)
"""

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
]

insert_relationship_query = """
INSERT INTO UnitRelationship (unit_code, pre_requisite) VALUES (?, ?)
"""

cursor.executemany(insert_relationship_query, unit_relationship_data)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Sample data inserted successfully.")
