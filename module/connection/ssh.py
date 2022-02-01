#from asyncio import subprocess
import subprocess
from module.shell import Shell
import os

class Conn(Shell):



    def __init__(self, config):
        self.shell_string = '' # this is what our app will use to prefix any commands we send to the database on the shell 

        self.config = config # not used right now as i'm just dealing with local docker

        self.path_cert = os.path.dirname(os.path.realpath(__file__)) + '\keys\starbuck_rest_api_key'

        if os.path.exists(self.path_cert) == False:
            exit(f'File does not exist: {self.path_cert}')

        print(f'Found key file: {self.path_cert}')
        
        container_id = self.choose_host()
        

        self._create_certs()
        
        self.build_shell_string(container_id)


    def build_shell_string(self, container_id):
        self.shell_string = f'docker exec {container_id}'


        

    def choose_host(self):

        # the host key contains a list of hosts
        for host in self.config['database_config']['host']:

            # -o options, including connection timeout in seconds
            # -oStrictHostKeyChecking gets around any invalid root CAs
            # -tt force psueo tty (honestly can't remember why this is here, test without?)
            # -i private key (identity file)
            #try:
            ssh = subprocess.Popen(['ssh',
                                        '-o',
                                        'ConnectTimeout=2',
                                        '-oStrictHostKeyChecking=no',
                                        '-tt',
                                        f'root@{host}',
                                        '-i',
                                        f'"{self.path_cert}"',
                                        f'"nodetool status"'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            (stdout, stderr) = ssh.communicate()
                #o, r = Shell.run(f'ssh -o ConnectTimeout=2 -oStrictHostKeyChecking=no -tt root@{host} -i "{self.path_cert}" "nodetool status"')
            #except:
            if stderr:
                print(stderr)
            else:
                return stdout
                #print(f'R:{r}')
        #return o.rstrip("\n")

    def _create_certs(self):
        #ssh-keygen -b 2048 -t rsa -f C:/temp/sshkey -q -N ""


        out, err = Shell.run(f'ssh-keygen -b 2048 -t rsa -f "{self.path_cert}" -q -N ""')

        out, err = Shell.run(f'ssh-keygen -b 2048 -t rsa -f "{self.path_cert}" -q -N ""')
        print(out)
        print(err)
        #Shell.run('ssh-keygen')