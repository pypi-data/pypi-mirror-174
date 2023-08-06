from ruamel.yaml import YAML

from . import options

yaml = YAML(typ='rt')

config_data = None

def load():
    global config_data
    config_path = options.atopile_file.value
    if config_data is None:
        try: 
            with config_path.open() as f:
                config_data = yaml.load(f)
        except FileNotFoundError:
            config_data = {}

    return config_data

def save():
    global config_data
    config_path = options.atopile_file.value
    with config_path.open('w') as f:
        yaml.dump(config_data, f)
