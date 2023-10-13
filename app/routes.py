from flask import Blueprint, render_template, request, jsonify, flash, redirect
import sqlite3
from app.forms import LoginForm
import script.constants as constants
import script.database_interface as database_interface
import script.study_planner_interface as study_planner_interface 

index = Blueprint('index', __name__)
unit = Blueprint('unit', __name__)
staff_editing_bp = Blueprint('staff_editing', __name__)

@index.route('/')
def index_route():   
    data_from_database = database_interface.get_all_units()
    # Pass the fetched data to the template for rendering
    return render_template('index.html', data=data_from_database)

@unit.route('/<unit_code>')
def unit_route(unit_code):
    # Fetch the unit from the database   
    prerequisites = database_interface.get_prerequisites(unit_code)

    # Return prerequisites as JSON
    return jsonify(prerequisites=prerequisites)

@index.route('/planner')
def planner_route():
    units_from_database =  database_interface.get_all_units()
    # Define the default plan
    default_plan = {
        'year_1': {
            'semester_1': ['MATH1011', 'GENG1010', 'PHYS1001', 'CITS2401'],
            'semester_2': ['MATH1012', 'ENSC1004', 'ENSC2004', 'GENG1101'],
        },
        'year_2': {
            'semester_1': ['GENG2003', 'GENG2004', 'MECH2002', 'ENSC2003'],
            'semester_2': ['MATH3023', 'MECH2004', 'MECH3024', 'BROAD001'],
        },
        'year_3': {
            'semester_1': ['MECH3002', 'MECH4429', 'BROAD003', 'BROAD002'],
            'semester_2': ['GENG3405', 'MECH3001', 'MECH3424', 'MECH4502'],
        },
        'year_4': {
            'semester_1': ['MECH5551', 'MECH4426', 'OPTION', 'BROAD004'],
            'semester_2': ['GENG5507', 'GENG3402', 'OPTION', 'OPTION'],
        }
    }
    num_years = len(default_plan)
    return render_template('planner.html', default_plan=default_plan, all_units=units_from_database, num_years=num_years)

@index.route('/fetch-database')
def fetch_database_route():
    new_plan = study_planner_interface.fetch_database_as_plan()
    num_years = len(new_plan)
    units_from_database =  database_interface.get_all_units()
    return jsonify(new_plan=new_plan, num_years=num_years, all_units=units_from_database)

@index.route('/planner2')
def planner2_route():
    # Connect to the database
    units_from_database =  database_interface.get_all_units()

    # Define the same default plan for semester 2 start
    default_plan = {
        'year_1': {
            'semester_1': ['BLANK', 'BLANK', 'BLANK', 'BLANK'],
            'semester_2': ['CITS2401', 'MATH1011', 'ENSC1004', 'GENG1010'],
        },
        'year_2': {
            'semester_1': ['ENSC2004', 'MATH1012', 'PHYS1001', 'MECH2002'],
            'semester_2': ['GENG3405', 'MECH2004', 'GENG1101', 'MATH3023'],
        },
        'year_3': {
            'semester_1': ['GENG2003', 'MECH3002', 'ENSC2003', 'GENG2004'],
            'semester_2': ['MECH3001', 'MECH3424', 'MECH3024', 'MECH4502'],
        },
        'year_4': {
            'semester_1': ['GENG5507', 'MECH5551', 'BROAD001', 'BROAD002'],
            'semester_2': ['GENG3402', 'BROAD003', 'OPTION', 'OPTION'],
        },
        'year_5': {
            'semester_1': ['BROAD004', 'MECH4426', 'OPTION', 'MECH4429'],
            'semester_2': ['BLANK', 'BLANK', 'BLANK', 'BLANK'],
        }
    }

    return render_template('planner2.html', default_plan=default_plan, all_units=units_from_database)

@index.route('/plannerCivil')
def planner3_route():
    units_from_database =  database_interface.get_all_units()
    
    # Define the default plan
    default_plan = {
        'year_1': {
            'semester_1': ['MATH1011', 'PHYS1001', 'CITS2401', 'BROAD001'],
            'semester_2': ['MATH1012', 'GENG1010', 'ENSC2004', 'GENG1014'],
        },
        'year_2': {
            'semester_1': ['GENG2004', 'GENG2009', 'CIVL2251', 'BROAD002'],
            'semester_2': ['CIVL2008', 'GENG2010', 'GENG2012', 'BROAD003'],
        },
        'year_3': {
            'semester_1': ['CIVL3401', 'CIVL3402', 'CIVL3404', 'BROAD004'],
            'semester_2': ['CIVL3403', 'CIVL4430', 'GENG3405', 'OPTION'],
        },
        'year_4': {
            'semester_1': ['GENG4411', 'CIVL5550', 'GENG5505', 'OPTION'],
            'semester_2': ['GENG4412', 'CIVL5552', 'GENG5507', 'OPTION'],
        }
    }

    return render_template('planner.html', default_plan=default_plan, all_units=units_from_database)