from flask import Flask
from database.db import mongo
from flask_restful import Api
from .routes import initialize_routes

app = Flask(__name__)
api = Api(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Wallet"
app.config['MONGO_DBNAME'] = 'Wallet'
app.config['SECRET_KEY'] = 'secret_key'

initialize_routes(api)
mongo.init_app(app)
