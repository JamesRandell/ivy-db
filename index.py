import subprocess
import datetime
import time
import requests
from requests.structures import CaseInsensitiveDict
from module.nodetool import nodetool

nodetool = nodetool()


url = "http://localhost:8888"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = '{"login":"my_login","password":"my_password"}'



def sendData():
    out, err = nodetool.info()
    resp = requests.post(url, headers=headers, data=out)
    print(resp.status_code)




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





