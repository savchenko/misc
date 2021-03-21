#!/usr/bin/env python
import argparse
import os, shutil

#
# TODO:
#   * Add detection of already processed images
#   * Folder watch
#

# -- Parser setup
parser = argparse.ArgumentParser(description="Creates proxy positive .JPGs from scanned negatives")
parser.add_argument("-src", help="Source directory with negatives, will process only TIFFs")
#  parser.add_argument("-dest", help="Where to put positive .jpeg")
args = parser.parse_args()

ramdisk = "/Volumes/ramdisk"
src_list = []

def check_ram_disk():
    """
    Checks ram-disk existence
    """
    if not os.path.isdir(ramdisk):
        return False
    else:
        return True


def collect_files(src_dir):
    """
    Collects *.TIFFs from the src_dir
    """
    if src_dir:
        if os.path.isdir(src_dir):
            for f in os.listdir(src_dir):
                if f.endswith(".tiff") or f.endswith(".tif"):
                    src_list.append(os.path.join(src_dir, f))


def copy_src_to_ramdisk(src):
    """
    Copies SRC to ramdisk
    """
    dest_ram = os.path.join(ramdisk, os.path.split(src)[1])
    try:
        shutil.copyfile(src, dest_ram)
    except:
        raise SystemError("Unable to copy %s to ramdisk") %src
    return dest_ram


def convert_neg_to_pos(f):
    """
    Runs ImageMagick script
    """
    converted = os.path.basename(f).split(".")[-2] + "_POS.jpeg"
    try:
        os.system("convert %s -resize 3000000@ %s" % (f, f))
        os.system("./negative2positive -l 0 -h 0 %s %s" % (f, f))
        os.system("./autolevel %s %s" % (f, os.path.join(ramdisk, converted)))
    except:
        raise SystemError("Unable to convert %s") % (f)
    return os.path.join(ramdisk, converted)


def main():
    """
    Main loop
    """
    if check_ram_disk():
        collect_files(args.src)
        if len(src_list) > 0:
            print "Collected %s TIFF images" % (len(src_list))
            positives_folder = os.path.join(args.src, "_Positives")
            if not os.path.isdir(positives_folder):
                os.makedirs(positives_folder)
                print "Created %s folder" % (positives_folder)
            for f in src_list:
                src_ramdisk = copy_src_to_ramdisk(f)
                pos_ramdisk = convert_neg_to_pos(src_ramdisk)
                pos_final_path = os.path.join(positives_folder, os.path.basename(pos_ramdisk))
                shutil.move(pos_ramdisk, pos_final_path)
                os.remove(src_ramdisk)
                print os.path.basename(f) + " processed"
    else:
        print "\nNo RAMDisk present, please make one 1st.\n"

main()
