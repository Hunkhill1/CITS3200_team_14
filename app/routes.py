from flask import Blueprint, render_template, request, jsonify
import sqlite3

index = Blueprint('index', __name__)

@index.route('/')
def index_route():
    # Connect to the database
    conn = sqlite3.connect('database/degree_database.db')
    cursor = conn.cursor()

    # Fetch data from the Unit table
    cursor.execute("SELECT code, name, semester, status FROM Unit")
    data_from_database = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Pass the fetched data to the template for rendering
    return render_template('index.html', data=data_from_database)

unit = Blueprint('unit', __name__)

@unit.route('/unit/<unit_code>')
def unit_route(unit_code):
    # Connect to the database
    conn = sqlite3.connect('database/degree_database.db')
    cursor = conn.cursor()

    # Fetch prerequisites for the specified unit
    cursor.execute("SELECT pre_requisite FROM UnitRelationship WHERE unit_code=?", (unit_code,))
    prerequisites = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    conn.close()

    # Return prerequisites as JSON
    return jsonify(prerequisites=prerequisites)
