import arcade
import random

# https://api.arcade.academy/en/latest/examples/array_backed_grid_sprites_1.html#array-backed-grid-sprites-1
# https://api.arcade.academy/en/2.6.0/examples/sprite_move_keyboard.html

# Set how many rows and columns we will have
ROW_COUNT = 40
COLUMN_COUNT = 40

SPRITE_SCALING = 0.5

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 20

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "yoooo"

MOVEMENT_SPEED = 3

class Player(arcade.Sprite):
    """ Player Class """

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

        gridx = (self.center_x - (WIDTH / 2 + MARGIN))// (WIDTH + MARGIN)
        gridy = (self.center_y - (HEIGHT / 2 + MARGIN))// (HEIGHT + MARGIN)
        self.pos = (int(gridx), int(gridy))

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)

        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        # This array can be altered later to contain 0 or 1
        # to show a white or green cell.
        #
        # A 4 x 4 grid would look like this
        #
        # grid = [
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        # ]
        # We can quickly build a grid with python list comprehension
        # self.grid = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
        # Making the grid with loops:
        self.grid = []
        for row in range(ROW_COUNT):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(COLUMN_COUNT):
                self.grid[row].append(0)  # Append a cell

        # Set the window's background color
        self.background_color = arcade.color.BLACK
        # Create a spritelist for batch drawing all the grid sprites
        self.grid_sprite_list = arcade.SpriteList()

        self.player_list = None
        self.player_sprite = None

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING)
        x = random.randrange(0, ROW_COUNT)
        y = random.randrange(0, COLUMN_COUNT)
        self.player_sprite.center_x = x * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        self.player_sprite.center_y = y * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.player_sprite.pos= (x, y) # should be randomized later on
        self.player_list.append(self.player_sprite)

    def resync_grid_with_sprites(self):
        """
        Update the color of all the sprites to match
        the color/stats in the grid.

        We look at the values in each cell.
        If the cell contains 0 we assign a white color.
        If the cell contains 1 we assign a green color.
        """
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # We need to convert our two dimensional grid to our
                # one-dimensional sprite list. For example a 10x10 grid might have
                # row 2, column 8 mapped to location 28. (Zero-basing throws things
                # off, but you get the idea.)
                # ALTERNATIVELY you could set self.grid_sprite_list[pos].texture
                # to different textures to change the image instead of the color.
                pos = row * COLUMN_COUNT + column
                if self.grid[row][column] == 0:
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                else:
                    self.grid_sprite_list[pos].color = arcade.color.GREEN

    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        arcade.start_render()

        # Batch draw all the sprites
        self.grid_sprite_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player
        self.player_list.update()
        c, r = self.player_sprite.pos
        self.grid[r][c] = 1
        self.resync_grid_with_sprites()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # If the player presses a key, update the speed
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        # If a player releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
