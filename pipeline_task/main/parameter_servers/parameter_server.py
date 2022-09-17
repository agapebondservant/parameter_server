from io import BytesIO
import joblib
import inspect
import re
import logging
import lz4


class ParameterServer:
    def __init__(self,
                 host):
        self.host = host

    def initialize_data(self):
        pass

    def get(self, key):
        pass

    def put(self, value, key=None):
        pass

    def finalize(self):
        pass

    def serialize(self, value):
        value = {k: (self.serialize_lob(v)
                 if inspect.getmodule(v) and re.search('(pandas|numpy)', inspect.getmodule(v).__name__)
                 else v)
                 for (k, v) in value.items()}
        return value

    def deserialize(self, value: dict):
        value = {k: (self.deserialize_lob(v)
                 if isinstance(v, BytesIO)
                 else v)
                 for (k, v) in value.items()}
        return value

    def serialize_lob(self, unserialized):
        """
        :param unserialized: Large object to serialize
        :return: A stream of bytes representing the serialized object
        """
        bytes_container = BytesIO()
        joblib.dump(unserialized, bytes_container)
        bytes_container.seek(0)
        compressed = BytesIO(lz4.frame.compress(bytes_container.read()))
        return compressed

    def deserialize_lob(self, serialized: BytesIO):
        """
        :param serialized: io.BytesIO object representing the object to deserialize
        :return: Deserialized object
        """
        decompressed = lz4.frame.decompress(serialized.read())
        deserialized = joblib.load(BytesIO(decompressed))
        return deserialized
