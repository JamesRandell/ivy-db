from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, reqparse, Namespace
from module.base import base
import json

#blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

# Namespace
ns_cluster = Namespace('cluster', description='Cluster wide information')

class nodetool_status(Resource, base):

    def get(self):
        out, err = self.command("nodetool status")
        out = self.process_shell_result(out)

        status = {"UN": "Up","UL": "Up","UJ": "Up","UM": "Up","DN": "Down","DL": "Down","DJ": "Down","DM": "Down"}
        state = {"UN": "Normal","UL": "Leaving","UJ": "Joining","UM": "Moving","DN": "Normal","DL": "Leaving","DJ": "Joining","DM": "Moving"}

        # convert keys to lowercase
        status = {k.lower(): v for k, v in status.items()}
        state = {k.lower(): v for k, v in state.items()}

        result = {}
        
        result["datacenter"] = out[1][2]
        result["host"] = []

        for key, line in out.items(): 
            if (key >= 6):
                ii = 0
                temp = {}
                # 1: UN/DN etc
                # 2: Address (IP) 
                # 3: Load
                # 4: Load in KiB (sometimes is empty is previous value is a ?)
                # 5: Tokens
                # 6: Owns (effective)
                # 7: Host ID
                # 8: Rack
                temp["status"] = status.get(line[1], "Unknown status")
                temp["state"] = state.get(line[1], "Unknown state")
                temp["load"] = line[3]

                if (line[3] == '?'):
                    """
                    Skip the next list item as it will be a unit, such as KiB
                    """
                    ii = 1
                
                temp["tokens"] = line[5-ii]
                temp["owns"] = line[6-ii]
                temp["hostID"] = line[7-ii]
                temp["rack"] = line[8-ii]
                result["host"].append(temp)

        
        return result, 200
ns_cluster.add_resource(nodetool_status, '/status') # Route_2


class nodetool_info(Resource, base):

    def get(self):
        out, err = self.command("nodetool info")
        out = self.process_shell_result(out, seperator=":")

        result = {}
        for line in out:
            result[ out[line][1] ] = {}
            result[ out[line][1] ] = out[line][2]

        result["load"] = self._convertSize(result["load"])
        result["key cache"] = self._info_cache(result["key cache"])
        result["row cache"] = self._info_cache(result["row cache"])
        result["counter cache"] = self._info_cache(result["counter cache"])

        return result, 200

    def _info_cache(self, cacheStr):
        counter = 0
        temp, result = {}, {}

        for line in cacheStr.split(","):
            counter = counter + 1
            temp[counter] = line.strip()

        result["entries"] = temp[1].replace('entries', '').strip()
        result["size"] = self._convertSize(temp[2].replace('size', '').strip())
        result["capacity"] = self._convertSize(temp[3].replace('capacity', '').strip())
        result["hits"] = temp[4].replace('hits', '').strip()
        result["requests"] = temp[5].replace('requests', '').strip()
        result["hit_rate"] = self._convertSize(temp[6].replace('recent hit rate', '').strip())
        result["save_period"] = temp[7].replace('save period in seconds', '').strip()

        return result
ns_cluster.add_resource(nodetool_info, '/info') # Route_2


class nodetool_profileload(Resource, base):
    def get(self):
        out, err = self.command("nodetool profileload")
        out = self.process_shell_result(out, seperator=":")
        #out = json.loads(out)
        return out, 200
ns_cluster.add_resource(nodetool_profileload, '/profile') # Route_2


class nodetool_histograms(Resource, base):
    def get(self):
        out, err = self.command("nodetool tablehistograms -F")
        out = self.process_shell_result(out, seperator=":")
        #out = json.loads(out)
        
        return out, 200
ns_cluster.add_resource(nodetool_histograms, '/histogram') # Route_2


class nodetool_tablestats(Resource, base):
    def get(self):
        out, err = self.command("nodetool tablestats -F json")
        out = json.loads(out)
        
        return out, 200

ns_cluster.add_resource(nodetool_tablestats, '/tablestats') # Route_2