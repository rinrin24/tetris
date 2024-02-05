from abc import abstractmethod, ABCMeta
from typing import Self, ClassVar
from dataclasses import dataclass, field
from random import sample

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

@dataclass(frozen=True, slots=True)
class Size:
    x: int
    y: int

@dataclass(frozen=True, slots=True)
class Position:
    """shows the position of each mino

    x coordinate will be counted from the left end of the field

    y coordinate will be counted from the bottom of the field

    """
    x: int
    y: int
    def to_center_position(self, size: Size) -> 'CenterPosition':
        new_x = self.x + size.x // 2
        new_y = self.y + size.y // 2
        return CenterPosition(new_x, new_y)

@dataclass(frozen=True, slots=True)
class CenterPosition:
    """shows the center position of each mino

    x coordinate will be counted from the left end of the field

    y coordinate will be counted from the bottom of the field

    """
    x: int
    y: int
    def to_position(self, size: Size) -> Position:
        new_x = self.x - size.x // 2
        new_y = self.y - size.y // 2
        return Position(new_x, new_y)

@dataclass(frozen=True, slots=True)
class PlotGridPosition:
    x: int
    y: int

@dataclass(frozen=True, slots=True)
class RelativePosition:
    x: int
    y: int

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
    def rotate_left(self):
        if self == Direction.A():
            return Direction.D()
        if self == Direction.B():
            return Direction.A()
        if self == Direction.C():
            return Direction.B()
        if self == Direction.D():
            return Direction.C()
    def rotate_right(self):
        if self == Direction.A():
            return Direction.B()
        if self == Direction.B():
            return Direction.C()
        if self == Direction.C():
            return Direction.D()
        if self == Direction.D():
            return Direction.A()

@dataclass(frozen=True, slots=True, eq=True)
class SuperRotationStep:
    step: int

class Grid:
    @classmethod
    def from_string_list(cls, new_list: list[list[str]], block_type: Block) -> 'Grid':
        new_grid: Grid = cls(Size(len(new_list[0]), len(new_list)))
        for i, column in enumerate(new_list):
            for j, block in enumerate(column):
                if not block == '':
                    new_grid.add_block(Position(j, i), block_type)
        return new_grid
    def __init__(self, size: Size) -> None:
        self.size_x: int = size.x
        self.size_y: int = size.y
        self.grid = [[ Block.EMPTY() for i in range(size.x)] for j in range(size.y)]
    def is_empty(self, position: Position) -> bool:
        return self.grid[position.y][position.x].is_empty()
    def add_block(self, position: Position, block: Block) -> None:
        self.grid[position.y][position.x] = block
    def _is_outside(self, position_x: int, position_y: int) -> bool:
        if (position_x < 0) or (position_y < 0):
            return True
        if (position_x >= self.size_x) or (position_y >= self.size_y):
            return True
        return False
    def plot_grid(self, position: Position, size: Size) -> 'Grid':
        new_grid = Grid(size)
        for y in range(size.y):
            for x in range(size.x):
                if self._is_outside(position.x+x, position.y+y):
                    new_grid.add_block(Position(x, y), Block.WALL())
                if not self._is_outside(position.x+x, position.y+y):
                    new_grid.add_block(Position(x, y), self.grid[position.y + y][position.x + x])
        return new_grid
    def get_size(self) -> Size:
        if len(self.grid) <= 0:
            return Size(0, 0)
        return Size(len(self.grid[0]), len(self.grid))
    def __repr__(self) -> str:
        return_string = '[\n'
        for line_number, column in enumerate(reversed(self.grid)):
            return_string += f'  {str(line_number).zfill(3)}[ '
            for block in column:
                if block.is_empty():
                    return_string += ' , '
                if not block.is_empty():
                    return_string += str(block._block_type) + ', '
            return_string += ']\n'
        return_string += ']\n'
        return return_string

