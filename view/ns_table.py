from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, reqparse, Namespace
from module.base import base
import json

#blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

# Namespace
ns_table = Namespace('_table', description='Cluster wide information')
ns_keyspace = Namespace('{keyspace}', description='Keyspace')



class test(Resource, base):

    def get(self):
        out, err = self.command("cqlsh -e \"SELECT JSON * FROM system_schema.tables\"")
        #print(f'A: {out}') 
        #out = self.processShellResult(out)
        #print(f'B: {out}') 
        
        out = self.process_cql_result(out, key="table_name")


        return jsonify(out)
ns_table.add_resource(test, '/status') # Route_2

class ns_table_table(Resource, base):

    def get(self, table):
        out, err = self.command("cqlsh -e \"SELECT JSON * FROM system_schema.tables\"")
        #print(f'A: {out}') 
        #out = self.processShellResult(out)
        #print(f'B: {out}') 
        out = self.process_cql_result(out, key="table_name")


        return jsonify(out)
ns_keyspace.add_resource(ns_table_table, '/<string:table>') # Route_2


