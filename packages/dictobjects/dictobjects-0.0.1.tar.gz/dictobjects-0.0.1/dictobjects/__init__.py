import json
import os
import pickle

class dictobj:
    """A object that converts dictionary keys to attributes"""

    def __init__(self, d=None):
        """
        :param d: The base dictionary
        """
        dct = d or {}
        if not isinstance(dct, dict): raise TypeError('must be dict')
        self.__dictionary__ = dct
        self.__createdict__()
    
    def __is_iter__(self, o):
        return (not isinstance(o, (str, dict))) and hasattr(o, '__iter__')
    
    def __deconvert__(self, o):
        if isinstance(o, dict): return o
        elif isinstance(o, dictobj): return o.__dictionary__
        elif self.__is_iter__(o): return self.__deconvertcollection__()

    def __create__(self, o):
        if isinstance(o, dict): return dictobj(o)
        elif isinstance(o, dictobj): return o
        elif self.__is_iter__(o): return self.__createcollection__(o)
        return o

    def __createcollection__(self, collection):
        res = []
        for i in collection:
            res.append(self.__create__(i))
        return res
    
    def __validate_id__(self, k):
        return isinstance(k, str) and k.isidentifier()

    def __createdict__(self):
        for k, v in self.__dictionary__.items():
            if not self.__validate_id__(k): raise ValueError('invalid key')
            setattr(self, k, self.__create__(v))
    
    def __setfield__(self, name, value):
        if not self.__validate_id__(name): raise ValueError('invalid key')
        self.__dictionary__[name] = value
        setattr(self, name, self.__create__(value))

    def __set_attr_or_field__(self, name, value):
        if name not in self.__dictionary__:
            return super().__setattr__(name, value)
        self.__setfield__(name, value)
        self.__on_set__(name, value)

    def __setattribute__(self, name, value):
        self.__set_attr_or_field__(name, value)

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, name, value):
        self.__set_attr_or_field__(name, value)

    def __str__(self):
        return f'{type(self).__name__}()'
    
    def __repr__(self):
        return str(self)

    def __on_set__(self, name, value):
        pass

    def __contains__(self, value):
        return value in self.__dictionary__

    def keys(self):
        """Get the keys of the dictionary"""
        return list(self.__dictionary__.keys())
    
    def values(self):
        """Get the values of the dictionary"""
        for i in dir(self):
            if i not in self.__dictionary__: continue
            return getattr(self, i)

    def get(self, key, default=None):
        """
        Get the corresponding value from the passed key.\n
        If not found then return the default value
        :param key: The key to find
        :param default: The default value
        """
        if key not in self.__dictionary__: return default
        return getattr(self, key)

    def dict(self):
        """Convert this object to a dictionary"""
        return self.__dictionary__

    def __dict__(self):
        return self.__dictionary__

    def save_simpledata(self, writer, *args):
        """Save the dictobj to a file or a string with the simpledata libary (pickle recomended)"""
        return dictobj(writer(*args))
    
    def save_json_file(self, *path):
        """Save the dictobj to a JSON file (error-prone)"""
        with open(os.path.join(*path), 'w', encoding='utf8') as f:
            json.dump(self.__dictionary__, f)
    
    def save_pickle_file(self, *path):
        """Save the dictobj to a Pickle file (recomended)"""
        with open(os.path.join(*path), 'wb') as f:
            pickle.dump(self, f)
    
    def save_json_str(self):
        """Save the dictobj to a JSON file (error-prone)"""
        return json.dumps(self.__dictionary__)
    
    def save_pickle_bytes(self):
        """Save the dictobj to a Pickle file (recomended)"""
        return pickle.dumps(self)

    def __iter__(self):
        for i in self.values():
            yield i

    @classmethod
    def from_simpledata(self, loader, *args):
        """Create a dictobj with the simpledata libary (pickle recomended)"""
        return dictobj(loader(*args))

    @classmethod
    def from_json_file(self, *path):
        """Create a dictobj from a JSON file (error-prone)"""
        with open(os.path.join(*path), encoding='utf8') as f:
            return dictobj(json.load(f))

    @classmethod
    def from_json_string(self, string):
        """Create a dictobj from a JSON string (error-prone)"""
        return dictobj(json.loads(string))

    @classmethod
    def from_pickle_file(self, *path):
        """Create a dictobj from a Pickle file (recomended)"""
        with open(os.path.join(*path), 'rb', encoding='utf8') as f:
            return dictobj(pickle.load(f))

    @classmethod
    def from_pickle_bytes(self, byte):
        """Create a dictobj from Pickle bytes (recomended)"""
        return dictobj(pickle.loads(byte))
