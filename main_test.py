from main import *


def repr_grid(grid) -> str:
    return_string = '[\n'
    for column in grid.grid:
        return_string += '  [ '
        for block in column:
            if block.is_empty():
                return_string += ' , '
            if not block.is_empty():
                return_string += str(block._block_type) + ', '
        return_string += ']\n'
    return_string += ']\n'
    return return_string

tetris = Tetris()
print(repr_grid(tetris.main_field))
