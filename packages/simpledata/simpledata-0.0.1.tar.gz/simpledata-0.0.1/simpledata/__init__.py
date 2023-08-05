import pickle
import json
import os

def _util_file(path, mode, func, args):
    kwargs = {}
    if mode != 'wb': kwargs['encoding'] = 'utf8'
    with open(os.path.join(*path), mode, **kwargs) as f: return func(*(map(lambda x: f if x == 'FILE' else x, args)))

class write:
    """Write to files and create strings"""
    class file:
        """Write to files"""
        @classmethod
        def json(_, obj, *path):
            """
            Write to a JSON file.
            :param obj: The object to write to the file
            :param path: The destination path
            """
            return _util_file(path, 'w', json.dump, [obj, 'FILE'])

        @classmethod
        def pickle(_, obj, *path):
            """
            Write to a Pickle file.
            :param obj: The object to write to the file
            :param path: The destination path
            """
            return _util_file(path, 'wb', pickle.dump, [obj, 'FILE'])

    class str:
        """Create strings with data"""
        @classmethod
        def json(_, obj):
            """
            Create a JSON string
            :param obj: The object passed to the creator function
            """
            return json.dumps(obj)

        @classmethod
        def pickle(_, obj):
            """
            Create a Pickle string (bytes)
            :param obj: The object passed to the creator function
            """
            return pickle.dumps(obj)

class load:
    """Load files and parse data from strings"""
    class file:
        @classmethod
        def json(_, *path):
            """
            Load a JSON file
            :param path: The path of the file to load from
            """
            return _util_file(path, 'r', json.load, ['FILE'])

        @classmethod
        def pickle(_, *path):
            """
            Load a Pickle file
            :param path: The path of the file to load from
            """
            return _util_file(path, 'r', pickle.load, ['FILE'])

    class str:
        @classmethod
        def json(_, obj):
            """
            Parse a JSON string
            :param obj: The string to parse
            """
            return json.loads(obj)

        @classmethod
        def pickle(_, obj):
            """
            Load Pickle data from a string
            :param obj: The string to load the data from
            """
            return pickle.loads(obj)

def _add_flags(o, *flags):
    for flag in flags:
        setattr(o, flag, True)

def _has_flags(o, *flags):
    checks = []
    for flag in flags:
        checks.add(hasattr(o, flag))
    return all(checks)

_add_flags(load.file.json, 'load', 'file', 'json')
_add_flags(load.file.pickle, 'load', 'file', 'pickle')
_add_flags(load.str.json, 'load', 'str', 'json')
_add_flags(load.str.pickle, 'load', 'str', 'pickle')
_add_flags(write.file.json, 'write', 'file', 'json')
_add_flags(write.file.pickle, 'write', 'file', 'pickle')
_add_flags(write.str.json, 'write', 'str', 'json')
_add_flags(write.str.pickle, 'write', 'str', 'pickle')

def write_func(f):
    """Decorator"""
    _add_flags(f, 'write')

def load_func(f):
    """Decorator"""
    _add_flags(f, 'load')

def file_func(f):
    """Decorator"""
    _add_flags(f, 'file')

def str_func(f):
    """Decorator"""
    _add_flags(f, 'str')

# class base_writers:
#     PICKLE = write.file.pickle
#     PICKLE_STR = write.str.pickle

#     JSON = write.file.json
#     JSON_STR = write.file.pickle

# class base_loaders:
#     PICKLE = load.file.pickle
#     PICKLE_STR = load.str.pickle

#     JSON = load.file.json
#     JSON_STR = load.str.json

# class base_lw_pairs:
#     PICKLE = (base_loaders.PICKLE, base_writers.PICKLE)
#     PICKLE_STR = (base_loaders.PICKLE_STR, base_writers.PICKLE_STR)

#     JSON = (base_loaders.JSON, base_writers.JSON)
#     JSON_STR = (base_loaders.JSON_STR, base_writers.JSON_STR)

class file_loader:
    """Loads files"""
    def __init__(self, func, *path):
        """
        :param func: The loader function
        :param path: The path
        """
        if not _has_flags(func, 'file', 'load'): raise ValueError('invalid function passed')
        self.func = func
        self.path = os.path.join(*path)
    
    def load(self):
        return self.func(self.path)

class file_writer:
    """Writes to files"""
    def __init__(self, func, *path):
        """
        :param func: The writer function
        :param path: The path
        """
        if not _has_flags(func, 'file', 'write'): raise ValueError('invalid function passed')
        self.func = func
        self.path = os.path.join(*path)
    
    def write(self, value):
        return self.func(value, self.path)

class file_operator:
    """Loads and writes to files"""
    def __init__(self, loaderf, writerf, *path):
        """
        :param loaderf: The loader function
        :param writerf: The writer function
        :param path: The path
        """
        if not _has_flags(loaderf, 'file', 'load'): raise ValueError('invalid loader function passed')
        if not _has_flags(writerf, 'file', 'load'): raise ValueError('invalid writer function passed')
        self.loaderf = loaderf
        self.writerf = writerf
        self.path = os.path.join(*path)
    
    def load(self):
        return self.loaderf(self.path)
    
    def write(self, value):
        return self.writerf(value, self.path)
