import subprocess
import datetime
unixtime = datetime.datetime.now().timestamp()

from module.nodetool import nodetool






nodetool = nodetool()

token_list = []

fileOutput = 'output'

out, err = nodetool.info()
print(err)
print(out)

