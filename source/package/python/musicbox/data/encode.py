# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import abc
import json
from pathlib import Path


class Encoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, Encodable):
            if isinstance(o, ImportedEncodable):
                encoded_value = o.encode(root_dir=self.root_dir)
            else:
                encoded_value = o.encode()
            return {
                'encoded_type': type(o),
                'encoded_value': encoded_value,
            }
        return super().default(o)


class JSONDataType():

    def __init__(self):
        super().__init__()

    def read(self, filepath):
        filepath = Path(filepath)
        with open(filepath, 'r') as file:
            return json.load(file, cls=Encoder)



class Project(JSONDataType):

    def __init__(self):
        


def register_encodable_type(cls):
    self._encodable_types[f'{cls.__module__}.{cls.__name__}'] = cls


def encode_to_string(object):
    return json.dumps(object, cls=Encoder)


def encode_to_file(object, file_object):
    json_dump(o, file_object, cls=Encoder)


def decode_from_string(string):
    return json.loads(string, cls=Decoder)


def decode_from_file(file_object):
    return json.load(file_object, cls=Encoder)


class Encodable(abc.ABC):

    @abstractmethod
    def encode(self):
        return

    @classmethod
    @abstractmethod
    def decode(cls, value):
        return


class ImportedEncodable(Encodable):

    def encode(self, * root_dir):
        return self._filepath.relative_to(Path(root_dir).resovle())

    @classmethod
    def decode(cls, filepath, root_dir):
        filepath = Path(root_dir).joinpath(filepath)
        with open(filepath, 'r') as fp:
            return decode_from_file(fp)



class Encoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, Encodable):
            if isinstance(o, ImportedEncodable):
                encoded_value = o.encode(root_dir=self.root_dir)
            else:
                encoded_value = o.encode()
            return {
                'encoded_type': type(o),
                'encoded_value': encoded_value,
            }
        return super().default(o)

class Decoder(JSONDecoder):

    def __init__(self, root_dir):
        super().__init__()
        self._root_dir = root_dir

    def decode(self, d):
        try:
            type_name = d['encoded_type']
            encoded_type = _encodable_types[type_name]
            encoded_value = d['encoded_value']
            if issubclass(encoded_type, ImportedEncodable):
                return encoded_type.decode(encoded_value, self.root_dir)
            else:
                return encoded_type.decode(encoded_valued)
        except KeyError:
            return d
