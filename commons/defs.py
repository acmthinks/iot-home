#common functions
import configparser

def setLocalPath():
    #set localPath and accommodate invocation by systemd or by local
    scriptName = sys.argv[0]
    print ("Running: " + scriptName)
    localPath = scriptName.rsplit('/', 1)[0]
    if scriptName == localPath: 
        localPath = ""
    else:
        localPath = localPath + "/"
    print ("localPath: " + localPath)
    return localPath

def getConfig(path, config):
    # read configuration file
    config = configparser.ConfigParser()
    config.read(path + config)
    return config