import subprocess
import datetime
import time
from urllib.request import Request, urlopen
from urllib.error import URLError
import json
from module.nodetool import nodetool

nodetool = nodetool()


url = "http://localhost:8888/db/cassandra"


def sendData():
    out, err = nodetool.status()
    
    try:
        req = Request(url, data=json.dumps(out).encode())
        req.add_header('Content-Type', 'application/json')
        #res = requests.post(url, headers=headers, data=json.dumps(out))
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach the server: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request: Error code: ', e.code)

    #except requests.exceptions.RequestException as e:  # This is the correct syntax
    #    print(e) 
        #raise SystemExit(e)
    




import sched
s = sched.scheduler(time.time, time.sleep)
def test():
    out, err = nodetool.info()
    #print(f'{time.time()}: {out}')
    s.enter(2, 1, test)
    s.run()
#test()

count = 0

while True:
    count += 1
    unixtime = datetime.datetime.now().timestamp()
    #sendData()
    #print(f'{count}: {unixtime}')
    
    time.sleep(5)



print(err)
print(out)





