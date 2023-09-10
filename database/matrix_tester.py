import unittest
import sqlite3
import os

# Import your database functions
from matrix import (
    update_semester_column,
    add_unit_to_matrix,
    add_sample_data,
    clear_table,
    get_study_units,
    drop_table,
)

# Create a temporary test database (in-memory) for testing
db_path = ":memory:"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Replace 'your_module_name' with the actual module name where your functions are defined

class TestDatabaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the study_units table in the test database
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

    @classmethod
    def tearDownClass(cls):
        # Drop the study_units table in the test database
        cursor.execute('DROP TABLE IF EXISTS study_units')
        conn.commit()
        conn.close()

    def setUp(self):
        # Clear the study_units table before each test
        clear_table()

    def test_update_semester_column(self):
        # Test if the semester column is updated correctly
        update_semester_column()
        study_units = get_study_units()
        self.assertTrue(study_units)  # Check if there are study units in the database

    def test_add_unit_to_matrix(self):
        # Test adding a unit to the matrix
        add_sample_data()  # Add some sample data
        study_units = get_study_units()
        # Check if the unit has been added to the matrix
        self.assertTrue(any("TEST1" in row for row in study_units))

    def test_clear_table(self):
        # Test clearing all data from the study_units table
        add_sample_data()  # Add some sample data
        clear_table()
        study_units = get_study_units()
        self.assertFalse(study_units)  # Check if the table is empty

if __name__ == '__main__':
    unittest.main()
