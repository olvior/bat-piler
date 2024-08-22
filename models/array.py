from typing import Dict, List

from memory.ram import RAM
from models.variable import Variable


class Array:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.address = RAM.allocate(size)
        self.variables: List[Variable] = [
            Variable(f"{name}_{index}", self.address + index) for index in range(size)
        ]
        active_arrays[name] = self

    def free(self) -> None:
        for variable in self.variables:
            variable.free()
        active_arrays.pop(self.name)


active_arrays: Dict[str, Array] = {}
