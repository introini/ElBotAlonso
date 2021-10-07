import yaml
from pathlib import Path

def loadConf():
    """
    Returns dict

    Loads yaml config file
    """
    configPath = Path('./config.yml').resolve()
    config = yaml.safe_load(open(configPath, 'r'))

    return config