from quart import Quart
from quart_cors import cors

from flask import Flask, request, jsonify
from flask_restx import Resource, Api, reqparse, Namespace
from flask_cors import CORS, cross_origin
from module.base import base
import json



from view.ns_cluster import ns_cluster
from view.ns_table import ns_table
from view.ns_keyspace import ns_keyspace
from view.ns_health import ns_health

app = Flask(__name__) 
#api = Api(app = app) 




api = Api(
    #blueprint,
    app = app,
    version="1.0.0",
    title="API Cassandra",
    description="Cassandra REST API"
)

# enable CORS
CORS(app, allow_origin="*", allow_methods=["GET", "POST", "DELETE", "OPTIONS"], allow_headers=['Content-Type', 'Access-Control-Allow-Origin','Access-Control-Allow-Headers', 'Access-Control-Allow-Methods'])


#CORS(app)
#CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}}, allow_headers=['Content-Type', 'Access-Control-Allow-Origin',
#                         'Access-Control-Allow-Headers', 'Access-Control-Allow-Methods'])
#CORS(app, support_credentials=True)
#, resources={r'/*': {'origins': '*'}}

#parser = reqparse.RequestParser()  # initialize
# APIs are defined under a given namespace, they appear under a given heading in Swagger
api.add_namespace(ns_cluster)
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
#ssl_context='adhoc',
if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5000', debug=True)
