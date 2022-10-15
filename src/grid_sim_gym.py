from utils import *
from constants import *
import random
import numpy as np
import collections
import arcade

x = random.randrange(0+3, ROW_COUNT-3)
y = random.randrange(0+3, COLUMN_COUNT-3)

class Player:
    def __init__(self, x, y):

        """ Player Movement Location """
        self.movement_speed = 10 # need to adjust it to scale or something
        self.center_x, self.center_y = grid_to_abs_pos((x,y))
        self.actual_x = self.center_x
        self.actual_y = self.center_y
        self.direction = random.randrange(0,4) # pick a random starting direction
        self.reset=False
        self.last_unoccupied = False

        """ Player Territory Information """
        self.pos = (x, y)
        self.path = set()
        self.zone = set()

        """ Player Score """
        self.score = -1

    def snap(self):
        x, y = abs_to_grid_pos((self.actual_x, self.actual_y))
        self.center_x, self.center_y = grid_to_abs_pos((x,y))
        self.pos = (int(x), int(y))

    def update(self, direction):

        self.direction += direction
        self.direction = (self.direction+4) % len(DIRECTIONS)

        self.old_pos = self.pos
        self.old_path = self.path
        self.old_zone = self.zone

        self.actual_x += DIRECTIONS[self.direction][0]*self.movement_speed
        self.actual_y += DIRECTIONS[self.direction][1]*self.movement_speed
        print(self.pos)
        self.snap()
        print(self.pos)

        x,y = self.pos
        if x < 0 or x>= ROW_COUNT or y < 0 or y>=COLUMN_COUNT:
            self.reset = True

    def pop_zone(self, pos):
        self.zone.discard(pos)
    def push_zone(self, pos):
        self.zone.add(pos)
        self.path.discard(pos)

    def push_path(self, pos):
        if pos not in self.zone: self.path.add(pos)

    def valid_collision(self):
        if (self.old_pos == self.pos):
            return False
        return True

    def reset_player(self):
        self.reset = True
        self.score = len(self.zone)
        self.stopped = True

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
        self.background_color = arcade.color.BLACK
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
        # arcade.run()

    def on_draw(self):
        arcade.start_render()
        self.grid_sprite_list.draw()

class PaperIoEnv:
    def __init__(self, render=False):
        self.grid = np.zeros((ROW_COUNT, COLUMN_COUNT))
        self.player_grid = np.full((ROW_COUNT, COLUMN_COUNT), None)
        self.player_list = []
        self.num_players = 4

        self.starting_coords = [
            (int(ROW_COUNT/4), int(COLUMN_COUNT/4)),
            (int(ROW_COUNT/4), int(COLUMN_COUNT/4)*3),
            (int(ROW_COUNT/4)*3, int(COLUMN_COUNT/4)*3),
            (int(ROW_COUNT/4)*3, int(COLUMN_COUNT/4)),
        ]
        self.setup()

        self.renderWindow = None
        if render:
            self.renderWindow = RenderWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    def setup(self):
        for player_num in range(self.num_players):
            start_x, start_y = self.starting_coords[player_num]
            self.player_list.append(Player(start_x, start_y))
            player = self.player_list[player_num]
            c, r = player.pos
            for cc in range(c-1, c + 2):
                for rr in range(r-1, r + 2):
                    self.grid[rr][cc] = OCCUPIED
                    self.player_grid[rr][cc] = player
                    player.push_zone((rr, cc))
        self.place_boost_bomb()

    # direction should be -1 or 1
    def step(self, direction):
        for player in range(len(self.player_list)):
            if player==0:
                self.player_list[player].update(direction)
            else:
                continue # TODO random movement of other players

        for player in self.player_list:
            if player.reset:
                self.reset_player(player)
            c, r = player.pos
            player_cell = self.grid[r][c]
            if player_cell == PASSED:
                reset_targets = [p for p in self.player_list if p.pos == player.pos]
                if len(reset_targets) > 1:
                    for target in reset_targets:
                        self.reset_player(target)
                if (player.valid_collision()):
                    self.reset_player(player)
            elif player_cell == OCCUPIED:
                occupied_by = self.player_grid[r][c]
                if player.last_unoccupied and  occupied_by == player:
                    self.update_occupancy(player)
                    player.last_unoccupied = False
                elif occupied_by != player:
                    occupied_by.pop_zone((r,c))
                    self.grid[r][c] = PASSED
                    self.player_grid[r][c] = player
                    player.last_unoccupied = True
            elif player_cell == UNOCCUPIED:
                self.grid[r][c] = PASSED
                self.player_grid[r][c] = player
                player.push_path((c,r))
                player.last_unoccupied = True
            elif player_cell == BOMB:
                self.reset_player(player)
                self.grid[r][c] = PASSED
                self.player_grid[r][c] = player
            elif player_cell == BOOST:
                self.grid[r][c] = PASSED
                self.player_grid[r][c] = player
                player.push_path((c,r))
                player.last_unoccupied = True
                player.movement_speed+=1
            else:
                raise Exception("Unknown grid value")

        if self.renderWindow:
            self.render()
        return self.player_list[0], self.player_grid

    def reset(self):
        print("Game Results:")
        for player in self.player_list:
            print(f"Player {player} earned {player.score} points!")
        print("\n")

        self.grid *= 0
        self.player_grid = np.full((ROW_COUNT, COLUMN_COUNT), None)
        self.player_list = []
        self.setup()

    def render(self):
        self.renderWindow.render(self.grid, self.player_grid, self.player_list)

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
            x = indices[0][i]
            y = indices[1][i]
            self.grid[x][y] = UNOCCUPIED
            self.player_grid[x][y] = None

        player.reset_player()

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

if __name__ == "__main__":
    paperio = PaperIoEnv(render=True)
    while True:
        for i in range(10):
            paperio.step(0)
        paperio.step(1)

    # paperio.render()
