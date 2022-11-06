import arcade
from .constants import *
import numpy as np
from .player import Player
import collections
import random

class GridEnv(arcade.Window):
    """ Main application class. """

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
        self.num_players = 4
        self.starting_coords = [
            (int(ROW_COUNT/4), int(COLUMN_COUNT/4)),
            (int(ROW_COUNT/4), int(COLUMN_COUNT/4)*3),
            (int(ROW_COUNT/4)*3, int(COLUMN_COUNT/4)*3),
            (int(ROW_COUNT/4)*3, int(COLUMN_COUNT/4)),
        ]

        self.player_colors = [
            (arcade.color.YELLOW_ORANGE, arcade.color.SAPPHIRE_BLUE),
            (arcade.color.HOT_PINK, arcade.color.SAP_GREEN),
            (arcade.color.RED_ORANGE, arcade.color.TEAL),
            (arcade.color.GOLD, arcade.color.PURPLE_HEART),
        ]

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

        for player_num in range(self.num_players):
            # Set up the player
            self.player_list.append(Player(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING))

            # Set up player start
            player = self.player_list[player_num]
            start_x, start_y = self.starting_coords[player_num]
            player.initialize(start_x, start_y)
            c, r = player.pos
            try:
                for cc in range(c-1, c+2):
                    for rr in range(r-1, r+2):
                        self.grid[rr][cc] = OCCUPIED
                        self.player_grid[rr][cc] = player
                        player.push_zone((rr, cc))
            except:
                pass
        self.place_boost_bomb()

    def resync_grid_with_sprites(self):

        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                pos = r * COLUMN_COUNT + c
                if self.grid[r][c] == UNOCCUPIED:
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                elif self.grid[r][c] == BOMB:
                    self.grid_sprite_list[pos].color = arcade.color.BLACK
                elif self.grid[r][c] == BOOST:
                    self.grid_sprite_list[pos].color = arcade.color.PURPLE
                elif self.grid[r][c] == PASSED:
                    self.grid_sprite_list[pos].color = self.player_colors[self.player_list.index(self.player_grid[r][c])][0]
                elif self.grid[r][c] == OCCUPIED:
                    self.grid_sprite_list[pos].color = self.player_colors[self.player_list.index(self.player_grid[r][c])][1]
                else:
                    raise Exception("Unknown grid value")

    def on_draw(self):
        """ Render the screen. """

        # We should always start by clearing the window pixels
        self.clear()

        arcade.start_render()

        # Batch draw all the sprites
        self.grid_sprite_list.draw()

        for player in self.player_list:
            if (not player.reset): player.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player
        self.player_list.update()

        if not (False in [player.reset for player in self.player_list]):
            self.reset_game()
        else:
            for player in self.player_list:
                if not player.reset:
                    c, r = player.pos

                    if (c < 0 or r < 0 or COLUMN_COUNT <= c or ROW_COUNT <= r):
                        self.reset_player(player)
                    elif (player.reset):
                        pass
                    else:
                        player_cell = self.grid[r][c]

                        if player_cell == PASSED:

                            reset_targets = [p for p in self.player_list if p.pos == player.pos]

                            if len(reset_targets) > 1:
                                for target in reset_targets:
                                    self.reset_player(target)
                            if (player.validCollision()):
                                self.reset_player(player)
                        elif player_cell == OCCUPIED:
                            occupied_by = self.player_grid[r][c]
                            if player.lastUnoccupied and  occupied_by == player:
                                self.update_occupancy(player)
                                player.lastUnoccupied = False
                            elif occupied_by != player:
                                occupied_by.pop_zone((r,c))
                                self.grid[r][c] = PASSED
                                self.player_grid[r][c] = player
                                player.lastUnoccupied = True
                        elif player_cell == UNOCCUPIED:
                            self.grid[r][c] = PASSED
                            self.player_grid[r][c] = player
                            player.push_path((c,r))
                            player.lastUnoccupied = True
                        elif player_cell == BOMB:
                            self.reset_player(player)
                            self.grid[r][c] = PASSED
                            self.player_grid[r][c] = player
                        elif player_cell == BOOST:
                            self.grid[r][c] = PASSED
                            self.player_grid[r][c] = player
                            player.push_path((c,r))
                            player.lastUnoccupied = True
                            player.movement_speed+=1
                        else:
                            raise Exception("Unknown grid value")

                        player.change_x=0

            self.resync_grid_with_sprites()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
            print('Game Paused' if self.paused else "Game Unpaused")
            for player in self.player_list:
                if not player.reset: player.stopped = not player.stopped

        if not self.paused:
            if key == arcade.key.LEFT:
                self.player_list[0].change_x -= 1
            elif key == arcade.key.RIGHT:
                self.player_list[0].change_x += 1
            elif key == arcade.key.BACKSPACE:
                for player in self.player_list:
                    self.reset_player(player)
                self.reset_game()
            elif len(self.player_list) > 1:
                if key == arcade.key.A:
                    self.player_list[1].change_x -= 1
                elif key == arcade.key.D:
                    self.player_list[1].change_x += 1
    def reset(self):
        self.grid *= 0

        for player_num in range(self.num_players):
            player = self.player_list[player_num]
            start_x, start_y = self.starting_coords[player_num]
            player.initialize(start_x, start_y)
            c, r = player.pos
            try:
                for cc in range(c-1, c+2):
                    for rr in range(r-1, r+2):
                        self.grid[rr][cc] = OCCUPIED
                        self.player_grid[rr][cc] = player
                        player.push_zone((rr, cc))
            except:
                pass

        self.place_boost_bomb()
        self.resync_grid_with_sprites()

    def place_boost_bomb(self, boost_count = BOOST_COUNT, bomb_count=BOMB_COUNT):
        # place boosts
        while (boost_count>0):
            x = random.randrange(0, ROW_COUNT)
            y = random.randrange(0, COLUMN_COUNT)
            if(self.grid[x][y]==0):
                self.grid[x][y]= BOOST
                boost_count-=1

        # place bombs
        while (bomb_count>0):
            x = random.randrange(0, ROW_COUNT)
            y = random.randrange(0, COLUMN_COUNT)
            if(self.grid[x][y]==0):
                self.grid[x][y]= BOMB
                bomb_count-=1

    def reset_player(self, player):

        indices = np.where(self.player_grid == player)

        for i in range(len(indices[0])):
            # print(np.shape(indices))
            x = indices[0][i]
            y = indices[1][i]
            self.grid[x][y] = UNOCCUPIED
            self.player_grid[x][y] = None

        player.reset_player()

    def reset_game(self):
        print("Game Results:")
        for player in self.player_list:
            print(f"Player {player} earned {player.score} points!")
        print("\n")
        self.reset()


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
                cell = self.grid[r][c]
                occupied_by = self.player_grid[r][c]
                if (occupied_by == player and cell == PASSED) or cell == UNOCCUPIED:
                    self.grid[r][c] = OCCUPIED
                    self.player_grid[r][c] = player
                    player.push_zone((c,r))
                elif cell == -1:
                    self.grid[r][c] = UNOCCUPIED
                    self.player_grid[r][c] = None