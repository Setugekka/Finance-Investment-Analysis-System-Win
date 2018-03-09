# coding=utf-8
from flask import Flask
from flask_apscheduler import APScheduler
from config import DevConfig
from models import db
from Api.Controller.database_update import database_update
from Api.Controller.wind_data import wind_data


def create_app(object_name):
    scheduler = APScheduler()
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    # create_admin(app)
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    #模块注册
    app.register_blueprint(database_update)
    app.register_blueprint(wind_data)
    return app
