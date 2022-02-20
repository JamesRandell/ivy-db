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
        #self.shell_string = '' # this is what our app will use to prefix any commands we send to the database on the shell 
        
        self.config = config # not used right now as i'm just dealing with local docker

        self.path_cert = os.path.dirname(os.path.realpath(__file__)) + '\keys\id_rsa'

        self.ssh_user = 'starbuck'


        if os.path.exists(self.path_cert) == False:
            exit(f'{color.FAIL}File does not exist: {self.path_cert}{color.END}')

        print(f'{color.HEADER}Found key file: {self.path_cert}{color.END}')
        
        container_id = self.run_ssh_command()
    

        #self._create_certs()
        
        self.build_shell_string(container_id)


    def build_shell_string(self, container_id):
        self.shell_string = f'docker exec {container_id}'


        

    def run_ssh_command(self):

        # the host key contains a list of hosts
        for host in self.config['database_config']['host']:

            # -o options, including connection timeout in seconds
            # -oStrictHostKeyChecking gets around any invalid root CAs
            # -tt force psueo tty (honestly can't remember why this is here, test without?)
            # -i private key (identity file)
            # -n don't pass standard input, so it doesnt wait for a password and cause the command to hang
            # -q supress warnings, -qq suppress fatal too!

            print(f'{color.HEADER}Connecting to: {self.ssh_user}@{host}{color.END}') 
            print(f'{color.HEADER}Running command:{color.END} nodetool status') 
            ssh = subprocess.Popen(['ssh',
                                        '-oConnectTimeout=1',
                                        '-oStrictHostKeyChecking=no',
                                        '-oBatchMode=yes',
                                        '-tt',
                                        f'{self.ssh_user}@{host}',
                                        '-i',
                                        f'{self.path_cert}',
                                        f'nodetool status'],
                                    stdin=subprocess.PIPE, 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE) 
            (stdout, stderr) = ssh.communicate()

            if stdout:
                print(f'{color.OKGREEN}{stdout.decode("utf-8").strip()}{color.END}')
                print(f'{color.HEADER}Connection closed{color.END}')
                return stdout.decode("utf-8").strip()
            else:
                print(f'{color.FAIL}{stderr.decode("utf-8").strip()}{color.END}')
                


    def _create_certs(self):

        out, err = Shell.run(f'ssh-keygen -b 2048 -t rsa -f "{self.path_cert}" -q -N ""')
        print(out)
        print(err)
        #Shell.run('ssh-keygen')