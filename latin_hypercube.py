from numpy import arange
import math
import os
import sys
import random

if len(sys.argv) < 3:
    print("use: python latin_hypercube.py parameters points outfile [-e] [-s] [-nr]")
    print("parameters: file with parameter names, lower bounds, upper bounds")
    print("points: how many points are wanted")
    print("-e: add this flag for an exponential distribution (don't use 0 as a bound here)")
    print("-s: add this flag to exhaustively search along the first two parameters")
    print("    in the parameter file (points^2 files will be generated)")
    print("-nr: add this flag to not shuffle the output; the first file will have the")
    print("smallest values, and the last file will have the largest.")
    sys.exit(1)

infile = sys.argv[1]
#This could crash with bad input, but I don't care
numpoints = int(sys.argv[2])
outfile  = sys.argv[3]

exponential = False
square = False
nonrandom = False
if "-e" in sys.argv:
    exponential = True
if "-s" in sys.argv:
    square = True
if "-nr" in sys.argv:
    nonrandom = True

reader = open(infile)
names = []
nums = []
for line in reader.readlines():
    words = line.split()
    names.append(words[0])
    lower = 0
    upper = 0
    if exponential:
        lower = math.log(float(words[1]))
        upper = math.log(float(words[2]))
    else:
        lower = float(words[1])
        upper = float(words[2])
    numlist = arange(lower, upper + (upper - lower)/numpoints, (upper - lower)/(numpoints-1))
    if not square and not nonrandom:
        random.shuffle(numlist)
    nums.append(numlist.tolist())


i = 0
metawriter = open("run_" + outfile + ".sh", 'w')
listwriter = open(outfile + "_list.txt", 'w')
#The loop condition here will never be false if we're doing a square sampling,
#since that one never pops elements from the lists.  But that has its own break.
while len(nums[0]) > 0:
    outname = outfile + str(i) + ".txt"
    writer = open(outname, "w")
    writer.write("dirname=\""+str(i)+"\"\n")
    if not square:
        for j in range(len(names)):
            towrite = ""
            if exponential:
                towrite = str(math.exp(nums[j].pop()))
            else:
                towrite = str(nums[j].pop())
            writer.write(names[j] + "=" + towrite + "\n")
    else:
        if exponential:
            writer.write(names[0] + "=" + str(math.exp(nums[0][i%numpoints])) + "\n")
            writer.write(names[1] + "=" + str(math.exp(nums[1][int(i/numpoints)])) + "\n")
        else:
            writer.write(names[0] + "=" + str(nums[0][i%numpoints]) + "\n")
            writer.write(names[1] + "=" + str(nums[1][int(i/numpoints)]) + "\n")
    writer.close()
    metawriter.write("python p21_sim.py " + outname + "\n")
    listwriter.write(outname + "\n")
    i += 1
    if i == numpoints**2 and square:
        break
metawriter.close()
