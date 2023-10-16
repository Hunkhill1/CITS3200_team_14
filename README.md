# Prerequisite Pathways Visualization Website

## Project Overview

Engineering units often have a number of unit prerequisites. Study plans show the prerequisites and the plans are designed to make sure the prerequisites are met. However, students often take units out of sequence and then realize they have not completed a prerequisite, which can impact their academic progression. The Prerequisite Pathways Visualization Website aims to address this issue by providing an intuitive and interactive platform for students to visualize unit prerequisite pathways.

This project utilizes Flask, a Python web framework, to create a dynamic and user-friendly website. When a student selects a specific unit in their study plan, the website will highlight the prerequisite relationships (both forward and backward) between the selected unit and others. This visualization will empower students to make informed decisions about their course selections and ensure they meet the necessary prerequisites.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Setting up Python and Flask](#setting-up-python-and-flask)
- [Usage](#usage)

## Getting Started

### Prerequisites

Before running the project, ensure you have the following prerequisites installed on your system:

- [Python](https://www.python.org/downloads/) (version X.X.X)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/installation/) (version X.X.X)
- [Visual Studio Code](https://code.visualstudio.com/download) (recommended code editor)
- Other dependencies...
  
### Installation

1. **Clone this repository to your local machine:**

   Open your terminal or code editor and run the following command:
   ```shell
   git clone https://github.com/yourusername/CITS3200_team_14.git
   ```

2. **Navigate to the project directory:**
   ```shell
   cd CITS3200_team_14
   ```

3. Create a virtual environment (recommended) and activate it:

   It's best practice to isolate project dependencies in a virtual environment. If you don't have a virtual environment installed, you can get it by running:
   ```shell
   pip install virtualenv
   ```

   Create a virtual environment (replace 'env' with your preferred environment name):
   ```shell
   virtualenv env
   ```

   On Windows, activate the environment with:
   ```shell
   env\Scripts\activate
   ```
   
   On macOS and Linux, use:
   ```shell
   source env/bin/activate
   ```
   
4. Install the project dependencies:
   
   Use pip to install the required packages listed in the requirements.txt file:
   ```shell
   pip install -r requirements.txt
   ```

  #### Setting up Python and Flask
  
  If you don't have Python and Flask installed, you can follow these steps:
  1. Install Python:
     - Visit the Python download page and download the latest version for your operating system.
     - Follow the installation instructions for your platform.
  2. Install Flask:
     - Visit the Flask installation page for guidance on installing Flask.
     - Typically, you can install Flask using pip by running the following command:
       ```shell
       pip install Flask
       ```

### Usage
1. Export Project py File
   Open your terminal or command prompt and set the FLASK_APP environment variable to point to your project file (Project.py). Replace Project.py with your actual project file name:
  ```shell
  export FLASK_APP=Project.py
  ```

2. Run the Flask application:
```shell
   flask run
```

3. Access the Prerequisite Pathways Visualization Website:
   Open your web browser and navigate to http://localhost:5000 to access the Prerequisite Pathways Visualization Website.
   
4. Explore and Visualize Unit Prerequisite Pathways:
   Follow the on-screen instructions to explore and visualize unit prerequisite pathways. Enjoy using the website!