class Mino(metaclass=ABCMeta):
    @abstractmethod
    def rotate_right(self) -> None:
        raise NotImplementedError()
    @abstractmethod
    def rotate_left(self) -> None:
        raise NotImplementedError()
    @abstractmethod
    def get_grid(self) -> Grid:
        raise NotImplementedError()
    @abstractmethod
    def get_size(self) -> Size:
        raise NotImplementedError()
    @abstractmethod
    def get_direction(self) -> Direction:
        raise NotImplementedError()
    @abstractmethod
    def super_rotate(self,
                     current_direction: Direction,
                     previous_direction: Direction,
                     current_step: SuperRotationStep,
                     current_relative_position: RelativePosition
                    ) -> RelativePosition:
        raise NotImplementedError()

class Mino3x3:
    def rotate_right(self, current_shape: Grid, block_type: Block) -> Grid:
        new_shape = Grid(Size(3, 3))
        new_shape.add_block(Position(1, 1), block_type)
        current_grid: list[list[Block]] = current_shape.grid
        for i in range(3):
            if not current_grid[0][i].is_empty():
                new_shape.add_block(Position(2, i), block_type)
        if not current_grid[1][0].is_empty():
            new_shape.add_block(Position(1, 0), block_type)
        if not current_grid[1][2].is_empty():
            new_shape.add_block(Position(1, 2), block_type)
        for i in range(3):
            if not current_grid[2][i].is_empty():
                new_shape.add_block(Position(0, i), block_type)
        return new_shape
    def rotate_left(self, current_shape: Grid, block_type: Block) -> Grid:
        new_shape = Grid(Size(3, 3))
        new_shape.add_block(Position(1, 1), block_type)
        current_grid: list[list[Block]] = current_shape.grid
        for i in range(3):
            if not current_grid[0][i].is_empty():
                new_shape.add_block(Position(0, 2-i), block_type)
        if not current_grid[1][0].is_empty():
            new_shape.add_block(Position(1, 2), block_type)
        if not current_grid[1][2].is_empty():
            new_shape.add_block(Position(1, 0), block_type)
        for i in range(3):
            if not current_grid[2][i].is_empty():
                new_shape.add_block(Position(2, 2-i), block_type)
        return new_shape
    def super_rotate(
            self,
            current_direction: Direction,
            previous_direction: Direction,
            current_step: SuperRotationStep,
            current_relative_position: RelativePosition
        ) -> RelativePosition:
        current_x = current_relative_position.x
        current_y = current_relative_position.y
        is_right_rotation = ((current_direction.value - 1) % 4) == previous_direction.value
        if current_step == SuperRotationStep(0):
            if current_direction == Direction.B():
                return RelativePosition(current_x-1, current_y+0)
            if current_direction == Direction.D():
                return RelativePosition(current_x+1, current_y+0)
            # rotate right
            if is_right_rotation:
                return RelativePosition(current_x-1, current_y+0)
            # rotate left
            if not is_right_rotation:
                return RelativePosition(current_x+1, current_y+0)
        if current_step == SuperRotationStep(1):
            if (current_direction == Direction.B()) or (current_direction == Direction.D()):
                return RelativePosition(current_x+0, current_y-1)
            if (current_direction == Direction.A()) or (current_direction == Direction.C()):
                return RelativePosition(current_x+0, current_y+1)
        if current_step == SuperRotationStep(2):
            if (current_direction == Direction.B()) or (current_direction == Direction.D()):
                return RelativePosition(0, 2)
            if (current_direction == Direction.A()) or (current_direction == Direction.C()):
                return RelativePosition(0, -2)
        if current_step == SuperRotationStep(3):
            if current_direction == Direction.B():
                return RelativePosition(current_x-1, current_y+0)
            if current_direction == Direction.D():
                return RelativePosition(current_x+1, current_y+0)
            # rotate right
            if is_right_rotation:
                return RelativePosition(current_x-1, current_y+0)
            # rotate left
            if not is_right_rotation:
                return RelativePosition(current_x+1, current_y+0)
        return RelativePosition(0, 0)

