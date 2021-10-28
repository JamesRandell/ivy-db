from module.base import base
import json

class nodetool(base):

    def __init__(self):
        super().__init__()
        self.cmd = {
            "status": "nodetool status",
            "gcstats": "nodetool gcstats",
            "info": "nodetool info",
            "ring": "nodetool ring",
            "tablestats": "nodetool tablestats -F json",
            "profileload": "nodetool profileload"
        }
        
    def status(self):
        out, err = self.runShell(self.cmd["status"])
        out = self.processShellResult(out)

        status = {"UN": "Up","UL": "Up","UJ": "Up","UM": "Up","DN": "Down","DL": "Down","DJ": "Down","DM": "Down"}
        state = {"UN": "Normal","UL": "Leaving","UJ": "Joining","UM": "Moving","DN": "Normal","DL": "Leaving","DJ": "Joining","DM": "Moving"}

        result = {}
        result["datacenter"] = out[1][2]

        for key, line in out.items(): 
            if (key >= 6):
                result[ line[2] ] = {}
                result[ line[2] ]["status"] = status.get(line[1], "Unknown status")
                result[ line[2] ]["state"] = state.get(line[1], "Unknown state")
                result[ line[2] ]["load"] = line[5]
                result[ line[2] ]["owns"] = line[6]
                result[ line[2] ]["hostID"] = line[7]
                result[ line[2] ]["rack"] = line[8]


        return json.dumps(result), err
    
    def info(self):
        out, err = self.runShell(self.cmd["info"])
        print(out)

        out = self.processShellResult(out, seperator=":")
        print(out)
        result = {}
        for line in out:
            print(f'{line}: {out[line][1]}: {out[line][2]}')
            result[ out[line][1] ] = {}
            result[ out[line][1] ] = out[line][2]

        result["Key Cache"] = self.info_cache(result["Key Cache"])
        result["Row Cache"] = self.info_cache(result["Row Cache"])
        result["Counter Cache"] = self.info_cache(result["Counter Cache"])
        return result, err

    def info_cache(self, cacheStr):
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
        result["hit_rate"] = temp[6].replace('recent hit rate', '').strip()
        result["save_period"] = temp[7].replace('save period in seconds', '').strip()

        return result

    def tablestats(self):
        out, err = self.runShell(self.cmd["tablestats"])
        return out, err