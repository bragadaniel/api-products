from typing import Any
from flask import Flask, jsonify, make_response, request
from marshmallow import ValidationError
from bd import Cars
from schema import CarSchema

app = Flask(__name__)

@app.route('/cars', methods=['GET'])
def get_cars():
  return make_response(jsonify(
    message= 'Cars List',
    value=Cars
    ))

@app.route('/cars', methods=['POST'])
def create_car():
  try:
     data: Any = request.json
     schema = CarSchema()
     result: Any = schema.load(data)
  except ValidationError as err:
     return bad_request(err.messages)
      
  Cars.append(result)
  return  make_response(jsonify(
    message='Created success'
  ), 201)

@app.errorhandler(400)
def bad_request(e):
    return make_response(jsonify(
    message=e
  ), 400)

if __name__ == '__main__':
  app.run(port=8000)
