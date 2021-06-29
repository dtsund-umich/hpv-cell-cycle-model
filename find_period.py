#Search the outputs of p21_sim, seeing if any of them exhibit periodicity
#Cruder than periodic_search; no Fourier transforms here, just local max search

import numpy
from glob import glob
import os
import sys

all_periods = []

def main(arg):
    directories = glob("*/")
    threshold = 0.1

    #New feature: Pass in an argument to check only one directory!
    #Return code is period (rounded down) for periodicity, 0 otherwise.
    #Newer feature: Pass the -periodic_only argument to only print the names
    #of periodic directories.
    checking_one = False
    periodic_only = False
    if arg != "":
        if arg == "-periodic_only":
            periodic_only = True
        else:
            directories = [arg]
            checking_one = True

    for d in directories:
        all_zeroes = True
        periodicity = False
        periodic_file = ""
        period = 0
        one_diverges = False
        if d == "./.git":
            continue
        os.chdir(d)
        bad = False
        for f in glob("*"):
            if "scaled" in f or ".ps" in f:
                continue
            if f != "Mb.txt":
                continue
            try:
                reader = open(f, 'r')
                lines = reader.readlines()
                halfway  = int(len(lines) / 2)
                stepsize = float(lines[0].split()[0].strip()) - float(lines[1].split()[0].strip())
                data = []
                if lines[-1].split()[1].strip() == "nan":
                    if checking_one:
                        return 0
                    if not periodic_only:
                        print("Failure to converge found in trial " + d)
                    bad = True
                    break
                if lines[-1].split()[1].strip() != "0.0":
                    all_zeroes = False
                for line in lines[halfway:]:
                    data.append(float(line.split()[1].strip()))
                maxima = []
                divergent = True
                for i in range(len(data)):
                    if i > 0 and i < len(data) - 1:
                        if data[i] < data[i+1]:
                            divergent = False
                        if data[i] > data[i-1] and data[i] > data[i+1]:
                            maxima.append(i)
                if divergent:
                    one_diverges = True
                if max(data) > 0.00000001 and (min(data) <= 0 or max(data)/min(data) > 1.002) and len(maxima) > 2:
                    periodicity = True
                    periodic_file = f
                    period = str((maxima[0] - maxima[1]) * stepsize)
                    if checking_one:
                        return int(float(period))
                    bad = True
                    break
            except IndexError:
                bad = True
                if checking_one:
                    return 0
                if not periodic_only:
                    print("ERROR found in trial " + d)
        if periodicity:
            if periodic_only:
                print(d.strip("/"))
            elif one_diverges:
                print("Periodivergence in trial " + d + ", periodic file " + periodic_file + ", period = " + period)
                all_periods.append(float(period))
            else:
                print("Periodic behavior found in trial " + d + ", file " + periodic_file + ", period = " + period)
                all_periods.append(float(period))
        elif not bad:
            if checking_one:
                return 0
            if all_zeroes and not periodic_only:
                print("Error or zero-convergence in trial " + d)
            elif one_diverges and not periodic_only:
                print("Divergence in trial " + d)
            elif not periodic_only:
                print("Steady-state behavior found in trial " + d)
        os.chdir("..")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(main(sys.argv[1]))
    else:
        main("")
    print("Mean period: " + str(numpy.mean(all_periods)))
    print("Variance: " + str(numpy.var(all_periods)))
