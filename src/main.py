from typing import Any
from flask import Flask, jsonify, make_response, request
from marshmallow import ValidationError
from bd import Cars
from schema import CarSchema
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)


class CarResource(Resource):
    def get(self):
        return make_response(jsonify(
            value=Cars,
            total=len(Cars)
        ))

    def post(self):
        try:
            data = request.json
            schema = CarSchema()
            result = schema.load(data)
        except ValidationError as err:
            return abort(400, message=err.messages)

        Cars.append(result)
        return make_response(jsonify(
            message='Created successs',
            id=123
        ), 201)


api.add_resource(CarResource, '/cars')

if __name__ == '__main__':
    app.run(port=8000)
