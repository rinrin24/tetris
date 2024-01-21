from abc import abstractmethod, ABCMeta

class Mino(metaclass=ABCMeta):
    @abstractmethod
    def rotate_right(self) -> None:
        raise NotImplementedError()
    def rotate_left(self) -> None:
        raise NotImplementedError()

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

class SMino(Mino):
    SHAPE = [
        ['', 'o', 'o'],
        ['o', 'x', ''],
        ['', '', '']
    ]
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape)

class ZMino(Mino):
    SHAPE = [
        ['o', 'o', ''],
        ['', 'x', 'o'],
        ['', '', '']
    ]
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape)

class JMino(Mino):
    SHAPE = [
        ['o', '', ''],
        ['o', 'x', 'o'],
        ['', '', '']
    ]
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape)

class LMino(Mino):
    SHAPE = [
        ['', '', 'o'],
        ['o', 'x', 'o'],
        ['', '', '']
    ]
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape)

class TMino(Mino):
    SHAPE = [
        ['', 'o', ''],
        ['o', 'x', 'o'],
        ['', '', '']
    ]
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = SMino.SHAPE
        self.mino3x3: Mino3x3 = Mino3x3()
    def rotate_right(self) -> None:
        self.current_shape = self.mino3x3.rotate_right(self.current_shape)
    def rotate_left(self) -> None:
        self.current_shape = self.mino3x3.rotate_left(self.current_shape)

class OMino(Mino):
    SHAPE = [
        ['o', 'o'],
        ['o', 'o']
    ]
    def __init__(self) -> None:
        self.current_shape: list[list[str]] = OMino.SHAPE
    def rotate_right(self) -> None:
        return
    def rotate_left(self) -> None:
        return

class IMino(Mino):
    SHAPE = [
        ['', '', '', ''],
        ['o', 'o', 'o', 'o'],
        ['', '', '', ''],
        ['', '', '', '']
    ]
    def __init__(self) -> None:
        self.current_shape = IMino.SHAPE
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
