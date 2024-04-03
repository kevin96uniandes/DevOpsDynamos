import os
from flask import Flask
from dotenv import load_dotenv
from ..models.models import db
from datetime import timedelta


class Config:

    @staticmethod
    def init():
        app = Flask(__name__)
        load_dotenv('.env.template')

        db_url = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_url}"


        """
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
        )
        """

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config["PROPAGATE_EXCEPTIONS"] = True
        app.config['JWT_SECRET_KEY'] = 'frase-secreta'
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=10)
        app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

        app_context = app.app_context()
        app_context.push()

        db.init_app(app)
        db.create_all()

        return app