class IMino(Mino):
    BLOCK_TYPE: Block = Block(1)
    SHAPE = Grid.from_string_list(list(reversed([
        ['', '', '', ''],
        ['o', 'o', 'o', 'o'],
        ['', '', '', ''],
        ['', '', '', '']
    ])), BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = IMino.SHAPE
        self.current_direction: Direction = Direction.A()
    def rotate_right(self) -> None:
        new_shape = Grid(Size(4, 4))
        for i in range(4):
            for j in range(4):
                if not self.current_shape.grid[j][i].is_empty():
                    new_shape.add_block(Position(3-j, i), IMino.BLOCK_TYPE)
        self.current_shape = new_shape
        self.current_direction = self.current_direction.rotate_right()
    def rotate_left(self) -> None:
        new_shape = Grid(Size(4, 4))
        for i in range(4):
            for j in range(4):
                if not self.current_shape.grid[j][i].is_empty():
                    new_shape.add_block(Position(j, 3-i), IMino.BLOCK_TYPE)
        self.current_shape = new_shape
        self.current_direction = self.current_direction.rotate_left()
    def get_grid(self) -> Grid:
        return self.current_shape
    def get_size(self) -> Size:
        return self.current_shape.get_size()
    def get_direction(self) -> Direction:
        return self.current_direction
    def super_rotate(
            self,
            current_direction: Direction,
            previous_direction: Direction,
            current_step: SuperRotationStep,
            current_relative_position: RelativePosition
        ) -> RelativePosition:
        current_x = current_relative_position.x
        current_y = current_relative_position.y
        is_right_rotation = ((current_direction.value - 1) % 4) == previous_direction.value
        if current_step == SuperRotationStep(0):
            if previous_direction == Direction.A():
                if current_direction == Direction.B():
                    return RelativePosition(current_x-2, current_y+0)
                if current_direction == Direction.D():
                    return RelativePosition(current_x-1, current_y+0)
            if previous_direction == Direction.C():
                if current_direction == Direction.B():
                    return RelativePosition(current_x+1, current_y+0)
                if current_direction == Direction.D():
                    return RelativePosition(current_x+2, current_y+0)
            if is_right_rotation:
                return RelativePosition(current_x-1, current_y+0)
            if not is_right_rotation:
                return RelativePosition(current_x+1, current_y+0)
        if current_step == SuperRotationStep(1):
            if previous_direction == Direction.A():
                return RelativePosition(current_x+3, current_y)
            if previous_direction == Direction.C():
                return RelativePosition(current_x-3, current_y)
            if current_direction == Direction.A():
                if is_right_rotation:
                    return RelativePosition(1, current_y)
                if not is_right_rotation:
                    return RelativePosition(-1, current_y)
            if current_direction == Direction.C():
                if is_right_rotation:
                    return RelativePosition(2, current_y)
                if not is_right_rotation:
                    return RelativePosition(-2, current_y)
        if current_step == SuperRotationStep(2):
            if current_direction == Direction.B():
                if is_right_rotation:
                    return RelativePosition(-2, 1)
                if not is_right_rotation:
                    return RelativePosition(1, 2)
            if current_direction == Direction.D():
                if is_right_rotation:
                    return RelativePosition(2, -1)
                if not is_right_rotation:
                    return RelativePosition(-1, -2)
            if current_direction == Direction.A():
                if is_right_rotation:
                    return RelativePosition(1, 2)
                if not is_right_rotation:
                    return RelativePosition(2, -1)
            if current_direction == Direction.C():
                if is_right_rotation:
                    return RelativePosition(-1, -2)
                if not is_right_rotation:
                    return RelativePosition(-2, 1)
        if current_step == SuperRotationStep(3):
            if current_direction == Direction.B():
                if is_right_rotation:
                    return RelativePosition(1, -2)
                if not is_right_rotation:
                    return RelativePosition(-2, -1)
            if current_direction == Direction.D():
                if is_right_rotation:
                    return RelativePosition(-1, 2)
                if not is_right_rotation:
                    return RelativePosition(2, 1)
            if current_direction == Direction.A():
                if is_right_rotation:
                    return RelativePosition(-2, -1)
                if not is_right_rotation:
                    return RelativePosition(-1, 2)
            if current_direction == Direction.C():
                if is_right_rotation:
                    return RelativePosition(2, 1)
                if not is_right_rotation:
                    return RelativePosition(1, -2)
        return RelativePosition(0, 0)

class OMino(Mino):
    BLOCK_TYPE: Block = Block(2)
    SHAPE = Grid.from_string_list(list(reversed([
        ['o', 'o'],
        ['o', 'o']
    ])), BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = OMino.SHAPE
        self.current_direction: Direction = Direction.A()
    def rotate_right(self) -> None:
        return
    def rotate_left(self) -> None:
        return
    def get_grid(self) -> Grid:
        return self.current_shape
    def get_size(self) -> Size:
        return self.current_shape.get_size()
    def get_direction(self) -> Direction:
        return self.current_direction
    def super_rotate(
            self,
            current_direction: Direction,
            previous_direction: Direction,
            current_step: SuperRotationStep,
            current_relative_position: RelativePosition
        ) -> RelativePosition:
        return RelativePosition(0, 0)

class SMino(Mino):
    BLOCK_TYPE: Block = Block(3)
    SHAPE = Grid.from_string_list(list(reversed([
        ['', 'o', 'o'],
        ['o', 'x', ''],
        ['', '', '']
    ])), BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
        self.current_direction: Direction = Direction.A()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, SMino.BLOCK_TYPE)
        self.current_direction = self.current_direction.rotate_right()
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, SMino.BLOCK_TYPE)
        self.current_direction = self.current_direction.rotate_left()
    def get_grid(self) -> Grid:
        return self.current_shape
    def get_size(self) -> Size:
        return self.current_shape.get_size()
    def get_direction(self) -> Direction:
        return self.current_direction
    def super_rotate(
            self,
            current_direction: Direction,
            previous_direction: Direction,
            current_step: SuperRotationStep,
            current_relative_position: RelativePosition
        ) -> RelativePosition:
        return self.mino3x3.super_rotate(
                current_direction,
                previous_direction,
                current_step,
                current_relative_position
            )

class ZMino(Mino):
    BLOCK_TYPE = Block(4)
    SHAPE = Grid.from_string_list(list(reversed([
        ['o', 'o', ''],
        ['', 'x', 'o'],
        ['', '', '']
    ])), BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = ZMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
        self.current_direction: Direction = Direction.A()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, ZMino.BLOCK_TYPE)
        self.current_direction = self.current_direction.rotate_right()
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, ZMino.BLOCK_TYPE)
        self.current_direction = self.current_direction.rotate_left()
    def get_grid(self) -> Grid:
        return self.current_shape
    def get_size(self) -> Size:
        return self.current_shape.get_size()
    def get_direction(self) -> Direction:
        return self.current_direction
    def super_rotate(
            self,
            current_direction: Direction,
            previous_direction: Direction,
            current_step: SuperRotationStep,
            current_relative_position: RelativePosition
        ) -> RelativePosition:
        return self.mino3x3.super_rotate(
                current_direction,
                previous_direction,
                current_step,
                current_relative_position
            )

