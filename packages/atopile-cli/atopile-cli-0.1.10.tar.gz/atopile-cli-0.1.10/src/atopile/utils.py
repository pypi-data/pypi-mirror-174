import collections.abc
import logging
from hashlib import sha1
from pathlib import Path

import attrs

from . import options


project_logger: logging.Logger = logging.getLogger('atopile.project')


def add_obj_to_hash(obj, hash):
    if hasattr(obj, '__attrs_attrs__'):
        attrs_to_hash = [a.name for a in obj.__attrs_attrs__]
        values_to_hash = [attrs.asdict(obj)[k] for k in attrs_to_hash]
    elif isinstance(obj, dict):
        attrs_to_hash = list(obj.keys())
        values_to_hash = [obj[k] for k in attrs_to_hash]
    elif isinstance(obj, list):
        values_to_hash = obj
    else:
        values_to_hash = [str(obj)]

    for value in values_to_hash:
        if isinstance(value, str):
            hash.update(value.encode())
        else:
            add_obj_to_hash(value, hash)

def compute_object_hash(obj) -> str:
    hash = sha1()
    add_obj_to_hash(obj)
    return hash.hexdigest()

def add_file_to_hash(path: Path, hash):
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash.update(chunk)

def hash_file(path: Path) -> str:
    hash = sha1()
    add_file_to_hash(path, hash)
    return hash.hexdigest()
    

class AtopileError(Exception):
    """
    Represents something wrong with the data fed in
    """
    pass

def merge_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = merge_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def reindent_str(string: str, indent=0) -> str:
    indent = ' ' * indent
    reindented = indent + f'\n{indent}'.join([v.strip() for v in string.splitlines()])
    return reindented

def resolve_project_relative_ref(ref):
    """
    Figure out what the user means when they specify a reference to something within some project
    """
    # let's first assume this is an absolute path
    # if an absolute reference is provided, we're assuming it's in the project, obviously
    # in this case we should be able to say we can work out the project root based on it
    path = Path(ref).absolute()
    if path.exists():
        options.project_dir.set_value(path, options.Level.CLICK_OPTION)
        return path.relative_to(options.project_dir.value)

    # if it's not an absolute path, we're assuming it's a relative path with respect to the project root
    path = options.project_dir.value / ref
    if path.exists():
        return path.relative_to(options.project_dir.value)

    # okay, I dunno what you're talking about
    raise FileNotFoundError
