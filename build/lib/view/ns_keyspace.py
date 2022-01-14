from flask import Flask, Blueprint, jsonify, request
from flask_restx import Resource, Api, reqparse, Namespace
from module.base import base

import json



# Namespace
ns_keyspace = Namespace('keyspace', description='Keyspace')

parser = ns_keyspace.parser()
parser2 = ns_keyspace.parser()
parser.add_argument('keyspace', type=str, help='The name of the Keyspace to create', location='form', required=True)
parser2.add_argument('keyspace', type=str, help='The name of the Keyspace to delete', location='form', required=True)
parser.add_argument('datacenter', 
    type=str, 
    help='Which datacenter to create the keyspace in. You can check the /cluster/status api for this info', 
    location='form',
    default='datacenter1',
    required=True)
parser.add_argument('replication_strategy', 
    type=str, 
    help='Which replication stratgey to choose. Can shooe between NetworkTopologyStrategy and SimpleStrategy', 
    location='form',
    default='NetworkTopologyStrategy',
    required=True)
parser.add_argument('replication_factor', 
    type=int, 
    help='How many nodes to write the data too', 
    location='form',
    default=1,
    required=True)


@ns_keyspace.route('/',
    doc={
        'description':'Everything related to cassandra keyspaces'
    }
)
class ns_keyspace_all(Resource, base):

    @ns_keyspace.doc(
        responses={
            200: 'List of all keyspaces in the cluster'}
        )
    def get(self):
        out, err = self.command("cqlsh -e \"SELECT JSON * FROM system_schema.keyspaces\"")
        out = self.process_cql_result(out, key="keyspace_name")

        return out, 200

 
    @ns_keyspace.doc(
        responses={
            201: 'Keyspace created',
            400: 'Could not create new keyspace, check error message'}
        )
    @ns_keyspace.expect(parser)
    def put(self):
        parsed_template = self._parse_create_keyspace()
        out, err = self.command_cql(parsed_template)
        
        result = {}
        if err:
            return err, 400
        else:
            result['message'] = 'Keyspace created'
            return result, 201


    @ns_keyspace.doc(
        responses={
            200: 'Keyspace deleted',
            400: 'Could not delete keyspace, check the error message'}
        )
    @ns_keyspace.expect(parser2)
    def delete(self):
        keyspace = request.form.get('keyspace')

        result = {}
 
        out, err = self.command_cql(f"DROP KEYSPACE {keyspace}")
        
        if err:
            return err, 400
        else:
            result['message'] = 'Keyspace deleted'
            return result, 200

    def _parse_create_keyspace(self):
        data = {}
        data['keyspace'] = request.form.get('keyspace')
        data['datacenter'] = request.form.get('datacenter')
        data['replication_strategy'] = request.form.get('replication_strategy')
        data['replication_factor'] = request.form.get('replication_factor')

        return self.template('create_keyspace', data)
        
@ns_keyspace.route('/<string:keyspace>')
class ns_keyspace_single(Resource, base):

    @ns_keyspace.doc(
        responses={
            200: 'Returns information about a keyspace',
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


