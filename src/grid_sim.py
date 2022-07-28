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
WIDTH = 10
HEIGHT = 10

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "yoooo"

MOVEMENT_SPEED = 3

TEMP = -1
UNOCCUPIED = 0
PASSED = 1
OCCUPIED = 2

DIRECTIONS = ((0,1), (1,0), (0,-1), (-1,0))

class Player(arcade.Sprite):
    """ Player Class """

    def initialize(self, x, y):

        """ Player Movement Location """
        self.center_x = x * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        self.center_y = y * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)

        self.actual_x = self.center_x
        self.actual_y = self.center_y
        self.direction = random.randrange(0,4) # pick a random starting direction
        self.reset=False
        self.lastUnoccupied = False

        """ Player Territory Information """
        self.pos = (x, y)
        self.path = set()
        self.zone = set()

        """ For Testing Purposes """
        self.stopped = False
        

    def snap(self):
        x = (self.actual_x - (WIDTH / 2 + MARGIN))// (WIDTH + MARGIN)
        y = (self.actual_y - (HEIGHT / 2 + MARGIN))// (HEIGHT + MARGIN)
        self.center_x = int(x) * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        self.center_y = int(y) * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.pos = (int(x), int(y))

    def update(self):
        """ Move the player """

        self.direction += int(self.change_x)
        self.direction = (self.direction+4) % len(DIRECTIONS)

        self.old_pos = self.pos
        self.old_path = self.path
        self.old_zone = self.zone

        self.actual_x += DIRECTIONS[self.direction][0]*MOVEMENT_SPEED * (not self.stopped)
        self.actual_y += DIRECTIONS[self.direction][1]*MOVEMENT_SPEED * (not self.stopped)
        self.snap()

        # if (self.old_pos != self.pos or self.old_path != self.path or self.old_zone != self.zone):
        #     print(f"pos\t{self.pos}")
        #     print(f"path\t{self.path}")
        #     print(f"zone\t{self.zone}")

        x,y = self.pos
        if x < 0 or x>= ROW_COUNT or y < 0 or y>=COLUMN_COUNT:
            self.reset = True
    
    def pop_zone(self, pos):
        self.zone.discard(pos)
    def push_zone(self, pos):
        self.zone.add(pos)
        self.path.discard(pos)
    
    def pop_path(self, pos):
        self.path.discard(pos)
    def push_path(self, pos):
        if pos not in self.zone: self.path.add(pos)

    def validCollision(self):
        if (self.old_pos == self.pos):
            return False
        
        return True

    def reset_player(self):
        self.reset = True
        self.pos = None
        self.path = None
        self.zone = None
        

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """ Set up the application. """
        super().__init__(width, height, title)

        self.grid = np.zeros((ROW_COUNT, COLUMN_COUNT))
        self.player_grid = np.full((ROW_COUNT, COLUMN_COUNT), None)

        # Set the window's background color
        self.background_color = arcade.color.BLACK
        # Create a spritelist for batch drawing all the grid sprites
        self.grid_sprite_list = arcade.SpriteList()

        self.player_list = None

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

        """ For Testing Purposes """
        self.paused = False

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_list.append(Player(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING))


        player_num = 0
        player = self.player_list[player_num]
        player.initialize(20, 20)
        c, r = player.pos
        try:
            for cc in range(c-1, c+2):
                for rr in range(r-1, r+2):
                    self.grid[rr][cc] = OCCUPIED
                    self.player_grid[rr][cc] = player
                    player.push_zone((rr, cc))
        except:
            pass

    def resync_grid_with_sprites(self):

        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                pos = r * COLUMN_COUNT + c
                if self.grid[r][c] == UNOCCUPIED:
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                elif self.grid[r][c] == PASSED:
                    self.grid_sprite_list[pos].color = arcade.color.GREEN
                elif self.grid[r][c] == OCCUPIED:
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
        if not (False in [player.reset for player in self.player_list]):
            self.reset()
        else:
            player_num = 0
            player = self.player_list[player_num]
            c, r = player.pos
            player_cell = self.grid[r][c]
            if player_cell == PASSED:
                if (player.validCollision()):
                    for (x,y) in np.concatenate(([player.pos], list(player.path), list(player.zone))):
                        self.grid[x][y] = UNOCCUPIED
                        self.player_grid[x][y] = None
                    player.reset_player()
            elif player_cell == OCCUPIED:
                if player.lastUnoccupied:
                    self.update_occupancy(player)
                    player.lastUnoccupied = False
            elif player_cell == UNOCCUPIED:
                self.grid[r][c] = PASSED
                self.player_grid[r][c] = player
                player.push_path((c,r))
                player.lastUnoccupied = True
            else:
                raise Exception("Unknown grid value")
            
            player.change_x=0

                
            self.resync_grid_with_sprites()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
            print('Game Paused' if self.paused else "Game Unpaused")
            for player_num in range(len(self.player_list)):
                self.player_list[player_num].stopped = not self.player_list[player_num].stopped
        
        if not self.paused:
            if key == arcade.key.LEFT:
                self.player_list[0].change_x -= 1
            elif key == arcade.key.RIGHT:
                self.player_list[0].change_x += 1
            elif len(self.player_list) > 0:
                if key == arcade.key.A:
                    self.player_list[1].change_x -= 1
                elif key == arcade.key.D:
                    self.player_list[1].change_x += 1

    def reset(self):

        player_num = 0
        player = self.player_list[player_num]

        player.initialize(20, 20)
        self.grid *= 0
        self.resync_grid_with_sprites()
        c, r = player.pos
        try:
            for cc in range(c-1, c+2):
                for rr in range(r-1, r+2):
                    self.grid[rr][cc] = OCCUPIED
                    self.player_grid[rr][cc] = player
                    player.push_zone((rr, cc))
        except:
            pass

    def update_occupancy(self, player):
        queue = collections.deque([])
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if (r in [0, ROW_COUNT-1] or c in [0, COLUMN_COUNT-1]) and self.grid[r][c] == UNOCCUPIED:
                    queue.append((r, c))
        while queue:
            r, c = queue.popleft()
            if 0<=r<ROW_COUNT and 0<=c<COLUMN_COUNT and self.grid[r][c] == UNOCCUPIED:
                self.grid[r][c] = TEMP
                queue.extend([(r-1, c),(r+1, c),(r, c-1),(r, c+1)])
        
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if self.grid[r][c] == UNOCCUPIED or self.grid[r][c] == PASSED:
                    self.grid[r][c] = OCCUPIED
                    self.player_grid[r][c] = player
                    player.push_zone((c,r))
                elif self.grid[r][c] == -1:
                    self.grid[r][c] = UNOCCUPIED
                    self.player_grid[r][c] = None
                        
        


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
