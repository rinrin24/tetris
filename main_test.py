import copy
from main import *


def repr_grid(grid: Grid, current_mino: CurrentMino) -> str:
    mino: Mino = current_mino.mino
    mino_position: Position = current_mino.position
    mino_grid = mino.get_grid().grid
    new_grid = copy.deepcopy(grid)
    mino_position_x = mino_position.x
    mino_position_y = mino_position.y
    for y, column in enumerate(mino_grid):
        for x, block in enumerate(column):
            if not block.is_empty():
                new_grid.add_block(Position(mino_position_x+x, mino_position_y+y), block)
    return_string = '[\n'
    for line_number, column in enumerate(reversed(new_grid.grid)):
        if line_number-20 < -1:
            continue
        return_string += f'  {str(line_number-20).zfill(3)}[ '
        for block in column:
            if block.is_empty():
                return_string += ' , '
            if not block.is_empty():
                return_string += str(block._block_type) + ', '
        return_string += ']\n'
    return_string += ']\n'
    return return_string

tetris = Tetris()
print(repr_grid(tetris.main_field, tetris.current_mino))
tetris.make_mino()
print(tetris.is_bottom())
# tetris.place_mino()
print(repr_grid(tetris.main_field, tetris.current_mino))
# print(tetris.current_mino.position)
for i in range(18):
    tetris.move_down()
print(repr_grid(tetris.main_field, tetris.current_mino))
print(tetris.is_bottom())

tetris.move_down()
print(repr_grid(tetris.main_field, tetris.current_mino))
print(tetris.is_bottom())

tetris.move_down()
print(repr_grid(tetris.main_field, tetris.current_mino))
tetris.place_mino()

tetris.make_mino()

tetris.move_down()
print(repr_grid(tetris.main_field, tetris.current_mino))

current_number = 0
for i in range(16):
    tetris.move_down()
    # print(tetris.is_bottom())
print(repr_grid(tetris.main_field, tetris.current_mino))
# print(current_number)
print(tetris.is_bottom())
tetris.place_mino()
tetris.make_mino()
print(repr_grid(tetris.main_field, tetris.current_mino))

# tetris.make_mino()
# for i in range(15):
#     tetris.move_down()
# print(repr_grid(tetris.main_field, tetris.current_mino))
# print(tetris.is_bottom())
# print(tetris.current_mino.position)
# print(repr_grid(tetris.main_field, CurrentMino(EmptyMino())))
# tetris.move_down()
#print(repr_grid(tetris.main_field, tetris.current_mino))

