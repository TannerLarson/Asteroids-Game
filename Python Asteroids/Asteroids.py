"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others

This program implements the asteroids game.
"""
import arcade
import random
import math
from abc import ABC, abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 3
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 33

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 10

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 5




# Defines a point
class Point():
    
    # Default constructor with option to change initialization
    def __init__(self, xIn = 0.0, yIn = 0.0):
        self.x = xIn
        self.y = yIn
        
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, xIn):
        self._x = xIn
        
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, yIn):
        self._y = yIn
        
        
# Defines a velocity
class Velocity():
    
    def __init__(self, dxIn = 0.0, dyIn = 0.0):
        self.dx = dxIn
        self.dy = dyIn
        
    @property
    def dx(self):
        return self._dx
    
    @dx.setter
    def dx(self, dxIn):
        self._dx = dxIn
        
    @property
    def dy(self):
        return self._dy
    
    @dy.setter
    def dy(self, dyIn):
        self._dy = dyIn
        


# Defines a flying object
class FlyingObject(ABC):
    
    # Default init, gives option to initialize flying object to something else
    def __init__(self, centerIn = Point(), velocityIn = Velocity(), radiusIn = 0.0):
        self.center = Point()
        self.velocity = Velocity()
        self.center.x = centerIn.x
        self.center.y = centerIn.y
        self.velocity.dx = velocityIn.dx
        self.velocity.dy = velocityIn.dy
        self.angle = 0
        self.radius = radiusIn
        self.alive = True
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, radiusIn):
        self._radius = radiusIn
        
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, angleIn):
        self._angle = angleIn
        
    # Wraps flying objects that are off scren
    def wrap(self):
        if self.center.x > SCREEN_WIDTH + 30:
            self.center.x = 0
        if self.center.x < 0 - 30:
            self.center.x = SCREEN_WIDTH
        if self.center.y > SCREEN_HEIGHT + 30:
            self.center.y = 0
        if self.center.y < 0 - 30:
            self.center.y = SCREEN_HEIGHT
    
    # Move my flying object
    def advance(self):
        self.wrap()
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    
    # Make sure all subclasses have a draw funtion
    @abstractmethod
    def draw(self):
        pass


class Ship(FlyingObject):
    
    def __init__(self):
        super().__init__(Point(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), Velocity(), SHIP_RADIUS)
        
    def draw(self):
        img = "images/playerShip1_Orange.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent
        x = self.center.x
        y = self.center.y
        angle = self.angle

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        
    def rotateLeft(self):
        self.angle += SHIP_TURN_AMOUNT
        
    def rotateRight(self):
        self.angle -= SHIP_TURN_AMOUNT
        
    def thrust(self):
        self.velocity.dx += SHIP_THRUST_AMOUNT * math.cos(math.radians(self.angle + 90))
        self.velocity.dy += SHIP_THRUST_AMOUNT * math.sin(math.radians(self.angle + 90))


# Defines a Bullet which is a flying object
class Bullet(FlyingObject):
    
    # Default constructor
    def __init__(self, p = Point(), v = Velocity()):
        super().__init__(p, v, BULLET_RADIUS)
        self.lifetime = 60
        
    # Draw a small cirlce for my bullet
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, arcade.color.WHITE)
        if self.lifetime <= 0:
            self.alive = False
        else:
            self.lifetime -= 1
    
    # Give bullet a direction and magnitude
    def fire(self, angle):
        self.velocity.dx += BULLET_SPEED * math.cos(math.radians(angle + 90))
        self.velocity.dy += BULLET_SPEED * math.sin(math.radians(angle + 90))


class Asteroid(FlyingObject):
    
    def __init__(self, x = Point(), v = Velocity(), r = 5):
        super().__init__(x, v, r)


class Big(Asteroid):
    
    def __init__(self, x = Point(), angleIn = 0.0):
        self.angle = angleIn
        dx = BIG_ROCK_SPEED * math.cos(math.radians(self.angle))
        dy = BIG_ROCK_SPEED * math.sin(math.radians(self.angle))
        super().__init__(x, Velocity(dx, dy), BIG_ROCK_RADIUS)
        
    def draw(self):
        img = "images/meteorGrey_big1.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent
        x = self.center.x
        y = self.center.y
        angle = self.angle

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        
    def rotate(self):
        self.angle += BIG_ROCK_SPIN


class Medium(Asteroid):
    
    def __init__(self, x = Point(), v = Velocity(), angleIn = 0.0):
        self.angle = angleIn
        dx = v.dx + BIG_ROCK_SPEED * math.cos(math.radians(self.angle))
        dy = v.dy + BIG_ROCK_SPEED * math.sin(math.radians(self.angle))
        super().__init__(x, Velocity(dx, dy), MEDIUM_ROCK_RADIUS)
        
    def draw(self):
        img = "images/meteorGrey_med1.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent
        x = self.center.x
        y = self.center.y
        angle = self.angle

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        
    def rotate(self):
        self.angle += MEDIUM_ROCK_SPIN


class Small(Asteroid):
    
    def __init__(self, x = Point(), v = Velocity(), angleIn = 0.0):
        print("Small asteroid created")
        self.angle = angleIn
        dx = v.dx + BIG_ROCK_SPEED * math.cos(math.radians(self.angle))
        dy = v.dy + BIG_ROCK_SPEED * math.sin(math.radians(self.angle))
        super().__init__(x, Velocity(dx, dy), SMALL_ROCK_RADIUS)
        
    def draw(self):
        img = "images/meteorGrey_small1.png"
        texture = arcade.load_texture(img)
        width = texture.width
        height = texture.height
        alpha = 1 # For transparency, 1 means not transparent
        x = self.center.x
        y = self.center.y
        angle = self.angle

        arcade.draw_texture_rectangle(x, y, width, height, texture, angle, alpha)
        
    def rotate(self):
        self.angle += SMALL_ROCK_SPIN


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        self.ship = Ship()
        self.asteroids = []
        self.bullets = []
        
        
        # Populate asteroids
        for x in range(0,5):
            # Find an appropriate starting place not in the center
            rand_angle = random.randint(0,360)
            rand_x = random.choice([random.randint(0, SCREEN_WIDTH / 2 - 50), random.randint(SCREEN_WIDTH / 2 + 50, SCREEN_WIDTH)])
            rand_y = random.choice([random.randint(0, SCREEN_HEIGHT / 2 - 50), random.randint(SCREEN_HEIGHT / 2 + 50, SCREEN_HEIGHT)])
            aNew = Big(Point(rand_x, rand_y), rand_angle)
            self.asteroids.append(aNew)
        

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        if self.ship.alive == True:
            self.ship.draw()
        
        for asteroid in self.asteroids:
            asteroid.draw()
            
        for bullet in self.bullets:
            bullet.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_collisions()

        # TODO: Tell everything to advance or move forward one step in time
        if self.ship.alive == True:
            self.ship.advance()
        
        for asteroid in self.asteroids:
            asteroid.advance()
            asteroid.rotate()
            
        for bullet in self.bullets:
            bullet.advance()


    def check_collisions(self):
        
        # Check if a bullet hit an asteroid
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                 # Make sure they are both alive before checking for a collision
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                                abs(bullet.center.y - asteroid.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        if isinstance(asteroid, Big):
                            small = Small(asteroid.center, Velocity(asteroid.velocity.dx + 5, asteroid.velocity.dy))
                            med1 = Medium(asteroid.center, Velocity(asteroid.velocity.dx, asteroid.velocity.dy + 2))
                            med2 = Medium(asteroid.center, Velocity(asteroid.velocity.dx, asteroid.velocity.dy - 2))
                            self.asteroids.append(small)
                            self.asteroids.append(med1)
                            self.asteroids.append(med2)
                            asteroid.alive = False
                        elif isinstance(asteroid, Medium):
                            print("Hit medium asteroid")
                            small1 = Small(asteroid.center, Velocity(asteroid.velocity.dx + 1.5, asteroid.velocity.dy + 1.5))
                            small2 = Small(asteroid.center, Velocity(asteroid.velocity.dx - 1.5, asteroid.velocity.dy - 1.5))
                            self.asteroids.append(small1)
                            self.asteroids.append(small2)
                            asteroid.alive = False
                        elif isinstance(asteroid, Small):
                            asteroid.alive = False
                        else:
                            print("There is a problem with check collisions")
                            
        # Check if asteroid hit ship
        for asteroid in self.asteroids:
            if self.ship.alive and asteroid.alive:
                too_close = self.ship.radius + self.ship.radius
                if (abs(self.ship.center.x - asteroid.center.x) < too_close and
                                    abs(self.ship.center.y - asteroid.center.y) < too_close):
                    self.ship.alive = False
        
        self.cleanup_zombies()
        

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.rotateLeft()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.rotateRight()

        if arcade.key.UP in self.held_keys:
            self.ship.thrust()

        if arcade.key.DOWN in self.held_keys:
            pass

        # Machine gun mode
        #if arcade.key.SPACE in self.held_keys:
            #pass
        
        
    def cleanup_zombies(self):
        """
        Removes any dead bullets or asteroids from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                bullet = Bullet(self.ship.center, self.ship.velocity)
                bullet.fire(self.ship.angle)
            
                self.bullets.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()