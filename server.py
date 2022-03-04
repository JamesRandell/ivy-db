from flask import Flask, request, jsonify
from flask_restx import Resource, Api, reqparse, Namespace
from module.base import base
import json

from view.ns_server import ns_nodetool
from view.ns_table import ns_table
from view.ns_keyspace import ns_keyspace
from view.ns_health import ns_health

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
api.add_namespace(ns_keyspace)
api.add_namespace(ns_health)

#app.register_blueprint(api_bp, url_prefix='/test')



#@ns_server.route('/')
class keyspace(Resource, base):
    def get(self, keyspace):
        out, err = self.command(f"cqlsh -e \"SELECT JSON * FROM system_schema.tables WHERE table_name = '{keyspace}' ALLOW FILTERING\"")
        print(out)
        print('fffffff')
        out = self.process_cql_result(out, key="table_name")
        
        return jsonify(out)

api.add_resource(keyspace, '/<string:keyspace>')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5000')