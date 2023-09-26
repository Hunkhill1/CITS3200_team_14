from flask import Blueprint, render_template, request, jsonify, flash, redirect
import sqlite3
from app.forms import LoginForm
import script.constants as constants
import script.database_interface as database_interface

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
            'semester_2': ['MATH3023', 'MECH2004', 'MECH3024', 'Select unit'],
        },
        'year_3': {
            'semester_1': ['MECH3002', 'MECH4429', 'Select unit', 'Select unit'],
            'semester_2': ['GENG3405', 'MECH3001', 'MECH3424', 'MECH4502'],
        },
        'year_4': {
            'semester_1': ['MECH5551', 'MECH4426', 'Select unit', 'Select unit'],
            'semester_2': ['GENG5507', 'GENG3402', 'Select unit', 'Select unit'],
        }
    }

    return render_template('planner.html', default_plan=default_plan, all_units=units_from_database)








