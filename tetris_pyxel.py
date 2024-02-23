import copy
import pyxel
from typing import ClassVar
from main import Tetris, Position

class App:
    NEXT_NUMBER: ClassVar[int] = 5
    def __init__(self): # 初期化
        pyxel.init(480, 360)
        pyxel.load('my_resource.pyxres')
        self.tetris = Tetris()
        self.tetris.make_mino()
        pyxel.run(self.update, self.draw) # アプリケーションの実行

    def update(self): # フレームの更新処理
        if pyxel.btnp(pyxel.KEY_RIGHT, hold=1, repeat=5):
            self.tetris.move_right()
        if pyxel.btnp(pyxel.KEY_LEFT, hold=1, repeat=5):
            self.tetris.move_left()
        if pyxel.btnp(pyxel.KEY_DOWN, hold=1, repeat=5):
            self.tetris.move_down()
        if pyxel.btnp(pyxel.KEY_Z):
            self.tetris.rotate_left()
        if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_UP):
            self.tetris.rotate_right()
        if pyxel.btnp(pyxel.KEY_C):
            self.tetris.hold()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.tetris.hard_drop()

    def draw(self): # 描画処理
        pyxel.cls(0)
        pyxel.blt(10, 10, 0, 0, 0, 16, 16)
        self.draw_main_field()
        self.draw_next()

    def draw_main_field(self):
        grid_position = {'x': 160, 'y': 16,}
        new_grid = copy.deepcopy(self.tetris.main_field)
        mino_position_x = self.tetris.current_mino.position.x
        mino_position_y = self.tetris.current_mino.position.y
        mino_grid = self.tetris.current_mino.mino.get_grid().grid
        for y, column in enumerate(mino_grid):
            for x, block in enumerate(column):
                if not block.is_empty():
                    new_grid.add_block(Position(mino_position_x+x, mino_position_y+y), block)
        print(new_grid)
        for y, column in enumerate(reversed(new_grid.grid)):
            if y <= 19:
                continue
            for x, block in enumerate(column):
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

App()
