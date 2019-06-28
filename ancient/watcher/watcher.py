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

from time import gmtime, strftime
import re, sys, os, time
import preflight

def watch_folder(folder):
    for root, dirs, files in os.walk(folder):
        return files
def timer_func(sec):
    time.sleep(sec)
    print '\nTimer done in', sec, 'seconds.'
    return None
def cTime():
    return time.strftime("%Y-%m-%d %H:%M", gmtime())

# Running checks
preflight.System()
preflight.Storage()

while True:
    timer_func(int(preflight.configParser('watcher', 'timerResolution')))
    def check_content(in_folder):
        wf = watch_folder(in_folder)
        wo = []
        for x in wf:
            pt = re.search('.exr', x)
            if pt:
                wo.append(x)
        if wo:
            print '\n', cTime(), '@ Found:', wo[:1], '\n'
            return wo
        else:
            print cTime(), ' @  Nothing found.\n'
            return None

    djvConverter = str(preflight.configParser('watcher', 'djvConverter'))
    path = str(preflight.configParser('watcher', 'path'))
    to_parse = check_content(path)
    clipLength = len(to_parse)-1

    if to_parse:
        def out_parser(parse):
            return '\n'.join(to_parse)
        def out_writer(outPath, outContent):
            file = open(outPath, 'a')
            wTime = '\n\n------------------------ ' + str(cTime()) + '\n'
            file.write(str(wTime))
            file.write(outContent)
        def encode():
            for x in to_parse:
                xN = x.split('.')[:1]
                xExt = x.split('.')[1:]
                xExtStr = "".join(xExt)
                for element in xN:
                    liPreOut = []
                    liPreOut.append(element)
                    for cName in liPreOut:
                        cNameS = []
                        cNameS = cName.split('_')[:1]
                        cNameCount = cName.split('_')[1:]
                        cNameCountS = "".join(cNameCount)
                        cNameCountNum = str(len(cNameCountS))
                        cNameS = ''.join(cNameS) + '_%0' + cNameCountNum + 'd' + '.' + xExtStr
                        cName = cName.split('_')[:1]
                        cName = ''.join(cName)
                        outFFmpeg = 'djv_convert', cNameS, cName + '.mov'
                        # -------- Ready for launch ---------
                        outFile = path + cName + '.mov'
                        outDjv = djvConverter + path + '\\' + element + '-0' + str(clipLength) + '.' + xExtStr + ' ' + path + '\\' + cName + '.mov'
                        return (outDjv, outFile)
    else:
        sys.exit()
    if os.path.isfile("".join(encode()[1:])) != True:
        djvOut = os.popen("".join(encode()[:1])).read()
        print djvOut
        out_writer(str(preflight.configParser('watcher', 'logPath'))', out_parser(to_parse))
    else:
        print 'File already exist.'