class JMino(Mino):
    BLOCK_TYPE: Block = Block(5)
    SHAPE = Grid.from_string_list(list(reversed([
        ['o', '', ''],
        ['o', 'x', 'o'],
        ['', '', '']
    ])), BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = JMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
        self.current_direction: Direction = Direction.A()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, JMino.BLOCK_TYPE)
        self.current_direction = self.current_direction.rotate_right()
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, JMino.BLOCK_TYPE)
        self.current_direction = self.current_direction.rotate_left()
    def get_grid(self) -> Grid:
        return self.current_shape
    def get_size(self) -> Size:
        return self.current_shape.get_size()
    def get_direction(self) -> Direction:
        return self.current_direction
    def super_rotate(
            self,
            current_direction: Direction,
            previous_direction: Direction,
            current_step: SuperRotationStep,
            current_relative_position: RelativePosition
        ) -> RelativePosition:
        return self.mino3x3.super_rotate(
                current_direction,
                previous_direction,
                current_step,
                current_relative_position
            )

class LMino(Mino):
    BLOCK_TYPE: Block = Block(6)
    SHAPE = Grid.from_string_list(list(reversed([
        ['', '', 'o'],
        ['o', 'x', 'o'],
        ['', '', '']
    ])), BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = LMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
        self.current_direction: Direction = Direction.A()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, LMino.BLOCK_TYPE)
        self.current_direction = self.current_direction.rotate_right()
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, LMino.BLOCK_TYPE)
        self.current_direction = self.current_direction.rotate_left()
    def get_grid(self) -> Grid:
        return self.current_shape
    def get_size(self) -> Size:
        return self.current_shape.get_size()
    def get_direction(self) -> Direction:
        return self.current_direction
    def super_rotate(
            self,
            current_direction: Direction,
            previous_direction: Direction,
            current_step: SuperRotationStep,
            current_relative_position: RelativePosition
        ) -> RelativePosition:
        return self.mino3x3.super_rotate(
                current_direction,
                previous_direction,
                current_step,
                current_relative_position
            )

