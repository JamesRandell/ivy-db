from module.base import base

class nodetool(base):

    def __init__(self):
        super().__init__()
        self.cmd = {
            "status": "nodetool status",
            "gcstats": "nodetool gcstats",
            "info": "nodetool info",
            "ring": "nodetool ring",
            "tablestats": "nodetool tablestats",
            "profileload": "nodetool profileload"
        }
        
    def status(self):
        out, err = self.runShell(self.cmd["status"])
        return out, err

        