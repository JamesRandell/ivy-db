import subprocess
import datetime
import time
import requests
import json
from requests.structures import CaseInsensitiveDict
from module.nodetool import nodetool

nodetool = nodetool()


url = "http://localhost:8888/db/cassandra"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"



def sendData():
    out, err = nodetool.info()
    
    try:
        res = requests.post(url, headers=headers, data=json.dumps(out))
        print(res.status_code)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        #raise SystemExit(e)
    




import sched
s = sched.scheduler(time.time, time.sleep)
def test():
    out, err = nodetool.info()
    print(f'{time.time()}: {out}')
    s.enter(2, 1, test)
    s.run()
#test()

count = 0

while True:
    count += 1
    unixtime = datetime.datetime.now().timestamp()
    sendData()
    print(f'{count}: {unixtime}')
    time.sleep(10)



print(err)
print(out)





