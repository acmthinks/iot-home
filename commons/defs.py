#common functions
import configparser

def setLocalPath(scriptName):
    #set localPath and accommodate invocation by systemd or by local
    print ("Running: " + scriptName)
    localPath = scriptName.rsplit('/', 1)[0]
    if scriptName == localPath: 
        localPath = ""
    else:
        localPath = localPath + "/"
    print ("localPath: " + localPath)
    return localPath

def getConfig(pathName, configName):
    # read configuration file
    config = configparser.ConfigParser()
    if not pathName:
        config.read(configName)
    else:
        config.read(pathName + configName)
    return config