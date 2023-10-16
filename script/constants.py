"""
constants.py

This module stores various constants and configuration parameters for the study planner application.

Contents:
- degree_db_address: Path to the degree database.
- study_planner_db_address: Path to the study planner database.
- static_folder_address: Path to the static folder for web assets.
- template_folder_address: Path to the template folder for web templates.
- number_of_semesters: Total number of semesters in a degree program.
- summer_units: List of unit codes that are offered during summer semesters.
- points_per_unit: Number of credit points per unit.
- fail_str: String indicating a failing grade.
- broading_str: String indicating a broadening unit.
- option_str: String indicating an option unit.
- select_unit_str: String for selecting a unit.

Usage:
- Import this module to access constants and configuration parameters throughout the application.
"""
# Constants and configuration parameters

degree_db_address = 'database/degree_database.db'
study_planner_db_address = 'database/study_planner.db'
static_folder_address = 'app/static'
template_folder_address = 'app/templates'
number_of_semesters = 8
summer_units = ['GENG1000', 'GENG2000', 'GENG3000']
points_per_unit = 6
fail_str = 'FAIL'
broading_str = 'BROADENING'
option_str = 'OPTION'
select_unit_str = 'Select unit'



degree_db_address = 'database/degree_database.db'
study_planner_db_address = 'database/study_planner.db'
static_folder_address = 'app/static'
template_folder_address = 'app/templates'
number_of_semesters = 8
summer_units: list[str] = ['GENG1000', 'GENG2000', 'GENG3000']
points_per_unit = 6
fail_str = 'FAIL'
broading_str = 'BROADENING'
option_str = 'OPTION'
select_unit_str = 'Select unit'

