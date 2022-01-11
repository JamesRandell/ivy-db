from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, reqparse, Namespace
from module.base import base
import json

#blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

# Namespace
ns_table = Namespace('_table', description='Cluster wide information')




class test(Resource, base):

    def get(self):
        out, err = self.command("cqlsh -e \"SELECT * FROM system_schema.tables\"")
        #print(f'A: {out}') 
        #out = self.processShellResult(out)
        #print(f'B: {out}') 
        out = self.processShellResult(out, seperator="|")
        return jsonify(out)
ns_table.add_resource(test, '/status') # Route_2


