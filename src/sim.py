"""
Paper.IO++ Simulator
"""
import arcade
import math

SPRITE_SCALING = 0.1

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Paper.IO++ Simulator"

MOVEMENT_SPEED = 5
ANGLE_SPEED = 5


class Player(arcade.Sprite):
    """ Player class """

    def __init__(self, image, scale):
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0

    def update(self):
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the agent
        self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("../assets/ice-cube.png", SPRITE_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites
        self.player_list.update()

        x, y = self.player_list.center
        
        if x < 0 and y > SCREEN_HEIGHT: # top left -> bottom right
            self.player_list[0].center_x = SCREEN_WIDTH
            self.player_list[0].center_y = 0

        elif x < 0 and y < 0: # bottom left -> top right
            self.player_list[0].center_x = SCREEN_WIDTH
            self.player_list[0].center_y = SCREEN_HEIGHT

        elif x > SCREEN_WIDTH and y > SCREEN_HEIGHT: # top right -> bottom left
            self.player_list[0].center_x = 0
            self.player_list[0].center_y = 0

        elif x > SCREEN_WIDTH and y < 0: # bottom right -> top left
            self.player_list[0].center_x = 0
            self.player_list[0].center_y = SCREEN_HEIGHT

        elif x > SCREEN_WIDTH:
            self.player_list[0].center_x = 0
        elif x < 0:
            self.player_list[0].center_x = SCREEN_WIDTH
        elif y > SCREEN_HEIGHT:
            self.player_list[0].center_y = 0
        elif y < 0:
            self.player_list[0].center_y = SCREEN_HEIGHT

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Forward/back
        if key == arcade.key.UP:
            self.player_sprite.speed = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.speed = -MOVEMENT_SPEED

        # Rotate left/right
        elif key == arcade.key.LEFT:
            self.player_sprite.change_angle = ANGLE_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = -ANGLE_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.set_background_color(arcade.color.WHITE_SMOKE)
    arcade.run()


if __name__ == "__main__":
    main()