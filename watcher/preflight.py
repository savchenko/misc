import sys, os, ConfigParser
from sys import platform as platform

def System():
    """
    Check if we are running on Windows
    """
    if platform == "linux" or platform == "linux2":
        sys.exit("! Currently only supported on Windows :(\n")
    elif platform == "darwin":
        sys.exit("! Currently only supported on Windows :(\n")
    elif platform == "win32":
        print "> Windows detected."

def Storage():
    """
    Checking for config storage and create if necessary
    """
    directory = "./.config"
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.isfile(directory + "/wtConfig.ini"):
        app = QtGui.QApplication(sys.argv)
        window = noConfigWindow()
        print "! No config found. Exiting."
        sys.exit(app.exec_())
    else:
        pass

def configParser(DIR, SET):
    """
    :param DIR: [directory] in .ini file
    :param SET: setting = value within [directory]
    """
    config = ConfigParser.RawConfigParser()
    config.read("./pmConfig.ini")
    return config.get(str(DIR), str(SET))
