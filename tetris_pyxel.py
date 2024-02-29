import copy
import pyxel
from dataclasses import dataclass, field
from typing import ClassVar, Type

import collections.abc as cabc
import contextlib
import sys

@dataclass(frozen=True, slots=True)
class DropTimer:
    DEFAULT_DROP_PERIOD: ClassVar[int] = 60
    DEFAULT_DROP_SPEED: ClassVar[int] = 1
    drop_period: int = field(init=False, default_factory=int)
    timer: int = field(default=0)
    _speed: int = field(default=DEFAULT_DROP_SPEED)
    def __post_init__(self):
        object.__setattr__(self, "drop_period", DropTimer.DEFAULT_DROP_PERIOD/self._speed)
    def should_drop(self):
        return self.timer >= self.drop_period

@dataclass(frozen=True)
class DropDelay:
    MAX_TIME: ClassVar[int] = 30
    MAX_COUNT: ClassVar[int] = 8
    timer: int = field(default=0)
    reset_count: int = field(default=0)
    def should_place(self) -> bool:
        return (self.timer >= DropDelay.MAX_TIME) or (self.reset_count >= DropDelay.MAX_COUNT)

class App:
    NEXT_NUMBER: ClassVar[int] = 5
    def __init__(self,
                 tetris_class: Type['Tetris'], 
                 position_class: Type['Position'],
                 empty_mino_class: Type['EmptyMino'], 
                 block_class: Type['Block']
                 ): # 初期化
        pyxel.init(480, 360, fps=60)
        pyxel.load('my_resource.pyxres')
        self.tetris = tetris_class()
        self.Position = position_class
        self.EmptyMino = empty_mino_class
        self.Block = block_class
        self.tetris.make_mino()
        self.speed = DropTimer.DEFAULT_DROP_SPEED
        self.drop_timer = DropTimer(_speed=self.speed)
        self.delay = DropDelay()
        pyxel.run(self.update, self.draw) # アプリケーションの実行

    def update(self): # フレームの更新処理
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_RIGHT, hold=12, repeat=2):
            if self.tetris.move_right() and self.tetris.is_bottom():
                self.reset_time()
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_LEFT, hold=12, repeat=2):
            if self.tetris.move_left() and self.tetris.is_bottom():
                self.reset_time()
        if pyxel.btnp(pyxel.KEY_DOWN, hold=1, repeat=5):
            if self.tetris.move_down():
                self.reset_time()
        if pyxel.btnp(pyxel.KEY_Z):
            if self.tetris.rotate_left():
                self.reset_time()
        if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_UP):
            if self.tetris.rotate_right():
                self.reset_time()
        if pyxel.btnp(pyxel.KEY_C):
            self.tetris.hold()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.tetris.hard_drop()
            self.drop_timer = DropTimer(_speed=self.speed)
        self.drop()

    def drop(self):
        if self.tetris.is_bottom():
            if self.delay.should_place():
                self.tetris.place_mino()
                self.drop_timer = DropTimer(_speed=self.speed)
                self.delay = DropDelay()
            else:
                self.delay = DropDelay(timer=self.delay.timer+1, reset_count=self.delay.reset_count)
        if not self.tetris.is_bottom():
            if self.delay.timer > 0:
                self.delay = DropDelay(reset_count=self.delay.reset_count+1)
                self.drop_timer = DropTimer(_speed=self.speed)
        if self.drop_timer.should_drop():
            self.drop_timer = DropTimer(_speed=self.speed)
            if not self.tetris.is_bottom():
                self.tetris.move_down()
        else:
            self.drop_timer = DropTimer(self.drop_timer.timer+1, self.speed)
    def is_game_over(self) -> bool:
        for y, column in enumerate(self.tetris.main_field.grid):
            for x, block in enumerate(column):
                if not block.is_empty():
                    current_position = self.Position(x, y)
                    if (current_position == self.Position(3, 20) or
                           current_position == self.Position(4, 20) or
                           current_position == self.Position(5, 20) or
                           current_position == self.Position(6, 20) or
                           current_position == self.Position(3, 21) or
                           current_position == self.Position(4, 21) or
                           current_position == self.Position(5, 21) or
                           current_position == self.Position(6, 21)
                           ):
                        return True
        return False
    def reset_time(self) -> None:
        self.drop_timer = DropTimer(_speed=self.speed)
        if self.tetris.is_bottom():
            self.delay = DropDelay(reset_count=self.delay.reset_count+1)
    def draw(self): # 描画処理
        pyxel.cls(0)
        pyxel.blt(10, 10, 0, 0, 0, 16, 16)
        self.draw_main_field()
        self.draw_next()
        self.draw_hold()
        pyxel.text(0, 0, f'{self.drop_timer.timer}/{self.drop_timer.drop_period}, {self.drop_timer.should_drop()}', 7)
        pyxel.text(0, 20, f'{self.delay.timer}, {self.delay.reset_count}, {self.delay.should_place()}', 7)

    def draw_main_field(self):
        grid_position = {'x': 160, 'y': 16,}
        new_grid = copy.deepcopy(self.tetris.main_field)
        mino_position_x = self.tetris.current_mino.position.x
        mino_position_y = self.tetris.current_mino.position.y
        mino_grid = self.tetris.current_mino.mino.get_grid().grid
        # add ghost block
        for y, column in enumerate(mino_grid):
            for x, block in enumerate(column):
                if not block.is_empty():
                    ghost_block_position = self.tetris.get_ghost_block()
                    new_grid.add_block(
                        self.Position(ghost_block_position.x+x, ghost_block_position.y+y),
                        self.Block(block._block_type+8)
                        )
        for y, column in enumerate(mino_grid):
            for x, block in enumerate(column):
                if not block.is_empty():
                    new_grid.add_block(self.Position(mino_position_x+x, mino_position_y+y), block)
        for y, column in enumerate(reversed(new_grid.grid)):
            for x, block in enumerate(column):
                if block.is_empty() and y <= 19:
                    continue
                block_type = block._block_type
                pyxel.blt(
                    grid_position['x']+x*16,
                    grid_position['y']+(y-19)*16,
                    0,
                    (block_type % 4)*16,
                    (block_type // 4)*16,
                    16,
                    16
                    )
    def draw_next(self):
        grid_position = {'x': 340, 'y': 100,}
        grid_margin_size = {'x': 0, 'y': 5}
        next_minos = self.tetris.current_mino_pile.pile + self.tetris.next_mino_pile.pile
        for i in range(App.NEXT_NUMBER):
            current_mino = next_minos[i]
            for y, column in enumerate(reversed(current_mino.get_grid().grid)):
                for x, block in enumerate(column):
                    if not block.is_empty():
                        next_grid_position = {
                            'x': grid_position['x']+grid_margin_size['x']*(i-1),
                            'y': grid_position['y']+grid_margin_size['y']*(i-1)+16*3*(i-1),
                        }
                        block_type = block._block_type
                        pyxel.blt(
                            next_grid_position['x']+x*16,
                            next_grid_position['y']+y*16,
                            0, (block_type % 4)*16,
                            (block_type // 4)*16,
                            16,
                            16
                            )
    def draw_hold(self):
        grid_position = {'x': 80, 'y': 32,}
        hold_mino = self.tetris.hold_mino
        if hold_mino == self.EmptyMino():
            return
        for y, column in enumerate(reversed(hold_mino.get_grid().grid)):
            for x, block in enumerate(column):
                if not block.is_empty():
                    block_type = block._block_type
                    pyxel.blt(
                        grid_position['x']+x*16,
                        grid_position['y']+y*16,
                        0,
                        (block_type % 4)*16,
                        (block_type // 4)*16,
                        16,
                        16
                        )

@contextlib.contextmanager
def print_exception() -> cabc.Iterator[None]:
    try:
        yield
    except Exception as error:
        print("Exception passthrough:", error)
        raise

def preload() -> None:
    module_paths = ("main.py", '')
    for path in module_paths:
        if path == '': break
        with open(path):  # pylint: disable=unspecified-encoding
            pass

@print_exception()
def main() -> int:
    preload()
    from main import Tetris, Position, EmptyMino, Block

    App(Tetris, Position, EmptyMino, Block)

    return  0

if __name__ == "__main__":
    sys.exit(main())