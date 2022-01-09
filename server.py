from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from json import dumps
#from flask.jsonpify import jsonify



app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()  # initialize
class Employees(Resource):
    def get(self):
        return {'employees': 'employees stuff'} # Fetches first column that is Employee ID

class Tracks(Resource):
    def get(self):
        result = {'data': 'stuff'}
        return jsonify(result)

class Employees_Name(Resource):
    def get(self, employee_id):
        result = {'data': 'employee name stuff'}
        return jsonify(result)
        
class Users(Resource):
    # methods go here
    def post(self):
        parser.add_argument('name', required=True)

        args = parser.parse_args()  # parse arguments to dictionary

        return {'data': 'true'}, 200

api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
     app.run(port='5002')