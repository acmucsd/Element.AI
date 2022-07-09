import arcade
import random
import numpy as np
import collections
# https://api.arcade.academy/en/latest/examples/array_backed_grid_sprites_1.html#array-backed-grid-sprites-1
# https://api.arcade.academy/en/2.6.0/examples/sprite_move_keyboard.html

# Set how many rows and columns we will have
ROW_COUNT = 80
COLUMN_COUNT = 80

SPRITE_SCALING = 0.5

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 8
HEIGHT = 5

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "yoooo"

MOVEMENT_SPEED = 3

UNOCCUPIED = 0
PASSED = 1
OCCUPIED = 2

DIRECTIONS = ((0,1), (1,0), (0,-1), (-1,0))

class Player(arcade.Sprite):
    """ Player Class """

    def initialize(self):
        x = random.randrange(0, ROW_COUNT)
        y = random.randrange(0, COLUMN_COUNT)
        self.center_x = x * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        self.center_y = y * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.pos= (x, y)
        self.actual_x = self.center_x
        self.actual_y = self.center_y
        self.direction = random.randrange(0,4) # pick a random starting direction
        self.reset=False
        self.lastUnoccupied = False
        self.path = set()

    def snap(self):
        x = (self.actual_x - (WIDTH / 2 + MARGIN))// (WIDTH + MARGIN)
        y = (self.actual_y - (HEIGHT / 2 + MARGIN))// (HEIGHT + MARGIN)
        self.center_x = int(x) * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        self.center_y = int(y) * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.pos = (int(x), int(y))
        self.path.add(self.pos)

    def update(self):
        """ Move the player """

        self.direction += int(self.change_x)
        self.direction = (self.direction+4) % len(DIRECTIONS)

        self.actual_x += DIRECTIONS[self.direction][0]*MOVEMENT_SPEED
        self.actual_y += DIRECTIONS[self.direction][1]*MOVEMENT_SPEED
        self.snap()

        x,y = self.pos
        if x < 0 or x>= ROW_COUNT or y < 0 or y>=COLUMN_COUNT:
            self.reset = True
        

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)

        self.grid = np.zeros((ROW_COUNT, COLUMN_COUNT))

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
        self.player_sprite.initialize()
        self.player_list.append(self.player_sprite)
        c, r = self.player_sprite.pos
        try:
            for cc in range(c-1, c + 2):
                for rr in range(r-1, r + 2):
                    self.grid[rr][cc] = OCCUPIED
        except:
            pass

    def resync_grid_with_sprites(self):

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                pos = row * COLUMN_COUNT + column
                if self.grid[row][column] == UNOCCUPIED:
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                elif self.grid[row][column] == PASSED:
                    self.grid_sprite_list[pos].color = arcade.color.GREEN
                elif self.grid[row][column] == OCCUPIED:
                    self.grid_sprite_list[pos].color = arcade.color.RED
                else:
                    raise Exception("Unknown grid value")

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
        if self.player_sprite.reset:
            self.reset()
        else:
            c, r = self.player_sprite.pos
            if self.grid[r][c] == PASSED:
                pass # handle colision here
            elif self.grid[r][c] == OCCUPIED:
                if self.player_sprite.lastUnoccupied:
                    self.update_occupancy()
                    self.player_sprite.lastUnoccupied = False
            elif self.grid[r][c] == UNOCCUPIED:
                self.grid[r][c] = PASSED
                self.player_sprite.lastUnoccupied = True
            else:
                raise Exception("Unknown grid value")
                
            self.resync_grid_with_sprites()
            self.player_sprite.change_x=0

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT:
            self.player_sprite.change_x -= 1
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x += 1

    def reset(self):
        self.player_sprite.initialize()
        self.grid = self.grid*0
        self.resync_grid_with_sprites()
        c, r = self.player_sprite.pos
        try:
            for cc in range(c-1, c + 2):
                for rr in range(r-1, r + 2):
                    self.grid[rr][cc] = OCCUPIED
        except:
            pass

    def update_occupancy(self):
        queue = collections.deque([])
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if (r in [0, ROW_COUNT-1] or c in [0, COLUMN_COUNT-1]) and self.grid[r][c] == UNOCCUPIED:
                    queue.append((r, c))
        while queue:
            r, c = queue.popleft()
            if 0<=r<ROW_COUNT and 0<=c<COLUMN_COUNT and self.grid[r][c] == UNOCCUPIED:
                self.grid[r][c] = -1
                queue.extend([(r-1, c),(r+1, c),(r, c-1),(r, c+1)])
        
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if self.grid[r][c] == UNOCCUPIED or self.grid[r][c] == PASSED:
                    self.grid[r][c] = OCCUPIED
                elif self.grid[r][c] == -1:
                    self.grid[r][c] = UNOCCUPIED
                        
        


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
