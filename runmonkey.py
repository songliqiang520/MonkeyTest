# -*- coding: utf-8 -*-

import time, os

# execute times
execcount = 2
# execute interval, (seconds)
execinterval = 1 * 5

monkeyclickcount = 1000

WORKSPACE = os.path.abspath(".")

def getWorkConfig():
    f = open("./.config", "r")
    config = {"monkeyclickcount": monkeyclickcount, "execcount": execcount}
    try:
        while True:
            line = f.readline()
            if line:
                line = line.strip()
                linesplit = line.split("：")
                if linesplit.__sizeof__() > 1:
                    if linesplit[0] == 'phone':
                        config['phone'] = linesplit[1]
                    elif linesplit[0] == 'monkeyclickcount':
                        config["monkeyclickcount"] = linesplit[1]
                    elif linesplit[0] == 'execcount':
                        config["execcount"] = linesplit[1]
            else:
                break
    finally:
        f.close()
        print "config : %s" % config
        return config

def installApk(config):
    phoneAddr = config.get("phone")
    print 'Ready to start installing apk'

    if phoneAddr:
        installPhoneApk = "adb -s %s install -r %s\\apk\\app-inland-debug.apk" % (phoneAddr, WORKSPACE)
        os.popen(installPhoneApk)
        print "install phone apk done"


def killTestApp():
    forceStopApp = "adb -s %s shell am force-stop com.example.demo1" % workConfig.get('phone')
    os.popen(forceStopApp)

def fullmonkey(workconfig):
    killTestApp()

    monkeycmd = "adb -s %s shell monkey -p com.example.demo1 " \
                "--ignore-timeouts --ignore-crashes --kill-process-after-error " \
                "--pct-touch 35 --pct-syskeys 30 --pct-appswitch 35 --hprof  " \
                "--throttle 100 -v -v -v %s" \
                % (workconfig.get("phone"), workConfig.get("monkeyclickcount"))
    os.popen(monkeycmd)

def createBugreport():
    print "create bugreport file"
    bugreport = "adb -s %s shell bugreport > %s\\bugreport.txt" % (workConfig.get("phone"), WORKSPACE)
    os.popen(bugreport)

    print "create bugreport file ,done"

    chkbugreport = "java -jar %s\\chkbugreport.jar %s\\bugreport.txt" % (WORKSPACE, WORKSPACE)
    os.popen(chkbugreport)

workConfig = getWorkConfig()
installApk(workConfig)
forcount = int(workConfig.get("execcount"))


for i in range(forcount):
    print "execute monkey ,loop = %s" % (i + 1)
    fullmonkey(workConfig)
    time.sleep(execinterval)

createBugreport()

print "Completion of the current round of testing"
raw_input("Enter key to close")