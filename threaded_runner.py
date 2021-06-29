import sys
import subprocess
import time

if len(sys.argv) < 3:
    print("Use: python threaded_runner file_list.txt cores [extra.txt]")
    print("file_list.txt: The list of parameter files to be used in p21_sim")
    print("cores: The number of cores to be used at once.")
    print("extra.txt: An additional parameter file to be used in every run.")

files = open(sys.argv[1], 'r').readlines()
num_procs = int(sys.argv[2])

extra = ""
if len(sys.argv) >= 4:
    extra = sys.argv[3]

proclist = []
#Will terminate any subprocess that runs for more than a minute.
#Solver occasionally hangs.
timelist = [0]*num_procs
for i in range(num_procs):
    proclist.append(None)

cur_process = 0
last_started = 0

for f in files:
    while True:
        if timelist[cur_process] == 60:
            proclist[cur_process].kill()
        if proclist[cur_process] == None or proclist[cur_process].poll() != None:
            proclist[cur_process] = subprocess.Popen("python goldbeter_full_ink4_p53.py " + f + " " + extra, shell="True")
            timelist[cur_process] = 0
            last_started = cur_process
            cur_process += 1
            cur_process = cur_process % num_procs
            break
        timelist[cur_process] += 1
        cur_process += 1
        cur_process = cur_process % num_procs
        if cur_process == last_started:
            time.sleep(1)

#Don't actually terminate *this* process until all subprocesses are done.
#Important for some things that call this and depend on this having entirely
#finished.
for proc in proclist:
    proc.wait()
