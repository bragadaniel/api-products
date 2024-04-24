import json

from flask import Flask, jsonify, make_response, request
from marshmallow import ValidationError
from bson import ObjectId, json_util
from schema import CarSchema
from flask_restful import Resource, Api, abort
from pymongo import MongoClient, ASCENDING, DESCENDING
from dotenv import dotenv_values
from mongoengine import Q

config = dotenv_values(".env")

app = Flask(__name__)
api = Api(app)


class CarResource(Resource):

    def __init__(self) -> None:
        self.__connection_uri = config["MONGO_DB_URI"]
        self.__database_name = config["DB_NAME"]
        self.__collection_name = config["COLLECTION_NAME"]
        self.convert_object_ids = _convert_object_ids(doc=[])
        try:
            self.__client = MongoClient(self.__connection_uri)
            self.__db_connection = self.__client.get_database(self.__database_name)
            self.__collection = self.__db_connection.get_collection(self.__collection_name)
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error: {e}")

    def get(self):
        size: int = int(request.args.get('size', 1))
        page: int = int(request.args.get('page', 10))
        sort_by: str = request.args.get('column', None)
        order: str = request.args.get('order')
        sort_order: int = ASCENDING if order == 'asc' else DESCENDING if order == 'desc' else None

        result = self.__collection.find({})
        result_list = list(result)
        id_list = [item['_id'] for item in result_list]

        query = Q(_id__in=id_list)
        normalize_query = query.to_query(document={})

        data_pipeline: list = [
            {"$lookup": {
                "from": "cars",
                "localField": "car_id",
                "foreignField": "_id",
                "as": "C"
            }},
            {"$match": normalize_query},
            {"$skip": (page - 1) * size},
            {"$limit": size},
            {"$addFields": {
                "name_car": {"$arrayElemAt": ["$C.name_car", 0]}
            }},
            *([{"$sort": {sort_by: sort_order}}] if sort_by else []),
            {"$project": {"C": 0}}
        ]

        count_pipeline: list = [
            {"$count": "total_elements"}
        ]

        ag = self.__collection.aggregate([
            {"$facet": {
                "data": data_pipeline,
                "count": count_pipeline
            }},
            {"$addFields": {
                "total_elements": {"$arrayElemAt": ["$count.total_elements", 0]}
            }},
            {"$project": {"count": 0}}
        ])

        ag_to_list = next(ag)
        data = ag_to_list.get('data')
        total = ag_to_list.get('total_elements')
        ag_converted = _convert_object_ids(doc=data)

        return make_response(jsonify(
            value=ag_converted,
            total=total,
            page=page,
            size=size
        ))

    def post(self):
        try:
            data = request.json
            schema = CarSchema()
            validate_data = schema.load(data)
            self.__collection.insert_one(validate_data)
        except ValidationError as err:
            return abort(400, message=err.messages)

        return make_response(jsonify(
            message='Created success',
            id=123
        ), 201)

    def delete(self, car_id):
        self.__collection.delete_one({'_id': ObjectId(car_id)})
        return make_response(jsonify(
            message='Deleted success',
            id=123
        ), 204)


def _convert_object_ids(doc):
    dump = json_util.dumps(doc)
    return json.loads(dump)


api.add_resource(CarResource, '/cars')

if __name__ == '__main__':
    app.run(port=8000)
