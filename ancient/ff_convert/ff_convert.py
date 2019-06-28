# -*- coding: utf-8 -*-
# --------------------------------------------------------------
#
# Andrew Savchenko © 2012
# art@artaman.net
#
# Attribution 4.0 International (CC BY 4.0)
# http://creativecommons.org/licenses/by/4.0/
#
# --------------------------------------------------------------

import os
import sys

convert_path = str(sys.argv[1:]).strip("[']")
files_to_process_full = []
files_to_process = []
filetypes = (".mov", ".mp4", ".avi", ".qt", ".mpg", ".mpeg")

if os.path.isdir(convert_path):
        for name in os.listdir(convert_path):
            if os.path.isfile(os.path.join(convert_path, name)):
                if name.endswith(filetypes):
                    files_to_process_full.append(os.path.join(convert_path, name))
                    name_without_extension = str(name.split(".")[:1]).strip("[']")
                    files_to_process.append(name_without_extension)
                else:
                    print "\n" + name + " has wrong extension."
elif convert_path == "":
    sys.exit("\nUsage:\n"
             "\tff_convert /path/to/videos\n")
else:
    sys.exit("\nSupplied argument is not a valid directory\n")

def createJpgs():
    """
    Create directories with _jpg ending
    Pass files from "convert_path" to ffmpeg
    """
    for filename_full in files_to_process_full:
        filename_index = files_to_process_full.index(filename_full)+1  # Done for humans
        filename = files_to_process[filename_index-1]
        newDir_name = str(filename_full.split(".")[:1]).strip("[']")
        newDir = newDir_name + "_jpg"
        print "\n------- File #" + str(filename_index) + " -------\n"
        if os.path.isdir(newDir):
            print filename + "_jpg already exist."
        else:
            os.system("mkdir " + newDir)
            os.system("ffmpeg -loglevel warning -stats -i "
                      + filename_full + " -q 2 " + newDir + "/" + filename + "_%d.jpg" + "&& printf '\n'")
createJpgs()