import configparser

config_file = "yant.cfg"
config = configparser.ConfigParser()
config.read(config_file)


def get(section, option):
    return config[section][option]


def set(section, option, value):
    if section not in config:
        config[section] = {}
    config[section][option] = value
    with open(config_file, "w") as cf:
        config.write(cf)
