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

    def processShellResult(self, input, seperator=" ", pivot=False):
        l, c = 0, 0
        output = {}
        keys = []

        lines = input.split("\n")

        lines = list(filter(None, lines))

        for line in lines:
            #if (line == ''):
            #    continue
            
            l, c = l + 1, 0

            if (l == 2 or l == (len(lines))):
                continue

            

            output[l] = {}

            if (pivot == True and l == 1):
                for col in line.split(seperator):
                    if (col == ''):
                        continue

                    keys.append(col.strip())

            if (self.dev == 1 ):
                print(f'Line {l}: {line}')
            
            for col in line.split(seperator):
                if (col == ''):
                    continue

                if (keys):
                    output[l][keys[c]] = col.strip().lower()    
                else:
                    output[l][c] = col.strip().lower()
                
                c = c + 1
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
    
