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

        if stderr:
            print(stderr)

        if (result.returncode != 0):
            print(f'Shell command failed "{arg}"')
            exit()

        return stdout, stderr

    def command (self, cmd):
        self.get_db_instance()
        cmd = f'docker exec {self.containerID} {cmd}'
        out, err = self.run_shell(cmd)

        return out, err

    def process_shell_result(self, input, seperator=" "):
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

    def process_cql_result(self, input, seperator = "|", key=None):
        """
        Takes the output of a cqlsh shell command and formats it use in the app
        The input here is already in cqlsh JSON format (SELECT JSON...)

        :param input: the cqlsh result to parse and format
        :param seperator: the delimiter to cut up our columns
        :param key: if specified, will 'key' a row by this value returned in each row
        :return: an array of the original result, parsed
        """

        meta = {}

        if key:
            output = {}
        else:
            output = []

        keys = []
        
        rows = input.split("\n")

        # remove any blank rows that get returned from the shell
        rows = list(filter(None, rows))
        
        
        # we process the first row (the header row) outside of the loop
        # and store it's keys in a dedicated array
        for col in rows[0].split(seperator):
            if (col == ''):
                continue

            keys.append(col.strip())

        # cqlsh tidy up. Remove the header row, the seperator row (------)
        # and the row count at the end. Do this in reverse order so we don't
        # trip over outsevles when doing array deletes
        try:
            del rows[len(rows)-1]
            del rows[1]
            del rows[0]
        except KeyError:
            pass

        meta['count'] = len(rows)
        if (meta['count'] == 0):
            meta['nodata'] = True

        for row in rows:
            if (row == ''):
                continue

            # we create a temp object to store each row in so we don't get 
            # row keys in our output, instead it's just a key-less array
            temp = {}
            temp = json.loads(row)

            if key:
                key_value = temp[key]
                output[key_value] = temp
            else:
                output.append(temp)

        return output, meta['count'], meta


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
    
