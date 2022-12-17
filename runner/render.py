import arcade
from .constants import *

class RenderWindow(arcade.Window):
    def __init__(self, width, height, title):
        """ Set up the application. """
        super().__init__(width, height, title)
        self.player_colors = [
            (arcade.color.YELLOW_ORANGE, arcade.color.SAPPHIRE_BLUE),
            (arcade.color.HOT_PINK, arcade.color.SAP_GREEN),
            (arcade.color.RED_ORANGE, arcade.color.TEAL),
            (arcade.color.GOLD, arcade.color.PURPLE_HEART),
        ]
        self.background_color = arcade.color.WHITE_SMOKE
        self.grid_sprite_list = arcade.SpriteList()
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

    def render(self, grid, player_grid, player_list):
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                pos = r * COLUMN_COUNT + c
                if grid[r][c] == UNOCCUPIED:
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                elif grid[r][c] == BOMB:
                    self.grid_sprite_list[pos].color = arcade.color.BLACK
                elif grid[r][c] == BOOST:
                    self.grid_sprite_list[pos].color = arcade.color.PURPLE
                elif grid[r][c] == PASSED:
                    self.grid_sprite_list[pos].color = self.player_colors[player_list.index(player_grid[r][c])][0]
                elif grid[r][c] == OCCUPIED:
                    self.grid_sprite_list[pos].color = self.player_colors[player_list.index(player_grid[r][c])][1]
                else:
                    raise Exception("Unknown grid value")

        self.on_draw()
        arcade.finish_render()
        arcade.run()

    def on_draw(self):
        arcade.start_render()
        self.grid_sprite_list.draw()