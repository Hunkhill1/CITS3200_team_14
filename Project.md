# CITS3200 Project

## Project Details

- Group = 14
- Members :
  - Ethan Wilson (23096565)
  - Sahil Narula (23313963)
  - Iash Bashir (23059859)
  - Thai Hoang Long Nguyen (23147438)
  - Joshua Patton (23103979)
- Client = Diane Hesterman



## Project Statement

The primary objective of this project is to develop a highly efficient web application that offers engineering students a semi-automated course study planner. This course planner will provide a straightforward method for structuring a student's academic journey, accompanied by precise instructions on the following: 

 - Course regulations 

- Essential course units  

- Unit prerequisites 

The application will work with the student's personal preferences to design a course plan adhering to all applicable rules. This plan will visually illustrate which units should be done each year and each semester of the individual degree. As a result, the student will receive a clear and optimal course plan that ensures degree completion within the designated timeframe.  

## Skills/Resources

### Web Developement

Our decision to utilize HTML, CSS, and vanilla JavaScript for the web application's interface was both strategic and practical.The team  developed proficiency in core web technologies, as the team has all completed the Agile Web Developement Unit (CITS3403). This foundation meant we could immediately dive into development without the need for a learning curve associated with more complex frameworks like Angular or React. Moreover, considering the project's tight timeline, it was imperative to leverage our existing skills rather than invest time upskilling on new languages or frameworks. This approach not only optimized our workflow but also ensured we delivered a high-quality product within the stipulated timeframe.  

### Database Management

For database management, our team unanimously chose SQLite, a decision driven by multiple factors. Foremost, our collective experience with SQLite in both the Relational Database and Agile Web Development units rendered us well-acquainted with its functionalities and advantages. SQLite's lightweight nature, ease of use, and built-in compatibility with Python presented a seamless choice for our requirements. Furthermore, its effortless integration with Flask—a framework our team is proficient in—further solidified our decision. By leveraging SQLite, we could capitalize on our pre-existing knowledge and ensure efficient, reliable database management for our web application.


## Front End

### Static Webpages

- Homepage
- Login
- Planner
- Staff Editing Page

### Flask

- Initiating Flask

```
init.py
```

This script configures and initializes a Flask web application along with several essential extensions. It creates an instance of the Flask app, configures it using settings from the Config class, and sets up a SQLAlchemy database connection and migration engine using Flask-SQLAlchemy and Flask-Migrate. Additionally, it integrates user authentication functionality using Flask-Login and sets the default login view to 'login'. Finally, it imports routes and models from the 'app' package, making them available for use within the Flask application. This script is a crucial part of setting up a Flask web application with a database and user authentication.

- Login Page

```
forms.py
```

Using the Flask application for user authentication and registration. The script defines two forms, LoginForm and RegistrationForm, using the Flask-WTF extension for handling web forms in a Flask application. The LoginForm includes fields for username, password, and a "Remember Me" checkbox for user login. The RegistrationForm includes fields for username, email, password, and a password confirmation field. Both forms have data validation logic implemented within them. The validate_username and validate_email methods ensure that the entered username and email address are unique in the database by querying the User model. If a duplicate is found, a validation error is raised.

```
models.py
```
This script defines a User model class using Flask-SQLAlchemy for database integration in a Flask application. The User model includes fields for user ID, username, email, and a password hash. It also inherits from UserMixin for Flask-Login integration, which provides user authentication functionality. The load_user function is registered as a loader function for Flask-Login, allowing it to retrieve a user by their ID from the database. The set_password method is used to securely hash and store the user's password, while the check_password method is used to verify the provided password during login. This script is a fundamental part of a Flask application's user authentication system, managing user data and authentication processes.

- Study Planner 

```
routes.py
```

This script defines three Flask blueprints (index, unit, and staff_editing_bp) that organize routes and views for different parts of a web application. The index blueprint handles the main page, displaying data fetched from a database. The unit blueprint provides a route to fetch prerequisites for a specific unit and return them as JSON. The staff_editing_bp blueprint appears to be intended for staff-related functionalities but is not detailed in this snippet. The index_route function renders the main page, planner_route and planner2_route render pages with predefined academic plans, and fetch_database_route returns data from a study planner interface as JSON. Overall, this script sets up routing and views for various components of a web application, including data retrieval and rendering.

## Back End

### Script

```
algo.py
```

