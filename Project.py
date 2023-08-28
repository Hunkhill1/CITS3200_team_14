from flask import Flask
from config import Config
from app.routes import index, unit  # Import the Blueprint

app = Flask(__name__)
app = Flask(__name__, template_folder='app/templates')
app.config.from_object(Config)
app.register_blueprint(index)
app.register_blueprint(unit, url_prefix='/unit')  # Register the Blueprint with the URL prefix

if __name__ == '__main__':
    app.run(debug=True)

