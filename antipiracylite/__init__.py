from flask import Flask

# import blueprints
from antipiracylite.blueprints.api import api
from antipiracylite.blueprints.frontend import frontend

# register app & blueprints
app = Flask(__name__)
app.register_blueprint(frontend)
app.register_blueprint(api, url_prefix='/api')
