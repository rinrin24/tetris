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

def repr_grid(grid: Grid, current_mino: CurrentMino, hold_mino: Mino, ghost_mino_position: Position) -> str:
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
                new_grid.add_block(Position(ghost_mino_position.x+x, ghost_mino_position.y+y), Block(9))
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
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))
tetris.make_mino()

print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

# I
for i in range(3):
    tetris.move_right()
tetris.rotate_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

# O
for i in range(4):
    tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#S
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))
print(tetris.hold_mino)
tetris.hold()
#Z
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))
tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#J
for i in range(4):
    tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))
#L
tetris.hold()

#S
for i in range(4):
    tetris.move_left()
tetris.rotate_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#T
tetris.rotate_left()
tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#I
tetris.rotate_left()
for i in range(4):
    tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#O
for i in range(4):
    tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#S
tetris.hold()
#L
tetris.rotate_right()
for i in range(4):
    tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#Z
tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#J
tetris.rotate_right()
for i in range(4):
    tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#L
tetris.rotate_left()
for i in range(4):
    tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#T
tetris.hold()
#S
tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#I
tetris.hold()
#T
tetris.move_left()
for i in range(15):
    tetris.move_down()
print(tetris.is_bottom())
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))
tetris.move_left()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

tetris.rotate_right()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))
result = tetris.place_mino()
print(result)
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#O
for i in range(3):
    tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))
#S
tetris.hold()
#I
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))
tetris.rotate_left()
tetris.move_left()
for i in range(17):
    tetris.move_down()
tetris.rotate_left()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))
result = tetris.place_mino()
print(result)
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#Z
tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

# J
tetris.hold()
# S
tetris.rotate_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

# L
tetris.rotate_left()
tetris.move_right()
tetris.move_right()
result = tetris.hard_drop()
print(result)
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#T
tetris.hold()
#J
tetris.rotate_right()
tetris.move_left()
tetris.move_left()
result = tetris.hard_drop()
print(result)
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#I
for i in range(2):
    tetris.move_right()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#O
for i in range(4):
    tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#S
tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#Z
tetris.rotate_left()
tetris.move_left()
tetris.move_left()
tetris.hard_drop()
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))

#J
tetris.hold()
#T
for i in range(3):
    tetris.move_right()
for i in range(18):
    tetris.move_down()
tetris.rotate_left()
result = tetris.place_mino()
print(result)
print(repr_grid(tetris.main_field, tetris.current_mino, tetris.hold_mino, tetris.get_ghost_block()))
