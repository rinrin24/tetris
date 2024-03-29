from abc import abstractmethod, ABCMeta
from typing import Self

class Mino(metaclass=ABCMeta):
    @abstractmethod
    def rotate_right(self) -> None:
        raise NotImplementedError()
    def rotate_left(self) -> None:
        raise NotImplementedError()

class Block:
    @classmethod
    def make_empty(cls) -> Self:
        return cls(None)
    def __init__(self, block_type: int) -> None:
        self._block_type: int = block_type
    def is_empty(self) -> bool:
        return self._block_type is None
    def __repr__(self) -> str:
        if self._block_type is None:
            return 'None'
        return str(self._block_type)

class Grid:
    @classmethod
    def from_string_list(cls, new_list: list[list[str]], block_type: Block) -> Self:
        new_grid: Grid = cls(len(new_list[0]), len(new_list))
        for i, column in enumerate(new_list):
            for j, block in enumerate(column):
                if not block == '':
                    new_grid.add_block(j, i, block_type)
        return new_grid
    def __init__(self, size_x: int, size_y: int) -> None:
        self.size_x: int = size_x
        self.size_y: int = size_y
        self.grid = [[ Block(None) for i in range(size_x)] for j in range(size_y)]
    def __repr__(self) -> str:
        return_string = '[\n'
        for column in self.grid:
            return_string += '  [ '
            for block in column:
                if block.is_empty():
                    return_string += ' , '
                if not block.is_empty():
                    return_string += str(block._block_type) + ', '
            return_string += ']\n'
        return_string += ']\n'
        return return_string
    def is_empty(self, position_x: int, position_y: int) -> bool:
        return self.grid[position_y][position_x].is_empty
    def add_block(self, position_x: int, position_y: int, block: Block) -> Self:
        self.grid[position_y][position_x] = block
        return

class Mino3x3:
    def rotate_right(self, current_shape: Grid, block_type: Block) -> Grid:
        new_shape = Grid(3, 3)
        new_shape.add_block(1, 1, block_type)
        current_grid: list[list[Block]] = current_shape.grid
        for i in range(3):
            if not current_grid[0][i].is_empty():
                new_shape.add_block(2, i, block_type)
        if not current_grid[1][0].is_empty():
            new_shape.add_block(1, 0, block_type)
        if not current_grid[1][2].is_empty():
            new_shape.add_block(1, 2, block_type)
        for i in range(3):
            if not current_grid[2][i].is_empty():
                new_shape.add_block(0, i, block_type)
        return new_shape
    def rotate_left(self, current_shape: Grid, block_type: Block) -> Grid:
        new_shape = Grid(3, 3)
        new_shape.add_block(1, 1, block_type)
        current_grid: list[list[Block]] = current_shape.grid
        for i in range(3):
            if not current_grid[0][i].is_empty():
                new_shape.add_block(0, 2-i, block_type)
        if not current_grid[1][0].is_empty():
            new_shape.add_block(1, 2, block_type)
        if not current_grid[1][2].is_empty():
            new_shape.add_block(1, 0, block_type)
        for i in range(3):
            if not current_grid[2][i].is_empty():
                new_shape.add_block(2, 2-i, block_type)
        return new_shape

class IMino(Mino):
    BLOCK_TYPE: Block = Block(1)
    SHAPE = Grid.from_string_list([
        ['', '', '', ''],
        ['o', 'o', 'o', 'o'],
        ['', '', '', ''],
        ['', '', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = IMino.SHAPE
    def rotate_right(self) -> None:
        new_shape = Grid(4, 4)
        for i in range(4):
            for j in range(4):
                if not self.current_shape.grid[j][i].is_empty():
                    new_shape.add_block(3-j, i, IMino.BLOCK_TYPE)
        self.current_shape = new_shape
    def rotate_left(self) -> None:
        new_shape = Grid(4, 4)
        for i in range(4):
            for j in range(4):
                if not self.current_shape.grid[j][i].is_empty():
                    new_shape.add_block(j, 3-i, IMino.BLOCK_TYPE)
        self.current_shape = new_shape

class OMino(Mino):
    BLOCK_TYPE: Block = Block(2)
    SHAPE = Grid.from_string_list([
        ['o', 'o'],
        ['o', 'o']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = OMino.SHAPE
    def rotate_right(self) -> None:
        return
    def rotate_left(self) -> None:
        return

class SMino(Mino):
    BLOCK_TYPE: Block = Block(3)
    SHAPE = Grid.from_string_list([
        ['', 'o', 'o'],
        ['o', 'x', ''],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, SMino.BLOCK_TYPE)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, SMino.BLOCK_TYPE)

class ZMino(Mino):
    BLOCK_TYPE = Block(4)
    SHAPE = Grid.from_string_list([
        ['o', 'o', ''],
        ['', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = ZMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, ZMino.BLOCK_TYPE)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, ZMino.BLOCK_TYPE)

class JMino(Mino):
    BLOCK_TYPE: Block = Block(5)
    SHAPE = Grid.from_string_list([
        ['o', '', ''],
        ['o', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = JMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, JMino.BLOCK_TYPE)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, JMino.BLOCK_TYPE)

class LMino(Mino):
    BLOCK_TYPE: Block = Block(6)
    SHAPE = Grid.from_string_list([
        ['', '', 'o'],
        ['o', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = LMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, LMino.BLOCK_TYPE)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, LMino.BLOCK_TYPE)

class TMino(Mino):
    BLOCK_TYPE: Block = Block(7)
    SHAPE = Grid.from_string_list([
        ['', 'o', ''],
        ['o', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = TMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, TMino.BLOCK_TYPE)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, TMino.BLOCK_TYPE)

SHAPE = Grid.from_string_list([
	['', '', '', ''],
	['o', 'o', 'o', 'o'],
	['', '', '', ''],
	['', '', '', '']
], Block(1))

# print(SHAPE)

mino = []
mino.append(IMino())
mino.append(SMino())
mino.append(ZMino())
mino.append(JMino())
mino.append(LMino())
mino.append(TMino())

# print(ZMino().current_shape)

for a_mino in mino:
    for x in range(4):
        print(a_mino.current_shape)
        a_mino.rotate_right()
