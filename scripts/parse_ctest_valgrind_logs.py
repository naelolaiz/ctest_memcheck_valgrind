#!/bin/env python
import subprocess
import re
import glob
import os
import sys

directory_of_test_logs = None
if len(sys.argv)>1 : 
    directory_of_test_logs = sys.argv[1]

output=subprocess.check_output(["ctest","-N"]).split(b"\n")
tests = {}
for line in output:
    line = line.decode("utf-8")
    match = re.search(".*Test #([0-9]+): (.*)$", line)
    if match:
        testNr, testName = match.groups()
        testNr = int(testNr)
        tests[testNr] = testName

if directory_of_test_logs:
    files = glob.glob(os.path.join(directory_of_test_logs,"MemoryChecker.*.log"))

    for file in files:
        hasErrors = re.search("ERROR SUMMARY: 0 errors",open(file).readlines()[-1]) == None
        baseFilename = os.path.basename(file)
        match = re.search("MemoryChecker.([0-9]+).log", baseFilename)
        if not match:
            raise Exception("error on filename {}".format(baseFilename))
        print (baseFilename, "->", "MemoryChecker.{}.log".format(tests[int(match.groups()[0])]))
        print(str(hasErrors))
