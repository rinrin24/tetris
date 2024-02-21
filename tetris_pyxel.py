import copy
import pyxel
from main import Tetris, Position

class App:
    def __init__(self): # 初期化
        pyxel.init(480, 360)
        pyxel.load('my_resource.pyxres')
        self.tetris = Tetris()
        self.tetris.make_mino()
        pyxel.run(self.update, self.draw) # アプリケーションの実行

    def update(self): # フレームの更新処理
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.tetris.move_right()
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.tetris.move_left()
        if pyxel.btnp(pyxel.KEY_DOWN, hold=1, repeat=5):
            self.tetris.move_down()
        if pyxel.btnp(pyxel.KEY_Z):
            self.tetris.rotate_left()
        if pyxel.btnp(pyxel.KEY_X):
            self.tetris.rotate_right()
        if pyxel.btnp(pyxel.KEY_C):
            self.tetris.hold()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.tetris.hard_drop()

    def draw(self): # 描画処理
        pyxel.cls(0)
        pyxel.blt(10, 10, 0, 0, 0, 16, 16)
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

App()
