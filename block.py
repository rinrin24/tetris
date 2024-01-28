from dataclasses import dataclass
from typing import Self, ClassVar

@dataclass(frozen=True, eq=True)
class Block:
    _block_type: int
    EMPTY_NUMBER: ClassVar[int] = 0
    @classmethod
    def EMPTY(cls) -> Self:
        return cls(Block.EMPTY_NUMBER)
    def is_empty(self) -> bool:
        return self._block_type is Block.EMPTY_NUMBER
    def __repr__(self) -> str:
        return str(self._block_type)

block1 = Block(2)
print(block1)
# block1._block_type = 5
empty_block = Block.EMPTY()
print(empty_block)
print(Block.EMPTY_NUMBER)
