from flask import Flask
from .configuration.configuracion import Config
from .blueprints.actions import actions_blueprint
import logging

app = Flask(__name__)
app = Config.init()

app.register_blueprint(actions_blueprint, url_prefix='/blacklists')

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)