'''
common functions
'''

import configparser

'''
setting the local path based on the script invoked
'''
def set_local_path(script_name):
    #set local path and accommodate invocation by systemd or by local
    print ("Running: " + script_name)
    local_path = script_name.rsplit('/', 1)[0]
    if script_name == local_path:
        local_path = ""
    else:
        local_path = local_path + "/"
    print ("local_path: " + local_path)
    return local_path

'''
getting the config file based on the local path
'''
def get_config(path_name, config_name):
    # read configuration file
    config = configparser.ConfigParser()
    if not path_name:
        config.read(config_name)
    else:
        config.read(path_name + config_name)
    return config
    