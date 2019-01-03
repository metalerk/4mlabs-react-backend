from flask_restful import Resource
from flask import jsonify

import json

class StoreInfo(Resource):
    def post(self):
        info = self.parser.parse_args()
        print(info)
