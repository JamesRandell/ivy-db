from distutils.log import error
import errno
from sre_compile import isstring
import yaml, importlib
from module.connectors import *

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
    
class Connection:

    config_fullpath = "config.yml"
    conn = object
    config = object
    connection_class = object

    def __init__(self):
        config = self._load_config()

        # now lets call a class that matches the config
        if 'database_env' not in config:
            exit(f"{color.FAIL}Config: error - 'database_env' is missing{color.END}") 
        
        print(f"{color.OKCYAN}Config: using config setings for {color.BOLD}'{config['database_env']}'{color.END}")

        try:
            self.connection_class = importlib.import_module(f"module.connectors.{config['database_env']}")
        except:
            exit(f"{color.FAIL}Connection: could not find a connection module called '{config['database_env']}'{color.END}")
        

        #my_class = locate(f"module.connection.{config['database_env']}")

        self.config = self._parse_config(config)


        
        self.db_env = '' # filed in from config


        
    

    def run(self, command):
        """
        Attempts to run a command against the database

        :param input: the cqlsh result to parse and format
        :return: the result of the command on the shell
        """
        c = self.connection_class.Conn(self.config) 
        
        return c.run(command), 'h'

    def _load_config(self):

        result = {}

        print(f"{color.HEADER}Config: attempting to load config file...'{color.END}")

        # LOAD the config file
        try:
            f = open(self.config_fullpath, "r")
            
        except IOError:
            print(f"{color.FAIL}Config: could not load '{self.config_fullpath}' file{color.END}")
            exit()
        else:
            with f:
                print(f"{color.OKCYAN}Config: config file loaded...'{color.END}")
                result = f.read()
        
        # PARSE the config file. Accepts yaml only
        try:
            result = yaml.safe_load(result)
        except:
            print(f"{color.FAIL}Config: could not parse yaml file. Tried to run yaml.safe_load{color.END}")
            exit()
        
        print(f"{color.OKCYAN}Config: yaml file parsed...'{color.END}")
        return result


    def _parse_config(self, config):
        # future method to make sure certain config keys exist like host and env

        # make sure there's a 'host' in there some where
        if 'host' not in config['database_config']:
            print(f"{color.FAIL}Config: no 'host' list found in the config file{color.END}")
            exit()
        
        host = config['database_config']['host']

        # ok, so we know it exists, we're going to see if it's a string or a list. If it's a string, convert it to a list with 1 item
        if isstring(host):
            temp_list = []
            temp_list.append(host)

            config['database_config']['host'] = temp_list
        
        print(f"{color.OKCYAN}Config: using the following hosts: {config['database_config']['host']}{color.END}")
        return config