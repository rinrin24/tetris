from abc import abstractmethod, ABCMeta
from typing import Self, ClassVar
from dataclasses import dataclass

class Mino(metaclass=ABCMeta):
    @abstractmethod
    def rotate_right(self) -> None:
        raise NotImplementedError()
    def rotate_left(self) -> None:
        raise NotImplementedError()
        raise NotImplementedError()

@dataclass(frozen=True, eq=True)
class Block:
    _block_type: int
    EMPTY_NUMBER: ClassVar[int] = 0
    WALL_NUMBER: ClassVar[int] = -1
    @classmethod
    def EMPTY(cls) -> Self:
        return cls(Block.EMPTY_NUMBER)
    @classmethod
    def WALL(cls) -> Self:
        return cls(Block.WALL_NUMBER)
    def is_empty(self) -> bool:
        return self._block_type is Block.EMPTY_NUMBER

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
        self.grid = [[ Block.EMPTY() for i in range(size_x)] for j in range(size_y)]
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
    def get_grid(self) -> None:
        return self.current_shape

class OMino(Mino):
    BLOCK_TYPE: Block = Block(2)
    SHAPE = Grid.from_string_list([
        ['o', 'o'],
        ['o', 'o']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = OMino.SHAPE
    def rotate_right(self) -> None:
        return
    def rotate_left(self) -> None:
        return
    def get_grid(self) -> None:
        return self.current_shape

class SMino(Mino):
    BLOCK_TYPE: Block = Block(3)
    SHAPE = Grid.from_string_list([
        ['', 'o', 'o'],
        ['o', 'x', ''],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, SMino.BLOCK_TYPE)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, SMino.BLOCK_TYPE)
    def get_grid(self) -> None:
        return self.current_shape

class ZMino(Mino):
    BLOCK_TYPE = Block(4)
    SHAPE = Grid.from_string_list([
        ['o', 'o', ''],
        ['', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = ZMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, ZMino.BLOCK_TYPE)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, ZMino.BLOCK_TYPE)
    def get_grid(self) -> None:
        return self.current_shape

class JMino(Mino):
    BLOCK_TYPE: Block = Block(5)
    SHAPE = Grid.from_string_list([
        ['o', '', ''],
        ['o', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = JMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, JMino.BLOCK_TYPE)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, JMino.BLOCK_TYPE)
    def get_grid(self) -> None:
        return self.current_shape

class LMino(Mino):
    BLOCK_TYPE: Block = Block(6)
    SHAPE = Grid.from_string_list([
        ['', '', 'o'],
        ['o', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = LMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, LMino.BLOCK_TYPE)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, LMino.BLOCK_TYPE)
    def get_grid(self) -> None:
        return self.current_shape

class TMino(Mino):
    BLOCK_TYPE: Block = Block(7)
    SHAPE = Grid.from_string_list([
        ['', 'o', ''],
        ['o', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = TMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, TMino.BLOCK_TYPE)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, TMino.BLOCK_TYPE)
    def get_grid(self) -> None:
        return self.current_shape

class EmptyMino(Mino):
    def __init__(self) -> None:
        self.current_shape: Grid = Grid(0, 0)
    def rotate_right(self) -> None:
        pass
    def rotate_left(self) -> None:
        pass
    def get_grid(self) -> None:
        return self.current_shape

@dataclass(frozen=True, slots=True)
class Position:
    """shows the position of each mino

    x coordinate will be counted from the left end of the field
    y coordinate will be counted from the bottom of the field

    """
    x: int
    y: int
    __slots__ = ['x', 'y']

class CurrentMino:
    def __init__(self, new_mino: Mino) -> None:
        self.mino: Mino = new_mino
        self.position: Position = Tetris.INITIAL_POSITION

        mino_pile: list[Mino] = [IMino(), OMino(), SMino(), ZMino(), JMino(), LMino(), TMino()]
class Tetris:
    INITIAL_POSITION = Position(4, 19)
    def __init__(self) -> None:
        pass
