from tkinter import *
import random
import math


# Basic moving point
class Point:
    """Define a moving point, with position (x and y) and speed (xpeed and yspeed)"""
    def __init__(self, x, y):
        """Initialize self

        - **parameters**\n
        `x` The x-position of the point (assumed micrometers for the simulation)\n
        `y` The y-position of the point (assumed micrometers for the simulation)\n
        """

        self.x = x
        """The x-position of the point (assumed micrometers for the simulation)"""
        self.y = y
        """The y-position of the point (assumed micrometers for the simulation)"""
        self.xspeed=0
        """The horizontal speed of the point (assumed micrometers/s for the simulation)"""
        self.yspeed=0
        """The vertical speed of the point (assumed micrometers/s for the simulation)"""


    def coordinates(self):
        """Return the current coordinates: vector of three elements, which are (x,y,radius=0)

        This method is defined in class `particleShearBase.Point`"""
        return [self.x, self.y, 0]

    def boundary_conditions(self, boundary_x, boundary_y):
        """Ensure location of the point within boundary conditions

        x should be >= 0 and < boundary_x\n
        y should be >= 0 and < boundary_y\n
        x will be adusted to satisfy this via addition or subtraction of multiples of boundary_x\n
        y will be adusted to satisfy this via addition or subtraction of multiples of boundary_y\n
        This method is defined in class `particleShearBase.Point`"""
        old_x = self.x
        old_y = self.y
        while self.x >= boundary_x:
            self.x = self.x - boundary_x
        while self.x < 0:
            self.x = self.x + boundary_x
        while self.y >= boundary_y:
            self.y = self.y - boundary_y
        while self.y < 0:
            self.y = self.y + boundary_y
        if self.doDrawing:
            self.theCanvas.move(self.shape, self.x - old_x, self.y - old_y)



    def d_euclidian(self,theSphere):
        """Calculate euclidian distance to another object of type `particleShearBase.Point`or derived

        The calculation is done via the Pythagorean formula: square root of the sum of the squares of the distances
        in x and y.\n
        This method is defined in class `particleShearBase.Point`"""
        pos = theSphere.coordinates()
        x = pos[0]
        y = pos[1]
        return math.sqrt((x - self.x) * (x - self.x) + (y - self.y) * (y - self.y))


    def d(self,theSphere):
        """Calculate the distance to another sphere.

        For this class, uses `particleShearBase.Point.d_euclidian` but is overriden by specific subclasses.\n
        This method is defined in class `particleShearBase.Point`"""
        return self.d_euclidian(theSphere)




    def n(self, theSphere):
        """Return unit vector pointing towards another sphere

        For this `particleShearBase.Point`, returns vector in cartesian coordinates pointing towards the center of the sphere
        indicated by the parameter theSphere. This behaviour can be overriden directly or indirectly by overriding
        the definition of `particleShearBase.Point.d`\n
        This method is defined in class `particleShearBase.Point`"""
        d = self.d(theSphere)
        if d > 0:
            pos = theSphere.coordinates()
            x = pos[0]
            y = pos[1]
            return ([(x - self.x) / d, (y - self.y) / d])
        if d == 0:
            angle = random.random()* 2 * math.pi
            return [math.cos(angle), math.sin(angle)]

    def relative_position(self,theSphere):
        """Return vector indicating the position of theSphere relative to myself

        For this `particleShearBase.Point`, returns vectorial difference between the position of theSphere and the current object,
        but this behaviour can be overriden directly, or also indirectly  when either the definition of
        `particleShearBase.Point.d` or `particleShearBase.Point.n` is overriden.\n
        This method is defined in class `particleShearBase.Point`"""
        n_vector = self.n(theSphere)
        d = self.d(theSphere)
        return [n_vector[0]*d,n_vector[1]*d]

    


    def move(self, dt=1):
        """Move for time interval dt

        This method is defined in class `particleShearBase.Point`"""
        self.x = self.x + self.xspeed * dt
        self.y = self.y + self.yspeed * dt




    def cool(self, f=0.8):
        """Cool by decreasing speed

        This method is defined in class `particleShearBase.Point`"""
        self.xspeed = self.xspeed * f
        self.yspeed = self.yspeed * f

    def relative_speed(self, theSphere):
        """Relative speed of the two spheres evaluated by the difference of speed of their centers

                This method is defined in class `particleShearBase.Point`"""
        return [theSphere.xspeed-self.xspeed, theSphere.yspeed-self.yspeed]
