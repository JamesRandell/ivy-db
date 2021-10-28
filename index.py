import subprocess

from module.nodetool import nodetool






nodetool = nodetool()

token_list = []

fileOutput = 'output'

out, err = nodetool.info()
print(err)





print(out)

