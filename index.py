import subprocess
from module.nodetool import nodetool

nodetool = nodetool()

token_list = []

fileOutput = 'output'

stdout, stderr = nodetool.status()
print(stderr)
for line in stdout.split("\n"): 
    print(f'Line: {line}')

    for col in line.split(" "):
        if (col == ''):
            continue
        print(f'Col: {col}')