class TMino(Mino):
    BLOCK_TYPE: Block = Block(7)
    SHAPE = Grid.from_string_list(list(reversed([
        ['', 'o', ''],
        ['o', 'x', 'o'],
        ['', '', '']
    ])), BLOCK_TYPE)
    def __init__(self) -> None:
        self.current_shape: Grid = TMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
        self.current_direction: Direction = Direction.A()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape, TMino.BLOCK_TYPE)
        self.current_direction = self.current_direction.rotate_right()
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape, TMino.BLOCK_TYPE)
        self.current_direction = self.current_direction.rotate_left()
    def get_grid(self) -> Grid:
        return self.current_shape
    def get_size(self) -> Size:
        return self.current_shape.get_size()
    def get_direction(self) -> Direction:
        return self.current_direction
    def super_rotate(
            self,
            current_direction: Direction,
            previous_direction: Direction,
            current_step: SuperRotationStep,
            current_relative_position: RelativePosition
        ) -> RelativePosition:
        return self.mino3x3.super_rotate(
                current_direction,
                previous_direction,
                current_step,
                current_relative_position
            )

class EmptyMino(Mino):
    def __init__(self) -> None:
        self.current_shape: Grid = Grid(Size(0, 0))
        self.current_direction: Direction = Direction.A()
    def rotate_right(self) -> None:
        pass
    def rotate_left(self) -> None:
        pass
    def get_grid(self) -> Grid:
        return self.current_shape
    def get_size(self) -> Size:
        return self.current_shape.get_size()
    def get_direction(self) -> Direction:
        return self.current_direction
    def super_rotate(
            self,
            current_direction: Direction,
            previous_direction: Direction,
            current_step: SuperRotationStep,
            current_relative_position: RelativePosition
        ) -> RelativePosition:
        return RelativePosition(0, 0)

@dataclass(slots=True)
class CurrentMino:
    mino: Mino
    position: Position = field(init=False)

    def __post_init__(self) -> None:
        self.position: Position = Tetris.INITIAL_POSITION.to_position(self.mino.get_size())

class EmptyMinoPileException(Exception):
    pass

class MinoPile:
    def __init__(self) -> None:
        mino_pile: list[Mino] = [IMino(), OMino(), SMino(), ZMino(), JMino(), LMino(), TMino()]
        self.pile: list[Mino] = sample(mino_pile, len(mino_pile))
    def pop_mino(self) -> Mino:
        if self.is_empty():
            raise EmptyMinoPileException()
        return self.pile.pop(0)
    def is_empty(self) -> bool:
        if len(self.pile) <= 0:
            return True
        return False

class NotBottomException(Exception):
    pass

