from typing import Self
class Block:
    @classmethod
    def make_empty(cls) -> Self:
        return cls(None)
    def __init__(self, block_type: int | None) -> None:
        self._block_type: int = block_type
    def __repr__(self) -> str:
        if self._block_type is None:
            return "None"
        return str(self._block_type)
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

grid = Grid(3, 5)
print(grid.grid)
grid.add_block(1, 3, Block(1))
print(grid.grid)
SHAPE = [
    ['', 'o', 'o'],
    ['o', 'x', ''],
    ['', '', '']
]
grid2 = Grid.from_list(SHAPE, Block(2))
print(grid2.grid)
