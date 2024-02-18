import copy
import ctypes
from main import *

def repr_block(block_type):
    return_string = ''
    current_block_type = block_type
    # I
    if current_block_type == 1:
        return_string += '\033[36m'
    # O
    if current_block_type == 2:
        return_string += '\033[33m'
    # S
    if current_block_type == 3:
        return_string += '\033[32m'
    #Z
    if current_block_type == 4:
        return_string += '\033[31m'
    #J
    if current_block_type == 5:
        return_string += '\033[34m'
    #L
    if current_block_type == 6:
        return_string += '\033[38;2;255;48;0m'
    #T
    if current_block_type == 7:
        return_string += '\033[35m'
    return_string += str(current_block_type)
    return_string += '\033[0m'
    return return_string

def repr_grid(grid: Grid, current_mino: CurrentMino, hold_mino: Mino) -> str:
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
                return_string += repr_block(block._block_type)
                return_string += ', '
        return_string += ']\n'
    return_string += ']\n'
    return_string += '\nHOLD:\n[\n'
    for line_number, column in enumerate(reversed(hold_mino.get_grid().grid)):
        return_string += f'  {str(line_number-hold_mino.get_size().y).zfill(3)}[ '
        for block in column:
            if block.is_empty():
                return_string += ' , '
            if not block.is_empty():
                return_string += repr_block(block._block_type)
                return_string += ', '
        return_string += ']\n'
    return_string += ']\n'
    return return_string

ENABLE_PROCESSED_OUTPUT = 0x0001
ENABLE_WRAP_AT_EOL_OUTPUT = 0x0002
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
MODE = ENABLE_PROCESSED_OUTPUT + ENABLE_WRAP_AT_EOL_OUTPUT + ENABLE_VIRTUAL_TERMINAL_PROCESSING
 
kernel32 = ctypes.windll.kernel32
handle = kernel32.GetStdHandle(-11)
kernel32.SetConsoleMode(handle, MODE)

tetris = Tetris()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))

# I
for i in range(3):
    tetris.move_right()
tetris.rotate_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

# O
for i in range(4):
    tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#S
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
print(tetris.hold_mino)
tetris.hold()
#Z
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#J
for i in range(4):
    tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()
#L
tetris.hold()

#S
for i in range(4):
    tetris.move_left()
tetris.rotate_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#T
tetris.rotate_left()
tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#I
tetris.rotate_left()
for i in range(4):
    tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#O
for i in range(4):
    tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#S
tetris.hold()
#L
tetris.rotate_right()
for i in range(4):
    tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#Z
tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#J
tetris.rotate_right()
for i in range(4):
    tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#L
tetris.rotate_left()
for i in range(4):
    tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#T
tetris.hold()
#S
tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()

#I
tetris.hold()
#T
tetris.move_left()
for i in range(15):
    tetris.move_down()
print(tetris.is_bottom())
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.move_left()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))

tetris.rotate_right()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
result = tetris.place_mino()
tetris.make_mino()
print(result)
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))

#O
for i in range(3):
    tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
tetris.make_mino()
#S
tetris.hold()
#I
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino))
