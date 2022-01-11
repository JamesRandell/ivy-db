import json

class base:

    def get_db_instance(self):
        self.containerID = ''
        o, r = self.run_shell('docker container list | awk \'{if ($(2) == "cassandra:latest") {print $1}}\'')

        self.containerID = self._clean(o)
        self.dev = 0

        return

    def run_shell(self, arg):
        import subprocess

       
        

        result = subprocess.Popen(arg,
                        shell=True,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        universal_newlines=True) 
        stdout, stderr = result.communicate()

        if (result.returncode != 0):
            print(f'Shell command failed "{arg}"')
            exit()

        return stdout, stderr

    def command (self, cmd):
        self.get_db_instance()
        cmd = f'docker exec {self.containerID} {cmd}'
        out, err = self.run_shell(cmd)

        return out, err

    def processShellResult(self, input, seperator=" "):
        l, c = 0, 0
        output = {}

        for line in input.split("\n"):
            if (line == ''):
                continue
                
            l, c = l + 1, 0

            output[l] = {}
            if (self.dev == 1 ):
                print(f'Line {l}: {line}')
            
            for col in line.split(seperator):
                if (col == ''):
                    continue

                c = c + 1
                
                output[l][c] = col.strip().lower()
                if (self.dev == 1 ):
                    print(f'Col {c}: {col}')

        return output

    def _convertSize(self, col):
        if "KiB" in col:
            temp = col.replace("KiB", '').strip()
            col = float(temp) * 1024
        elif "MiB" in col:
            temp = col.replace("MiB", '').strip()
            col = float(temp) * 1024 * 1024
        elif "NaN" in col:
            temp = col.replace("NaN", '').strip()
            col = ""
        elif "bytes" in col:
            temp = col.replace("bytes", '').strip()
            col = temp
        return col
                    
    def _clean(self, arg):
        return arg.rstrip("\n")
    
