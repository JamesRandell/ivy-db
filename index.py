

var = 'docker container list | awk \'{if ($(2) == "cassandra:latest") {print $1}}\''

import subprocess
print("a")
process = subprocess.Popen(['echo', 'More output'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
stdout, stderr

print("b")


sts = subprocess.Popen(var).wait()


import os
os.system('docker container list | awk \'{if ($(2) == "cassandra:latest") {print $1}}\'')

print("c")