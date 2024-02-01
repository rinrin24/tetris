from typing import ClassVar
from dataclasses import dataclass, FrozenInstanceError

@dataclass(frozen=True, slots=True, eq=True)
class Direction:
    """the direction of mino
    
    Note:
        direction numbers are defined from page under
        https://tetrisch.github.io/main/srs.html
    """
    value: int
    _NUMBER_A: ClassVar[int] = 0
    _NUMBER_B: ClassVar[int] = 1
    _NUMBER_C: ClassVar[int] = 2
    _NUMBER_D: ClassVar[int] = 3
    @classmethod
    def A(cls) -> 'Direction':
        return cls(Direction._NUMBER_A)
    @classmethod
    def B(cls) -> 'Direction':
        return cls(Direction._NUMBER_B)
    @classmethod
    def C(cls) -> 'Direction':
        return cls(Direction._NUMBER_C)
    @classmethod
    def D(cls) -> 'Direction':
        return cls(Direction._NUMBER_D)

dir1 = Direction.A()
print(dir1 == Direction.A())
print(dir1 is Direction.A())
print(dir1 == Direction.B())
print(Direction.__slots__)
try:
    dir1.value = 2
except FrozenInstanceError:
    print('you cannot change field!')
