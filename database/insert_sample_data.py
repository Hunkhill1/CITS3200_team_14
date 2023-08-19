import sqlite3

# Connect to the database
connection = sqlite3.connect('degree_database.db')
cursor = connection.cursor()

# Insert sample data into the Unit table
unit_data = [
    # Unit name, unit code, semester
    # Year 1 Semester 1
    ('Multivariable Calculus', 'MATH1011', 12),
    ('Introduction to Engineering', 'GENG1010', 12),
    ('Physics for Scientists & Engineers', 'PHYS1001', 12),
    ('Computer Analysis & Visualisation', 'CITS2401',12),
    # Year 1 Semester 2
    ('Mathematical Theory & Methods', 'MATH1012', 12),
    ('Engineering Materials', 'ENSC1004', 2),
    ('Engineering Mechanics', 'ENSC2004', 12),
    ('Engineering Drawings', 'GENG1101', 2),
    # Year 2 Semester 1
    ('Fluid Mechanics', 'GENG2003', 1),
    ('Solid Mechanics', 'GENG2004', 1),
    ('Engineering Materials 2', 'MECH2002', 1),
    ('Eng. Electrical Fundamentals', 'ENSC2003', 12),
    # Year 2 Semester 2
    ('Adv. Mathematics Applications', 'MATH3023', 2),
    ('Engineering Dynamics', 'MECH2004', 2),
    ('Engineering Thermodynamics', 'MECH3024', 2),
    # Year 3 Semester 1
    ('Manufacturing', 'MECH3002', 1),
    ('Applied Eng. Thermodynamics', 'MECH4429', 1),
    # Year 3 Semester 2
    ('Numerical Methods & Modelling', 'GENG3405', 2),
    ('Mechanisms & Machines', 'MECH3001', 2),
    ('Measurement & Instrumentation', 'MECH3424', 2),
    ('Analysis and Design of Machine Components', 'MECH4502', 2),
    # Year 4 Semester 1
    ('Mechanical Eng Design Project 1', 'MECH5551', 1),
    ('Dynamics, Vibration & Sound', 'MECH4426', 1),
    # Year 4 Semester 2
    ('Risk, Reliability and Safety', 'GENG5507', 12),
    ('Control Engineering', 'GENG3402', 2),

]

insert_unit_query = """
INSERT INTO Unit (name, unit_code, semester) VALUES (?, ?, ?)
"""

cursor.executant(insert_unit_query, unit_data)

# Insert sample data into the UnitRelationship table
unit_relationship_data = [
    ("MATH1011", "GENG2003", 'prerequisite'),   # MATH1011 is a prerequisite for GENG2003
    ("MATH1012", "GENG2003", 'prerequisite'),   # MATH1012 is a prerequisite for GENG2003
    ("PHYS1001", "GENG2003", 'prerequisite'),   # PHYS1001 is a prerequisite for GENG2003
    ("MATH1011", "ENSC2004", 'postrequisite'),  # Physics 101 is a postrequisite for Physics 201
    ("ENSC2004", "GENG2004     ", 'postrequisite'),  # Calculus 101 is a postrequisite for Advanced Calculus
]

insert_relationship_query = """
INSERT INTO UnitRelationship (unit_code, related_unit_code, relationship_type) VALUES (?, ?, ?)
"""

cursor.executant(insert_relationship_query, unit_relationship_data)

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Sample data inserted successfully.")
