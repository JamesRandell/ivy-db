from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, reqparse, Namespace
from module.base import base
import json

#blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

# Namespace
api = Namespace('health', description='Health API')

parser = api.parser()
parser.add_argument('keyspace', 
    type=str, 
    help='The keyspace', 
    location='args', 
    required=True)
parser.add_argument('table',
    type=str, 
    help='The table', 
    location='args', 
    required=True)

@api.route('/<string:keyspace>/<string:table>',
    doc={
        'description':'Health API'
    }
)
class ns_health_health(Resource, base):
    def get(self, keyspace, table):
        out, err = self.command(f"nodetool tablehistograms {keyspace} {table}")
        
        out = self.process_shell_result(out, seperator="    ")

        # lets deal with some errors that may happen
        # save the first row if it mentions no sstables exist on a single value
        if (len(out[1]) == 1):
            sstable = out[1]

        # find the number of cols in the last row, as this will be how many cols we 
        # actually have, anything less is something wierd
        no_of_rows = len(out)
        no_of_cols = len(out[no_of_rows-1])

        for key in [key for key in out if len(out[key]) < no_of_cols]: del out[key]

        # because we've deleted some keys, we need to get the first 'row', but we don't know what the key is
        # also update the length of the result (how many rows are we left with)
        first_key = list(out.keys())[0]
        no_of_rows = len(out)
        row_i, col_i = 0, 1
        new_out = {}
        print(first_key)

        # now we can pivot the result, using all the cols in the first row as 'keys' for all the values in the dict
        new_out.update(out[first_key])
        for row in out:
            

            temp = {}
            # skip the header row as we assigned this outside the loop
            if (row_i == 0):
                row_i+=1
                continue
            print(row)
            col_i=1
            for col in out[row].items():
                print(f'Col loop: {row}:{col_i}')
                temp[col] = out[row][col_i]

                col_i+=1

            new_out.update(temp)
            row_i+=1

        out = new_out
        #out = json.loads(out)
        
        return out, 200


ns_health = api