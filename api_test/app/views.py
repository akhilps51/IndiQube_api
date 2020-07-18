from flask import Flask, session, Blueprint, jsonify, request, Response
from database.db import mongo
from flask_restful import Resource
import pandas as pd

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Home(Resource):
    def get(self):
        res = {"update_api": "/wallet", "balance_check": "/fetch/balance"}
        return jsonify(res)

class WalletApi(Resource):
    def post(self):
        if 'file' not in request.files:
            return jsonify({"error": "Invalid file", "message": "Please upload a valid file with csv extention", "status": False})
        data_file = request.files.get('file')
        if data_file.filename == '':
            return jsonify({"error": "Invalid file", "message": "Please upload a valid file with csv extention", "status": False})
        if data_file and allowed_file(data_file.filename):
            df = pd.read_csv(data_file, header=0, names=[])
            wallet_collection = mongo.db.wallet
            for data in df.index:
                existing_data = list(wallet_collection.find({"email": data[0]}, {"balance": 1, "_id": 0}))
                if len(existing_data):
                    balance = existing_data[0]['balance']
                    wallet_collection.update({"email": data[0]}, {"$set": {"balance": balance+data[1]}})
                else:
                    wallet_collection.insert({"email": data[0], "balance": data[1]})
            return jsonify({"status": True, "message": "Wallet updated"})
        else:
            return jsonify({"error": "Invalid file", "message": "Please upload a valid file with csv extention", "status": False})


class CheckBalance(Resource):
    def get(self):
        email = request.args.get('email')
        if email:
            wallet_collection = mongo.db.wallet
            data = list(wallet_collection.find({"email": email}))
            if len(data):
                response = {"email": data[0]['email'], "balance": data[0]['balance'], "status": True}
            else:
                response = {"status": False, "message": "Please provide valid email address", "error": "Invalid Email"}
        else:
            response = {"status": False, "message": "Please provide valid email address", "error": "Invalid Email"}
        return jsonify(response)

