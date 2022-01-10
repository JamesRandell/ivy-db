from flask import Flask, Blueprint
from flask_restx import Resource, Api, reqparse, Namespace
from module.base import base
import json

#blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

# Namespace
ns_nodetool = Namespace('nodetool', description='a test namespace')


class Test(Resource, base):
    @ns_nodetool.response(200, 'Success')
    @ns_nodetool.response(400, 'Validation Error')
    def get(self):
        result = {'data': 'stuff'}
        #return jsonify(result)
        return 'hello', 200




class nodetool_status(Resource, base):

    def get(self):
        out, err = self.runShell("nodetool status")
        out = self.processShellResult(out)

        status = {"UN": "Up","UL": "Up","UJ": "Up","UM": "Up","DN": "Down","DL": "Down","DJ": "Down","DM": "Down"}
        state = {"UN": "Normal","UL": "Leaving","UJ": "Joining","UM": "Moving","DN": "Normal","DL": "Leaving","DJ": "Joining","DM": "Moving"}

        result = {}
        result["datacenter"] = out[1][2]
        result["host"] = []

        for key, line in out.items(): 
            if (key >= 6):
                temp = {}
                #result["host"][ line[2] ] = {}
                temp["status"] = status.get(line[1], "Unknown status")
                temp["state"] = state.get(line[1], "Unknown state")
                temp["load"] = line[5]
                temp["owns"] = line[6]
                temp["hostID"] = line[7]
                temp["rack"] = line[8]
                result["host"].append(temp)


class nodetool(base):

    def __init__(self, dev=0):
        super().__init__()
        self.cmd = {
            "status": "nodetool status",
            "gcstats": "nodetool gcstats",
            "info": "nodetool info",
            "ring": "nodetool ring",
            "tablestats": "nodetool tablestats -F json",
            "profileload": "nodetool profileload",
            "histograms": "nodetool tablehistograms"
        }
        
    def status(self):
        out, err = self.runShell(self.cmd["status"])
        out = self.processShellResult(out)

        status = {"UN": "Up","UL": "Up","UJ": "Up","UM": "Up","DN": "Down","DL": "Down","DJ": "Down","DM": "Down"}
        state = {"UN": "Normal","UL": "Leaving","UJ": "Joining","UM": "Moving","DN": "Normal","DL": "Leaving","DJ": "Joining","DM": "Moving"}

        result = {}
        result["datacenter"] = out[1][2]
        result["host"] = []

        for key, line in out.items(): 
            if (key >= 6):
                temp = {}
                #result["host"][ line[2] ] = {}
                temp["status"] = status.get(line[1], "Unknown status")
                temp["state"] = state.get(line[1], "Unknown state")
                temp["load"] = line[5]
                temp["owns"] = line[6]
                temp["hostID"] = line[7]
                temp["rack"] = line[8]
                result["host"].append(temp)


        return result, err
    
    def info(self):
        out, err = self.runShell(self.cmd["info"])
        out = self.processShellResult(out, seperator=":")

        result = {}
        for line in out:
            result[ out[line][1] ] = {}
            result[ out[line][1] ] = out[line][2]

        result["load"] = self._convertSize(result["load"])
        result["key cache"] = self._info_cache(result["key cache"])
        result["row cache"] = self._info_cache(result["row cache"])
        result["counter cache"] = self._info_cache(result["counter cache"])
        
        return result, err

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

        return result, err

    def profileload(self):
        out, err = self.runShell(self.cmd["profileload"])
        print(out)
        out = self.processShellResult(out, seperator=":")

        print(out)
        return out, err
    
    def histograms(self):
        out, err = self.runShell(self.cmd["histograms"])
        print(out)
        out = self.processShellResult(out, seperator=":")

        print(out)
        return out, err

    def tablestats(self):
        out, err = self.runShell(self.cmd["tablestats"])
        return out, err

ns_nodetool.add_resource(nodetool_status, '/status') # Route_2