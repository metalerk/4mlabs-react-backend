from flask import Flask
from flask_restful import Api, reqparse
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo

from api.visitor_info import VisitorInfo

import random
import string
import os
import logging


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"])
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

app.config['DEBUG'] = os.getenv('DEBUG', True)
app.config['SECRET_KEY'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/test')

parser = reqparse.RequestParser()
mongo = PyMongo(app)

api.add_resource(VisitorInfo, '/visitorinfo', resource_class_kwargs={'parser': parser, 'mongo': mongo, 'logger': app.logger})

parser.add_argument('visitor_info', type=dict, location='body')

if __name__ == '__main__':
    app.run(host=os.getenv('APP_HOST', '0.0.0.0'), port=os.getenv('APP_PORT', '8080'))
