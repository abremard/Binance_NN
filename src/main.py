import test as test
import os
import subprocess
import sys
import datetime
import logging

# log retention
pspath = os.path.abspath("log-retention.ps1")
logpath = os.path.abspath("..\log")
p = subprocess.Popen(["powershell.exe", 
              pspath, logpath], 
              stdout=sys.stdout)
p.communicate()

# log config
logDay = datetime.datetime.now().strftime('%d-%m-%Y')
logging.basicConfig(filename='../log/'+logDay+'.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',  datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

# main
test.test()