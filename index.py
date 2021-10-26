import subprocess

var = 'docker container list | awk \'{if ($(2) == "cassandra:latest") {print $1}}\''


process = subprocess.Popen(['echo', 'More output'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
stdout, stderr




#sts = subprocess.Popen([var], shell=True).wait()
sts = subprocess.run(var)
print(sts)

#import os
#os.system('docker container list | awk \'{if ($(2) == "cassandra:latest") {print $1}}\'')

