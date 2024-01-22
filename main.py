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

class Grid:
    @classmethod
    def from_list(cls, new_list: list[list[str]], block_type: Block) -> Self:
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
    def add_block(self, position_x: int, position_y: int, block: Block) -> None:
        self.grid[position_y][position_x] = block
    def is_empty(self, position_x: int, position_y: int):
        return
class Mino3x3:
    def rotate_right(self, current_shape: list[list[str]]) -> list[list[str]]:
        new_shape = [
            ['', '', ''],
            ['', 'x', ''],
            ['', '', '']
        ]
        for i in range(3):
            if current_shape[0][i] == 'o':
                new_shape[i][2] = 'o'
        if current_shape[1][0] == 'o':
            new_shape[0][1] = 'o'
        if current_shape[1][2] == 'o':
            new_shape[2][1] = 'o'
        for i in range(3):
            if current_shape[2][i] == 'o':
                new_shape[i][0] = 'o'
        return new_shape
    def rotate_left(self, current_shape: list[list[str]]) -> list[list[str]]:
        new_shape = [
            ['', '', ''],
            ['', 'x', ''],
            ['', '', '']
        ]
        for i in range(3):
            if current_shape[0][i] == 'o':
                new_shape[2-i][0] = 'o'
        if current_shape[1][0] == 'o':
            new_shape[2][1] = 'o'
        if current_shape[1][2] == 'o':
            new_shape[0][1] = 'o'
        for i in range(3):
            if current_shape[2][i] == 'o':
                new_shape[2-i][2] = 'o'
        return new_shape

class IMino(Mino):
    BLOCK_TYPE: Block = Block(1)
    SHAPE = Grid.from_list([
        ['', '', '', ''],
        ['o', 'o', 'o', 'o'],
        ['', '', '', ''],
        ['', '', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = IMino.SHAPE
    def rotate_right(self) -> None:
        new_shape = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', '']
        ]
        for i in range(4):
            for j in range(4):
                if self.current_shape[j][i] == 'o':
                    new_shape[i][3-j] = 'o'
        self.current_shape = new_shape
    def rotate_left(self) -> None:
        new_shape = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', ''],
            ['', '', '', '']
        ]
        for i in range(4):
            for j in range(4):
                if self.current_shape[j][i] == 'o':
                    new_shape[3-i][j] = 'o'
        self.current_shape = new_shape

class OMino(Mino):
    BLOCK_TYPE: Block = Block(2)
    SHAPE = Grid.from_list([
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
    SHAPE = Grid.from_list([
        ['', 'o', 'o'],
        ['o', 'x', ''],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape)

class ZMino(Mino):
    BLOCK_TYPE = Block(4)
    SHAPE = Grid.from_list([
        ['o', 'o', ''],
        ['', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape)

class JMino(Mino):
    BLOCK_TYPE: Block = Block(5)
    SHAPE = Grid.from_list([
        ['o', '', ''],
        ['o', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape)

class LMino(Mino):
    BLOCK_TYPE: Block = Block(6)
    SHAPE = Grid.from_list([
        ['', '', 'o'],
        ['o', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape)

class TMino(Mino):
    BLOCK_TYPE: Block = Block(7)
    SHAPE = Grid.from_list([
        ['', 'o', ''],
        ['o', 'x', 'o'],
        ['', '', '']
    ], BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape)

class Position:
    """shows the position of each mino

    x coordinate will be counted from the left end of the field
    y coordinate will be counted from the bottom of the field

    """
    def __init__(self, new_x: int, new_y: int) -> None:
        self.x = new_x
        self.y = new_y

class CurrentMino:
    def __init__(self, new_mino: Mino) -> None:
        self.mino: Mino = new_mino
        self.position: Position = Tetris.INITIAL_POSITION

class Tetris:
    INITIAL_POSITION = Position(4, 19)
    def __init__(self) -> None:
        pass
