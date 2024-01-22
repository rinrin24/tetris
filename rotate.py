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
    def add_block(self, position_x: int, position_y: int, block: Block):
        self.grid[position_y][position_x] = block
        return

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
        new_shape = Grid(4, 4)
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