import json

CONFIG_FILE = "config.json"

def load_config(key, default_value):
    try:
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            return config.get(key, default_value)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_value

def save_config(key, value):
    config = {}
    try:
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    config[key] = value
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)