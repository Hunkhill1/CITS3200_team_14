from flask import Flask, render_template, flash, redirect, jsonify, request
from flask_login import LoginManager, current_user
from config import Config
from app.routes import index, unit
from app.forms import LoginForm
from app.models import User
from app import db
from script.algo import algorithm
import script.constants as constants


app = Flask(__name__, template_folder=constants.template_folder_address, static_folder=constants.static_folder_address)
app.config.from_object(Config)

login = LoginManager(app) # type: ignore
login.login_view = 'login'

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(index)
app.register_blueprint(unit, url_prefix='/unit')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/planner', methods=['GET'])
def planner():
    return render_template('planner.html', title='Unit Planner')

@app.route('/process_json', methods=['POST'])
def process_json_data():
    try:
        json_data = request.get_json()
        
        # Process the JSON data as needed
        print("Received JSON data:")
        print(json_data)

        # Initialize lists to store complete and incomplete units
        complete_units = []
        incomplete_units = []

        # Loop through the JSON data and categorize units based on status
        for unit_code, status in json_data.items():
            if status == 'complete':
                complete_units.append(unit_code)
            elif status == 'incomplete':
                incomplete_units.append(unit_code)

        # Convert the lists of complete and incomplete units to strings
        

        print(f'Complete Units: {complete_units}')
        print(f'Incomplete Units: {incomplete_units}')

        # Return a response if needed
        response_data = {'message': 'Data received successfully'}
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)


