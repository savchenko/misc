#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Andrew Savchenko (c) MIT
# andrew@savchenko.net

import os
import argparse
from datetime import date
from hashlib import sha1
from shutil import rmtree
from shutil import copy2 as copy
from itertools import combinations

parser = argparse.ArgumentParser(description='Creates random data to test de-duplication')
parser.add_argument('--files_number', '-f', help='Number of unique files to create')
parser.add_argument('--bytes', '-b', default=131072, help="Size of each file in bytes")
parser.add_argument('--debug', '-d', default=False, help="Print file hashes to the stdout")
args = parser.parse_args()

if args.files_number and args.bytes:
    unique_files = int(args.files_number)
    f_size = int(args.bytes)
    assert (f_size > 1), "Testing makes sense if files are larger than 1 byte"
    assert (unique_files > 3), "Testing makes sense with --files_number >= 4"
else:
    parser.exit(1, parser.print_help())

out_path = "%s/dup_test_%s" % (os.getcwd(), date.today().isoformat())

if os.path.isdir(out_path):
    rmtree(path=out_path, ignore_errors=False)

os.makedirs(out_path)

files = []

if args.debug:
    print "\nHashes:"

for f in range(0, unique_files):
    f_name = "%s/uniq_%s" % (out_path, f)
    with open(f_name, "w+") as f_obj:
        rand = os.urandom(f_size)
        if args.debug:
            print "%s %s" % (f, sha1(rand).hexdigest())
        f_obj.write(rand)
        f_obj.close()
    files.append(f_obj)

files_per_subdir = len(files)/2
file_combinations = combinations(files, files_per_subdir)
total_files = (len([x for x in file_combinations])*files_per_subdir)+unique_files

for num, combo in enumerate(combinations(files, files_per_subdir)):
    sub_path = "%s/sub_%s" % (out_path, num)
    os.makedirs(sub_path)
    for f_obj in combo:
        copy(f_obj.name, "%s/%s" % (sub_path, os.path.basename(f_obj.name)))

print "\nTotal files: %s\nTotal size: %sKb\n" % (total_files, total_files*f_size/1024)
