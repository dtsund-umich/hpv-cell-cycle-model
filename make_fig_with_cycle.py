import os
import sys
import subprocess
import bisect

if len(sys.argv) < 2:
    print("Try that again but with an argument next time.")
    sys.exit(1)

#Autocomplete might give us a slash in the directory name; this leads
#to confusing behavior if we don't strip it out.
model = sys.argv[1].split("/")[0]


#Step 1: Generate original figure using a command line call to gracebat
gracecommand = "gracebat " + model + "/Me.txt " + model + "/Ma.txt " + model + "/Mb.txt -param easy-params-leftbox.agr -printfile temp.ps"
subprocess.call(gracecommand.split())
subprocess.call(("convert -rotate 90 temp.ps " + model + "_cycle_fixbox.png").split())
subprocess.call("rm temp.ps".split())
image = model + "_cycle_fixbox.png"

#Step 2: Load Cdc20a, p27, and Ma to determine phase transition points

#G1/S-G2 transition: peak p27?
#S-G2/G2-M transition: peak Ma?
#G2-M/G1 transition: peak Cdc20a?

p27lines = open(model+"/p27.txt").readlines()
malines = open(model+"/Ma.txt").readlines()
cdc20alines = open(model+"/Cdc20a.txt").readlines()

#For now, I will assume one peak per cycle.
#This will break in very visible ways if the assumption doesn't hold, and I'll go back and fix it then if it ever comes up.
g1_sg2_trans = []
sg2_g2m_trans = []
g2m_g1_trans = []

#Minor assumption: all three loaded files are the same length.  If this doesn't hold, something is very seriously wrong...
for i in range(1,len(p27lines)-1):
    if float(p27lines[i].split()[1]) > float(p27lines[i-1].split()[1]) and float(p27lines[i].split()[1]) > float(p27lines[i+1].split()[1]):
        g1_sg2_trans.append(float(p27lines[i].split()[0]))
    if float(malines[i].split()[1]) > float(malines[i-1].split()[1]) and float(malines[i].split()[1]) > float(malines[i+1].split()[1]):
        sg2_g2m_trans.append(float(malines[i].split()[0]))
    if float(cdc20alines[i].split()[1]) > float(cdc20alines[i-1].split()[1]) and float(cdc20alines[i].split()[1]) > float(cdc20alines[i+1].split()[1]):
        g2m_g1_trans.append(float(cdc20alines[i].split()[0]))


#X-range for rectangle: 92 up to 704
#Y-range: let's try 60 to 90 for starters



#Step 3: Use imagemagick to mangle original image into finalized image
transtime = g1_sg2_trans[bisect.bisect(g1_sg2_trans, 400)-1]
curphase = "sg2"
if sg2_g2m_trans[bisect.bisect(sg2_g2m_trans, 400)-1] > transtime:
    curphase = "g2m"
    transtime = sg2_g2m_trans[bisect.bisect(sg2_g2m_trans, 400)-1]
if g2m_g1_trans[bisect.bisect(g2m_g1_trans, 400)-1] > transtime:
    curphase = "g1"
    transtime = g2m_g1_trans[bisect.bisect(g2m_g1_trans, 400)-1]

transtime = 400

while True:
    if curphase == "sg2":
        newindex = bisect.bisect(sg2_g2m_trans,transtime)
        endpoint = 0
        if newindex == len(sg2_g2m_trans):
            endpoint = 500
        else:
            endpoint = sg2_g2m_trans[newindex]
        #draw rectangle
        xstart = str((transtime - 400) * 6.13 + 91)
        xend = str((endpoint - 400) * 6.13 + 91)
        command = "convert " + image + " -fill DarkSlateGray2 -stroke black -draw \'rectangle " + xstart + " 60 " + xend + " 90\' " + image
        os.system(command)
        if endpoint == 500:
            break
        transtime = endpoint
        curphase = "g2m"


    elif curphase == "g2m":
        newindex = bisect.bisect(g2m_g1_trans,transtime)
        endpoint = 0
        if newindex == len(g2m_g1_trans):
            endpoint = 500
        else:
            endpoint = g2m_g1_trans[newindex]
        #draw rectangle
        xstart = str((transtime - 400) * 6.13 + 91)
        xend = str((endpoint - 400) * 6.13 + 91)
        command = "convert " + image + " -fill firebrick3 -stroke black -draw \'rectangle " + xstart + " 60 " + xend + " 90\' " + image
        os.system(command)
        if endpoint == 500:
            break
        transtime = endpoint
        curphase = "g1"


    elif curphase == "g1":
        newindex = bisect.bisect(g1_sg2_trans,transtime)
        endpoint = 0
        if newindex == len(g1_sg2_trans):
            endpoint = 500
        else:
            endpoint = g1_sg2_trans[newindex]
        #draw rectangle
        xstart = str((transtime - 400) * 6.13 + 91)
        xend = str((endpoint - 400) * 6.13 + 91)
        command = "convert " + image + " -fill LightGoldenrod -stroke black -draw \'rectangle " + xstart + " 60 " + xend + " 90\' " + image
        os.system(command)
        if endpoint == 500:
            break
        transtime = endpoint
        curphase = "sg2"

    else:
        print("FLAGRANT ERROR")
        break


