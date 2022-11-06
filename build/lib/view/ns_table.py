from flask import Flask, Blueprint, jsonify, request
from flask_restx import Resource, Api, reqparse, Namespace
from module.base import base
import json

#blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

# Namespace
api = Namespace('table', description='Tabla meta data')
#ns_keyspace = Namespace('{keyspace}', description='Keyspace')


parser = api.parser()
parser.add_argument('table', 
    type=str, 
    help='Name of the table to create', 
    location='form',
    required=True)

@api.route('/<string:keyspace>',
    doc={
        'description':'Everything related to tables in a keyspace'
    }
)
class ns_table_table(Resource, base):

    @api.doc(
        responses={
            200: 'Returns all the tables in a keyspace',
            404: 'Keyspace not found or no tables exist in keyspace'},
        params={
            'keyspace': 'Name of a keyspace'
        })

    def get(self, keyspace):
        out, err = self.command(f'cqlsh -e "SELECT JSON * FROM system_schema.tables WHERE keyspace_name = \'system\'"')
        out, count, meta = self.process_cql_result(out)
        
        if (count == 0):
            return meta, 404
        else:
            return out, 200


    @api.doc(
        responses={
            201: 'Table created successfully',
            400: 'Could not create table, see error for more details',
            404: 'Keyspace not found'},
        params={
            'keyspace': 'Name of a keyspace'
        }) 
    @api.expect(parser)
    def put(self, keyspace):
        parsed_template = self._parse_create_table()
        out, err = self.command_cql(parsed_template)
        
        result = {}
        if err:
            return err, 400
        else:
            result['message'] = f'Table created in keyspace: {keyspace}'
            return result, 201


    def _parse_create_table(self):
        data = {}
        data['keyspace'] = request.form.get('keyspace')
        data['table'] = request.form.get('table')
        print(1111)
        print(data)
        print(2222)
        return self.template('create_table', data)


ns_table = api


