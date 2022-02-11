#from asyncio import subprocess
import subprocess
from module.shell import Shell
import os

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class Conn(Shell):



    def __init__(self, config):
        self.shell_string = '' # this is what our app will use to prefix any commands we send to the database on the shell 

        self.config = config # not used right now as i'm just dealing with local docker

        self.path_cert = os.path.dirname(os.path.realpath(__file__)) + '\keys\id_rsa'

        self.ssh_user = 'starbuck'


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
            print(f'{color.HEADER}Connecting to: {self.ssh_user}@{host}{color.END}') 
            ssh = subprocess.Popen(['ssh',
                                        '-o',
                                        'ConnectTimeout=2',
                                        '-o',
                                        'StrictHostKeyChecking=no',
                                        '-tt',
                                        f'{self.ssh_user}@{host}',
                                        '-i',
                                        f'{self.path_cert}',
                                        f'nodetool status'],
                                    stdin=subprocess.PIPE, 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE) 
            (stdout, stderr) = ssh.communicate() 
                #o, r = Shell.run(f'ssh -o ConnectTimeout=2 -oStrictHostKeyChecking=no -tt root@{host} -i "{self.path_cert}" "nodetool status"')
            #except:
            if stderr:
                print(f'{stderr}')
                print(f'fff{color.FAIL}{stdout.decode("utf-8").strip()}{color.END}')
                print(stderr.decode("utf-8").strip())
            else:
                return stdout.decode("utf-8").strip()

        #return o.rstrip("\n")

    def _create_certs(self):

        out, err = Shell.run(f'ssh-keygen -b 2048 -t rsa -f "{self.path_cert}" -q -N ""')
        print(out)
        print(err)
        #Shell.run('ssh-keygen')