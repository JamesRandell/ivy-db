class base:

    def __init__(self):
        self.containerID = ''
        o, r = self.runShell('docker container list | awk \'{if ($(2) == "cassandra:latest") {print $1}}\'')
        self.containerID = self._clean(o)

        return
    

    def runShell(self, arg):
        import subprocess
        if (self.containerID != ''):
            arg = f'docker exec {self.containerID} {arg}'

        print(arg)
        result = subprocess.Popen(arg,
                        shell=True,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        universal_newlines=True) 
        stdout, stderr = result.communicate()
        return stdout, stderr

    def _clean(self, arg):
        return arg.rstrip("\n")
    
