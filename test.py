from view.ns_server import *
from module.base import base
from flask import jsonify
import sys, importlib
from pydoc import locate

args = sys.argv[1:]

b = importlib.import_module(f'view.{args[0]}')
print(f'Loaded "{args[0]}"...')
print(f'Calling "{args[1]}"...')


my_class = locate(f'view.{args[0]}')

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
        res = my_instance.get()

        if isinstance(res, str):
            print(res)
        else:
            print(res.data)