This script contains a set of functions related to a study planner algorithm. The algorithm function takes lists of completed and incomplete unit codes, along with a starting semester, and adds units to a study plan based on certain conditions and prerequisites. It iteratively adds units until no more can be added. The script also includes utility functions like remove_string_from_list for removing specified strings from a list and clean_list for cleaning up a list by removing specific string occurrences. Overall, these functions are used in a study planner application to automatically plan a student's course based on completed and incomplete units while considering prerequisites and other criteria.

```
available_units.py
```
This script defines a function named CanDo that checks if a list of incomplete units can be taken based on the completion of their prerequisites. It takes two lists as input: completed_units, which contains unit codes that have been completed, and incomplete_units, which contains unit codes that need to be checked for prerequisites. The function iterates through the incomplete units, retrieves their prerequisites using the get_prerequisites function, and checks if all prerequisites are in the list of completed units or a predefined list of summer units. If all prerequisites are satisfied, the unit is added to the post_units list, which is then returned as a list of units that can be taken. This script is useful for determining which units a student can enroll in based on their completed coursework and prerequisite requirements.

```
constants.py
```
This script defines a set of configuration constants and variables related to a study planner application. It includes file paths for database locations (degree_db_address and study_planner_db_address), static and template folder paths (static_folder_address and template_folder_address), and other application-specific settings like the number of semesters, a list of summer units, points per unit, and strings used for specific purposes (e.g., 'FAIL', 'BROADENING', 'OPTION', 'Select unit'). These constants are used to configure and customize various aspects of the study planner application, such as database connections, folder paths, and default values for specific parameters.

```
create_database.py
```

This script performs database schema setup for a study planner application. It first establishes a connection to an SQLite database located at the address specified in the degree_db_address constant. Then, it creates two tables: UnitCategory to store unit categories, and Unit to store unit-related information such as unit code, name, points required, semester, and category ID. It also inserts predefined category data into the UnitCategory table. Additionally, it creates a table UnitRelationship to manage relationships between units, particularly prerequisites. Finally, the script commits the changes to the database and closes the connection, ensuring that the database schema is properly set up for the study planner application.

```
database_interface.py
```
This script defines a set of functions for interacting with an SQLite database that stores information about academic units and their prerequisites for a study planner application. The functions include get_prerequisites, which retrieves the prerequisites for a given unit code, insert_unit_data for inserting unit data into the database, get_unit_semester to get the semester of a unit, insert_prerequisite to insert prerequisites for a unit, and get_all_units to retrieve all units from the database. These functions allow the application to manage unit data, prerequisites, and semesters, facilitating the automatic planning of a student's academic course based on their completed units and prerequisites. The database connection is opened and closed within each function to ensure proper data access and management.

```
insert_sample_data.py
```
This script inserts sample data into an SQLite database used by a study planner application. It connects to the database specified in the constants.degree_db_address, creates and populates two tables: Unit and UnitRelationship. The Unit table stores information about academic units, including their code, name, semester, unit points, and category ID, and the UnitRelationship table manages relationships between units, particularly prerequisites. Sample data is provided for units, their prerequisites, and associated categories, allowing the application to demonstrate functionality such as unit planning and course requirements checking. After inserting the data, the script commits the changes to the database and closes the connection, confirming that the sample data has been successfully inserted.

```
study_planner_interface.py
```
This script is a Python program that manages a study planner database, allowing users to add study units, update their study plan, and retrieve information about their study progression. It achieves this by defining functions to interact with an SQLite database containing information about study units and their prerequisites. The script can add completed and incompleted study units to the study plan, taking into account prerequisites, current semester, and available slots in the study matrix. It also handles semester updates, calculates current points, and provides functions for clearing the database and fetching the study plan as a structured dictionary. Additionally, it contains utility functions for database operations, such as creating and updating tables. Overall, this script serves as a tool for managing a student's academic study plan by intelligently placing study units in available slots based on various constraints.

## Overall System

```
Project.py
```
This Flask-based Python script creates a web application for managing a university unit planner. It allows users to log in, view their unit planner, and interact with their study plan by marking units as complete or incomplete. The script includes routes for handling login and logout, rendering web pages, and processing JSON data sent by the user. It employs a login system and integrates with a database to store user information and unit data. The key functionality involves categorizing and processing units as complete or incomplete, and then passing this data to an algorithm (presumably for study planning purposes). Additionally, the script serves HTML templates, manages user sessions, and handles errors. Overall, it provides a user-friendly interface for managing a university unit planner.
