#!/usr/bin/env python3

import os
import logging
from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_config(profile='default', required_options=[]):
    """Load a Falcon sandbox configuration. Configuration files are user specific::
        ~/<current-user>/.config/falcon.ini
    :param str profile: (optional) Specifiy a group or company to work with.
    """
    logger = logging.getLogger(__name__+".load_config")
    config = ConfigParser()
    config_paths = []
    # user specific
    config_paths.append(os.path.join(os.path.expanduser("~"),'.config','falcon.ini'))
    finds = []
    for cp in config_paths:
        if os.path.exists(cp):
            logger.debug("Found config file at {}.".format(cp))
            finds.append(cp)
    if not finds:
        logger.critical("Didn't find any config files defined at these paths: {}".format(config_paths))
        return None

    config.read(finds)
    try:
        config[profile]
    except KeyError:
        logger.critical("No section named '{}' in configuration files : {}".format(profile, config_paths))
        return False

    for op in required_options:
        if not config.has_option(profile, op):
            logger.error("Configuation missing required options: {}".format(op))
            return False
        elif not config[profile][op]:
            logger.error("Configuration option missing value: {}".format(op))
            return False

    return config[profile]

def create_user_config(client_id, client_secret, ignore_proxy):
    """Creates a minimal configuration for the user.
    """
    config = ConfigParser()
    # user specific
    config_path = os.path.join(os.path.expanduser("~"),'.config','falcon.ini')
    config['default'] = {'client_id': client_id,
                         'client_secret': client_secret,
                         'ignore_proxy': ignore_proxy}
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    logging.info("Wrote user configuration to: {}".format(config_path))
    return