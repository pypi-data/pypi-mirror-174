from CoegilSdk import Coegil
from pathlib import Path
from typing import Dict
import json
import os


def get_sdk() -> Coegil:
    config = _get_configuration()
    return Coegil(config['apiKey'], instance_name=config['environment'], auto_validate=False)


def get_environment(config: Dict = None) -> str:
    config = _get_configuration() if config is None else config
    return config['environment']


def set_configuration(environment: str, api_key: str):
    file_name = _get_config_file_name()
    with open(file_name, "w") as f:
        payload = json.dumps({
            'apiKey': api_key,
            'environment': environment
        })
        f.write(payload)


def _get_configuration() -> Dict:
    file_name = _get_config_file_name()
    with open(file_name, "r") as f:
        return json.loads(f.read())


def _get_config_file_name() -> str:
    directory = os.path.join(str(Path.home()), '.coegil')
    Path(directory).mkdir(parents=True, exist_ok=True)
    return os.path.join(directory, 'credentials')
