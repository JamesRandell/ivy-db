from flask import Flask, request, jsonify
from flask_restx import Resource, Api, reqparse, Namespace
from json import dumps

from view.ns_server import ns_nodetool
from view.ns_table import ns_table

app = Flask(__name__) 
#api = Api(app = app)



api = Api(
    #blueprint,
    app = app,
    version="1.0",
    title="API Cassandra",
    description="Cassandra REST API"
)
#parser = reqparse.RequestParser()  # initialize
# APIs are defined under a given namespace, they appear under a given heading in Swagger
api.add_namespace(ns_nodetool)
api.add_namespace(ns_table)

#app.register_blueprint(api_bp, url_prefix='/test')



#@ns_server.route('/')
class HelloWorld(Resource):
    def get(self):
        return 'hello'


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

#ns_server.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3
#api.add_resource(nodetool, '/nodetool')

if __name__ == '__main__':
     app.run(port='5000')