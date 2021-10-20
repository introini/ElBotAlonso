import yaml
from pathlib import Path
import logging

def loadConf():
    """
    Returns dict

    Loads yaml config file
    """
    configPath = Path('./config.yml').resolve()
    config = yaml.safe_load(open(configPath, 'r'))

    return config

def logger():
    conf = loadConf()

    log_level = conf['log_level'].upper()
    level = {'INFO': logging.INFO, 
    'WARNING': logging.WARNING, 
    'DEBUG': logging.DEBUG, 
    'ERROR': logging.ERROR }

    logging.basicConfig(filename=conf['log_file'], level=level[log_level])
    return logging.getLogger()
