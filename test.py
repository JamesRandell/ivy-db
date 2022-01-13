from view.ns_server import *
from module.base import base
from flask import jsonify, request
import sys, importlib
from pydoc import locate

args = sys.argv[1:]

b = importlib.import_module(f'view.{args[0]}')
print(f'Loaded "{args[0]}"...')
print(f'Calling "{args[1]}"...')


my_class = locate(f'view.{args[0]}')


def parse_post_option(post_string):
    """
    this doesnt work
    :post_string: a comma delimited list of key=value pairs
    """
    for pair in post_string.split(","):
        key, value = pair.split("=")


# create an application context for testing. We do this so we 
# can continue to use jsonify in our code. As jsonfiy is part of 
# flask, we sort of need to instqnce or pass the application 
# context along to use it
# https://testdriven.io/blog/flask-contexts/ for more
app = Flask(__name__) 
with app.app_context():
    if (args[0]):
        my_class = getattr(my_class, args[1])
        my_instance = my_class()

        # urgh, ok this test is getting a little more complex.
        # i'm adding in POST support! This is a bad idea
        # I'm going to loop throug the args and check for an -POST key
        i = 0
        for arg in args:
            

            # if found, convert the next argument to key=value
            if (arg == 'POST'):

                if (args[i+1]):
                    # wrap this bit into a function as it's a little complex
                    parse_post_option(args[i+1])
                else:
                    pass

            i = i+1

        args_string = ' '.join(args[2:])


        res, HTTP_status = my_instance.get(args_string)

        if isinstance(res, str):
            print(res)
        elif('data' in res):
            print(res.data)
        else:
            print(res)

        print(HTTP_status)