class Tetris:
    INITIAL_POSITION: CenterPosition = CenterPosition(5, 19)
    FIELD_SIZE_X: int = 10
    FIELD_SIZE_Y: int = 20
    NEXT_NUMBER: int = 5
    def __init__(self) -> None:
        self.main_field: Grid = Grid(Size(Tetris.FIELD_SIZE_X, Tetris.FIELD_SIZE_Y*2))
        self.current_mino_pile: MinoPile = MinoPile()
        self.next_mino_pile: MinoPile = MinoPile()
        self.current_mino: CurrentMino = CurrentMino(EmptyMino())
        self.current_mino_size: Size = self.current_mino.mino.get_size()
    def _can_move(self, surrounding_grid: Grid, mino: Mino, position: PlotGridPosition) -> bool:
        """whether mino can move in surrounding grid

        Args:
            surrounding_grid (Grid): surrounding grid of mino
            mino (Mino): the shape of mino
            position (Position): position of mino in surrounding grid

        Returns:
            bool: whether mino can move
        """
        position_x = position.x
        position_y = position.y
        mino_grid = mino.get_grid().grid
        mino_grid_size_x = mino.get_grid().get_size().x
        mino_grid_size_y = mino.get_grid().get_size().y
        surrounding_grid_size_x = surrounding_grid.get_size().x
        surrounding_grid_size_y = surrounding_grid.get_size().y
        for y, column in enumerate(mino_grid):
            for x, block in enumerate(column):
                if not block.is_empty():
                    surrounding_grid_x = mino_grid_size_x - (surrounding_grid_size_x - position_x) + x
                    surrounding_grid_y = mino_grid_size_y - (surrounding_grid_size_y - position_y) + y
                    if not surrounding_grid.is_empty(Position(surrounding_grid_x, surrounding_grid_y)):
                        return False
        return True
    def move_right(self) -> None:
        position = self.current_mino.position
        new_position = Position(position.x, position.y)
        size = self.current_mino_size
        new_size = Size(size.x + 1, size.y)
        surrounding_grid = self.main_field.plot_grid(new_position, new_size)
        if not self._can_move(surrounding_grid, self.current_mino.mino, PlotGridPosition(2, 0)):
            return
        self.current_mino.position = Position(position.x + 1, position.y)
    def move_left(self) -> None:
        position = self.current_mino.position
        new_position = Position(position.x - 1, position.y)
        size = self.current_mino_size
        new_size = Size(size.x + 1, size.y)
        surrounding_grid = self.main_field.plot_grid(new_position, new_size)
        if not self._can_move(surrounding_grid, self.current_mino.mino, PlotGridPosition(0, 0)):
            return
        self.current_mino.position = Position(position.x - 1, position.y)
    def move_down(self) -> None:
        position_x = self.current_mino.position.x
        position_y = self.current_mino.position.y
        position = Position(position_x, position_y-1)
        size = self.current_mino_size
        new_size = Size(size.x, size.y + 1)
        surrounding_grid = self.main_field.plot_grid(position, new_size)
        if not self._can_move(surrounding_grid, self.current_mino.mino, PlotGridPosition(0, 1)):
            return
        self.current_mino.position = Position(position.x, position.y)
    def make_mino(self) -> None:
        self.current_mino = CurrentMino(self.current_mino_pile.pop_mino())
        self.current_mino_size = self.current_mino.mino.get_size()
        if self.current_mino_pile.is_empty():
            self.current_mino_pile = self.next_mino_pile
            self.next_mino_pile = MinoPile()
    def is_bottom(self) -> bool:
        position_x = self.current_mino.position.x
        position_y = self.current_mino.position.y
        position = Position(position_x, position_y-1)
        size = self.current_mino_size
        new_size = Size(size.x, size.y + 1)
        surrounding_grid = self.main_field.plot_grid(position, new_size)
        if not self._can_move(surrounding_grid, self.current_mino.mino, PlotGridPosition(0, 1)):
            return True
        return False
    def place_mino(self) -> None:
        if not self.is_bottom():
            raise NotBottomException()
        current_mino_grid = self.current_mino.mino.get_grid().grid
        current_x = self.current_mino.position.x
        current_y = self.current_mino.position.y
        for y, column in enumerate(current_mino_grid):
            for x, block in enumerate(column):
                if not block.is_empty():
                    self.main_field.add_block(Position(current_x + x, current_y + y), block)
