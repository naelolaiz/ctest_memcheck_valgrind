#!/bin/env python
import subprocess
import re
import glob
import os
import sys
import shutil

# returns a dictionary {test_number: test_name,...}
def get_ctests_list(build_dir):
    cwd = os.getcwd()
    os.chdir(build_dir)
    output=subprocess.check_output(["ctest","-N"]).split(b"\n")
    tests = {}
    for line in output:
        line = line.decode("utf-8")
        match = re.search(".*Test #([0-9]+): (.*)$", line)
        if match:
            testNr, testName = match.groups()
            testNr = int(testNr)
            tests[testNr] = testName
    return tests

def rename_and_copy_failed_memcheck_log_files(tests, memcheck_logs_dir, output_dir):
    files = glob.glob(os.path.join(memcheck_logs_dir, "MemoryChecker.*.log"))

    for file in files:
        hasErrors = re.search("ERROR SUMMARY: 0 errors",open(file).readlines()[-1]) == None
        match = re.search("MemoryChecker.([0-9]+).log", file)
        if not match:
            raise Exception("error on filename {}".format(file))
        if hasErrors:
            output_file = os.path.join(output_dir, "MemoryChecker.{}.log".format(tests[int(match.groups()[0])]))
            print ("Valgrind issues found on {}. Moving it to {}".format(file, output_file))
            shutil.copyfile(file, output_file)
        else:
            print("test {} has no errors".format(file))

if __name__ == "__main__":
    if len(sys.argv) < 3: 
        print("usage: {} <build dir> <output dir>".format(os.path.basename(sys.argv[0])))
        sys.exit(-1)
     
    build_dir = sys.argv[1]
    memcheck_logs_dir = os.path.join(build_dir, "Testing", "Temporary")
    output_dir = sys.argv[2]

    list_of_tests = get_ctests_list(build_dir)
    rename_and_copy_failed_memcheck_log_files(list_of_tests, memcheck_logs_dir, output_dir)

