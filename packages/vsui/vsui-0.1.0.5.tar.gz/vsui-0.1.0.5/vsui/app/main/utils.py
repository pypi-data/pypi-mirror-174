import logging
import sys
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Union
import yaml
import json

def get_settings_data(data: Union[Path, dict, None]) -> SimpleNamespace:
    """Given a path to a YAML file or a dictionary object, returns a 
    simple namespace object holding settings data. If the data is None, 
    an empty namespace is returned.
    """
    if data is None:
        return SimpleNamespace()
    elif isinstance(data, Path):
        logging.info(f"Loading settings from {data}")
        if data.exists():
            with open(data, "r") as stream:
                settings_dict = yaml.safe_load(stream)
            return SimpleNamespace(**settings_dict)
        else:
            logging.error("Couldn't find settings file... Exiting!")
    elif isinstance(data, dict):
        return SimpleNamespace(**data)

def write_settings_data(data: SimpleNamespace, location: Union[Path, dict, None]) -> None:
    """Given a SimpleNamespace containing the information and a path to a YAML file,
    writes/overwrites the information to that file. If given Empty NameSpace reports an error
    Can also extract the dictionary of the simpleNamespace if for whatever reason you needed 
    it do do that"""
    print(f'writing to path {location}')
    # empty dictionaries evaluate to false
    if location is None:
        logging.error("no write location specified")
    elif isinstance(location, Path):
        print('writing')
        if not data.__dict__:
            logging.error("settings data empty")
        else:
            if not os.path.exists(location):
                head, tail = os.path.split(location)
                os.makedirs(head)
            with open(location, 'w') as file:
                export = yaml.dump(data.__dict__, file)
    elif isinstance(location, dict):
        return data.__dict__

def read_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f'no json file at {path}')

filetype_map = {
    True:'directory',
    False:'file-generic'
}
def explore(path):
    if os.path.isdir(path):
        try:
            return 'success', [{'path': f.path, 'dir': f.is_dir(), 'type': filetype_map[f.is_dir()]} for f in os.scandir(path)]
        except:
            # return information about the error encountered
            the_type, the_value, the_traceback = sys.exc_info()
            print([the_type, the_value, the_traceback])
            return str(the_value), False
    else:
        # if it wasn't a directory, explore the file's parent directory instead
        return explore(os.path.dirname(path))

def parse_args(args: SimpleNamespace):
    print(f'args: {args}')
    ''' take a simple namespace of arguments, turn each key into a flag and each value into its argument'''
    out = []
    for k, v in args.__dict__.items():
        out.append("--" + k)
        if isinstance(v, list):
            out.append(' '.join(v))
            print(out)
        elif isinstance(v, str):
            out.append(v)
        else:
            logging.error(f'flag --{k} was supplied an argument that was not a list or string')
    return out