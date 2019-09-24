from pprint import pprint
from flask_restful import Resource
from flask import jsonify, request
from bson.json_util import dumps
import requests as req
from flask_cors import cross_origin

from utils.mail import send_mail, style_mail

import json
import os


def fetch_provider(query, provider='ip-api'):
    providers = {
        'ip-api': 'http://ip-api.com/json/{}'.format(query),
        #'ipstack': 'http://api.ipstack.com/{}?access_key={}'.format(query, os.getenv('IPSTACK_API_KEY')),
    }
    return req.get(providers[provider]).json()

class VisitorInfo(Resource):
    def __init__(self, parser, mongo, logger):
        self.parser = parser
        self.db = mongo.db
        self.logger = logger

    @cross_origin(origin='*',headers=['Content-Type'])
    def post(self):
        try:
            visitor_info = request.get_json()
            visitor_info['location']['data'] = [
                fetch_provider(provider=visitor_info['location']['provider'], query=x) for x in request.access_route
            ]
            record_id = self.db.visitors.insert_one(dict(visitor_info)).inserted_id
            visitor_info['mongodb_id'] = str(record_id)
            self.logger.debug(visitor_info)

            send_mail(
                from_email=os.getenv('EMAIL_USER', ''),
                to_email=os.getenv('EMAIL_TO', ''),
                subject='Visita al sitio!',
                content=style_mail(title='Registro de visita', track_obj=visitor_info),
                receiver_name='Luis Esteban Rodriguez',
            )

            return jsonify({
                'success': True,
                'data': visitor_info,
            })
        except Exception as e:
            self.logger.debug(str(e))
            return jsonify({
                'success': False,
                'reason': str(e),
                'data': [],
            })
