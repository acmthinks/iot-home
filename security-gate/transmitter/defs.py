'''
common functions
'''

import configparser

def set_local_path(script_name):
    '''setting the local path based on the script invoked by systemd or by local'''
    local_path = script_name.rsplit('/', 1)[0]
    if script_name == local_path:
        local_path = ""
    else:
        local_path = local_path + "/"
    return local_path

def get_config(path_name, config_name):
    '''getting the config file based on the local path'''
    # read configuration file
    config = configparser.ConfigParser()
    if not path_name:
        config.read(config_name)
    else:
        config.read(path_name + config_name)
    return config