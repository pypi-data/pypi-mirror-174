import json
from typing import Tuple, List

from deep_serialization.memory_objects import PythonSerializer
from deep_serialization.json_converter import MemoryDumpEncoder


def serialize_object(obj: object) -> Tuple[str, str]:
    serializer = PythonSerializer()
    id_ = serializer.write_object_to_memory(obj)
    return id_, json.dumps(serializer.memory, cls=MemoryDumpEncoder)


def serialize_objects(objs: List[object]) -> Tuple[List[str], str]:
    serializer = PythonSerializer()
    ids = [
        serializer.write_object_to_memory(obj)
        for obj in objs
    ]
    return ids, json.dumps(serializer.memory, cls=MemoryDumpEncoder)
