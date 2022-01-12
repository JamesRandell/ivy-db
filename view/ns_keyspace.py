from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, reqparse, Namespace
from module.base import base
import json



# Namespace
ns_keyspace = Namespace('_keyspace', description='Keyspace')


class ns_keyspace_all(Resource, base):

    def get(self):
        out, err = self.command("cqlsh -e \"SELECT JSON * FROM system_schema.keyspaces\"")
        out = self.process_cql_result(out, key="keyspace_name")

        return jsonify(out)
ns_keyspace.add_resource(ns_keyspace_all, '/') # Route_2

@ns_keyspace.route('/<string:keyspace>')
class ns_keyspace_single(Resource, base):

    @ns_keyspace.doc(
        responses={
            200: 'Keyspace found',
            404: 'Keyspace not found'},
        params={
            'keyspace': 'Name of a keyspace'
        })
    def get(self, keyspace):
        out, err = self.command(f"cqlsh -e \"SELECT JSON * FROM system_schema.keyspaces WHERE keyspace_name = '{keyspace}' ALLOW FILTERING\"")
        out, rows, meta = self.process_cql_result(out, key="keyspace_name")
        
        if (rows):
            print(f'rows: {rows}')
            return out, 200
        else:
            return {'error':'Keyspace not found'}, 404
#ns_keyspace.add_resource(ns_keyspace_single, '/<string:keyspace>') # Route_2


