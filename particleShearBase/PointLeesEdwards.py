from tkinter import *
import random
import math
from .Point import Point


# Basic moving point
class PointLeesEdwards(Point):
    """Define a moving point, under Lees-Edwards boundary conditions.

    Lees-Edwards boundary conditions are period boundary conditions where particles exiting on one face of the
     rectangular simulation area reappear on the opposing face; in addition, during such jumps, the x-position is adjusted to reflect
     applied shear (e.g. delta_x = delta_y * shear) and x-speed is adjusted to reflect applied shear rate (e.g.
     delta_v_x = delta_y * shear_rate). This is well illustrated on a number of websites or publications
     (for instance, Bertevas, Erwan & Fan, Xijun & I. Tanner, Roger. (2009).
     Simulation of the rheological properties of suspensions of oblate
     spheroidal particles in a Newtonian fluid. Rheologica Acta. 49. 53-73. 10.1007/s00397-009-0390-8. )\n\n
     Oriented-object implementation of the Lees-Edwards boundary conditions requires that the object is aware of
     the pertinent global parameters of the simulation in addition to its own local properties:
     size of the simulation rectangle, current shear rate, current shear."""
    def __init__(self, x, y,size_x=500,size_y=500,shear=0,shear_rate=0,use_lees_edwards=True):
        """Initialize self

        - **parameters**\n
        `x` The x-position of the point (assumed micrometers for the simulation)\n
        `y` The y-position of the point (assumed micrometers for the simulation)\n
        `size_x` Width of area to be used in pixels = micrometers for the simulation\n
        `size_y` Height of area to be used in pixels = micrometers for the simulation\n
        `shear` shear (affecting the x-coordinate; expressed relative, so dimension-less)\n
        `shear_rate` shear rate (affecting the x-movement; expressed relative, so units 1/s)"""
        super(PointLeesEdwards,self).__init__(x,y)

        self.use_lees_edwards=use_lees_edwards
        """Flag to indicate whether or not we use Lees-Edwards boundary conditions"""
        self.size_x=size_x
        """Width of area to be used in pixels = micrometers for the simulation"""
        self.size_y=size_y
        """Height of area to be used in pixels = micrometers for the simulation"""


        self.shear=shear
        """Current applied shear (relative, so dimension-less)"""
        self.shear_rate=shear_rate
        """Current shear rate (relative, so 1/s)"""









    def boundary_conditions(self, boundary_x, boundary_y):
        """Ensure location of the point within boundary conditions

               x should be >= 0 and < boundary_x\n
               y should be >= 0 and < boundary_y\n
               x will be adusted to satisfy this via addition or subtraction of multiples of boundary_x\n
               y will be adusted to satisfy this via addition or subtraction of multiples of boundary_y\n
               In addition to the parent method defined in `particleShear.Point`, here the corrections associated with
               the Lees-Edwards boundary conditions are taken into account by using
               `particleShear.PointLeesEdwards.lee_edwards_boundary_conditions` if
               `particleShear.PointLeesEdwards.use_lees_edwards` is set to True\n
                This method is defined in class `particleShear.PointLeesEdwards`"""
        self.size_x=boundary_x
        self.size_y=boundary_y



        if not self.use_lees_edwards:
            super(PointLeesEdwards,self).boundary_conditions(boundary_x,boundary_y)
        else:
            self.lee_edwards_boundary_conditions()




    def lee_edwards_closest_to_zero(self,x,y):
        """Return the closest match to zero (for x and y separately) under periodic transformations respecting the
        Lees-Edwards boudary conditions

        This method is defined in class `particleShear.PointLeesEdwards`
        """

        while y >= (self.size_y/2):
            y = y - self.size_y
            x = x - self.size_y * self.shear
        while y < (-self.size_y/2):
            y = y + self.size_y
            x = x + self.size_y * self.shear
        while x >= (self.size_x/2):
            x = x - self.size_x
        while x < (-self.size_x/2):
           x = x + self.size_x

        return [x, y]

    def lee_edwards_positive(self,x,y):
        """Return the smallest positive solution (for x and y separately) under periodic transformations respecting the
        Lees-Edwards boudary conditions

        This method is defined in class `particleShear.PointLeesEdwards`
        """
        while y >= self.size_y:
            y = y - self.size_y
            x = x - self.size_y * self.shear
        while y < 0:
            y = y + self.size_y
            x = x + self.size_y * self.shear
        while x >= self.size_x:
            x = x - self.size_x
        while x < 0:
           x = x + self.size_x

        return [x, y]


    def lee_edwards_relative_speed(self,theSphere):
        """Return relative speed using neighbor convention under Lees-Edwards boundary conditions

        For this, the relative speed for the nearest representation under repetition and shear is calculated. Adjustement
        in the x-speed is made only for transformation by multiples of the simulation area height\n
        This method is defined in class `particleShear.PointLeesEdwards`
        """

        vx_rel = theSphere.xspeed - self.xspeed
        vy_rel = theSphere.yspeed - self.yspeed

        y = theSphere.y - self.y
        while y >= (self.size_y / 2):
            y = y - self.size_y
            vx_rel = vx_rel - self.size_y * self.shear_rate
        while y < (-self.size_y / 2):
            y = y + self.size_y
            vx_rel = vx_rel + self.size_y * self.shear_rate


        return [vx_rel, vy_rel]

    def relative_speed(self,theSphere):
        """Relative speed of the two spheres evaluated by the difference of speed of their centers.

        If `particleShear.PointLeesEdwards.use_lees_edwards` is set to True, this
        method uses `particleShear.PointLeesEdwards.lee_edwards_relative_speed`; otherwise,
        it uses `particleShear.Point.relative_speed` defined in the parent class `particleShear.Point`\n
        This method is defined in class `particleShear.PointLeesEdwards`
        """
        if self.use_lees_edwards:
            return self.lee_edwards_relative_speed(theSphere)
        else:
            return super(PointLeesEdwards,self).relative_speed(theSphere)






    def lee_edwards_boundary_conditions(self):
        """Ensure location of the point within boundary conditions

        x should be >= 0 and < boundary_x\n
        y should be >= 0 and < boundary_y\n
        x will be adusted to satisfy this via addition or subtraction of multiples of boundary_x\n
        y will be adusted to satisfy this via addition or subtraction of multiples of boundary_y\n
        In addition, adjusting y is coupled with a change in x and speed in x-direction
        to reflect shear, respectively shear rate, according to the Lees-Edwards boundary conditions.\n
        This method is defined in class `particleShear.PointLeesEdwards`."""


        old_x = self.x
        old_y = self.y

        new_pos = self.lee_edwards_positive(self.x,self.y)

        # Adjust speed

        self.xspeed = self.xspeed + (new_pos[1]-self.y)*self.shear_rate

        self.x = new_pos[0]
        self.y = new_pos[1]

        if self.doDrawing:
            self.theCanvas.move(self.shape, self.x - old_x, self.y - old_y)

    def lee_edwards_relative_vector(self,theSphere):
        """Return a relative vector to the Sphere, using smallest x- and y- distances resulting under Lees-Edwards
        periodic boundary condition transforms.

        This is achieved by applying
        `particleShear.PointLeesEdwards.lee_edwards_closest_to_zero` to the actual delta x and delta y vector.\n
        This method is defined in class `particleShear.PointLeesEdwards`.
         """
        pos = theSphere.coordinates()
        x = pos[0]
        y = pos[1]
        delta_x = x - self.x
        delta_y = y - self.y
        return self.lee_edwards_closest_to_zero(delta_x, delta_y)


    def d(self,theSphere):
        """Return the distance to another sphere under Lees-Edwards boundary conditions.

        This is the shortest distance
        among periodic repetitions, as evaluated as the absolute length of the delta vector returned by
        `particleShear.PointLeesEdwards.lee_edwards_relative_vector`.
        If `particleShear.PointLeesEdwards.use_lees_edwards` is False, the parent method
        `particleShear.Point.d` of class `particleShear.Point` is used instead.\n
        This method is defined in class `particleShear.PointLeesEdwards`."""
        if not self.use_lees_edwards:
            return super(PointLeesEdwards,self).d(theSphere)

        newDelta = self.lee_edwards_relative_vector(theSphere)
        return math.sqrt(newDelta[0] * newDelta[0] + newDelta[1] * newDelta[1])
    # To get a normal unit vector to another sphere

    def n(self, theSphere):
        """Return normal unit vector pointing towards another sphere, using Lees-Edward boundary conditions for
        determining the shortest connection among the periodic representations.


        Uses `particleShear.PointLeesEdwards.lee_edwards_relative_vector` to determine the shortest distance among the
        peridic representations under the Lees-Edwards boundary conditions.
        If `particleShear.PointLeesEdwards.use_lees_edwards` is False, the parent method
        `particleShear.Point.n` of class `particleShear.Point` is used instead.\n
        This method is defined in class `particleShear.PointLeesEdwards`.
        """


        if not self.use_lees_edwards:
            return super(PointLeesEdwards,self).n(theSphere)

        d = self.d(theSphere)
        if d > 0:
            rel=self.lee_edwards_relative_vector(theSphere)
            return ([rel[0] / d, rel[1] / d])
        if d == 0:
            angle = random.random()* 2 * math.pi
            return [math.cos(angle), math.sin(angle)]


    def transmit_lees_edwards_parameters(self,theSphere):
        """Transmit the parameters pertaining to the Lees-Edwards boundary conditions to another sphere (that is,
        object deriving from `particleShear.PointLeesEdwards`).

        If `particleShear.PointLeesEdwards.use_lees_edwards` is set to True, transmit the instance variables regarding
        canvas size (`particleShear.PointLeesEdwards.size_x`,`particleShear.PointLeesEdwards.size_y`), and shear regime
        (`particleShear.PointLeesEdwards.shear`,`particleShear.PointLeesEdwards.shear_rate`,
        `particleShear.PointLeesEdwards.use_lees_edwards`) to the given target sphere.
        Else, only set the `particleShear.PointLeesEdwards.use_lees_edwards` field in the
        target sphere to False\n
        This method is defined in class `particleShear.PointLeesEdwards`"""
        if self.use_lees_edwards:
            theSphere.size_x = self.size_x
            theSphere.size_y = self.size_y
            theSphere.shear_rate = self.shear_rate
            theSphere.shear = self.shear
            theSphere.use_lees_edwards = self.use_lees_edwards
        else:
            if hasattr(theSphere,"use_lees_edwards"):
                theSphere.use_lees_edwards=False
        return theSphere


    def cool(self, f=0.8):
        """Cool by decreasing local speed

        Cool relative to fine-grained local movement (x-speed of the fluid is expected to be
        (y-size_y/2)*shear_rate), decrease the delta to this expected speed rather than
        diminishing the absolute speed. This is used to stabilize the ensemble at the given
        shear; physically, this reflects friction with the pore or interstitial fluid.\n
        This method is defined in class `particleShear.PointLeesEdwards`"""
        x_speed_local = (self.y-self.size_y/2)*self.shear_rate

        #self.xspeed = x_speed_local+(self.xspeed-x_speed_local) * f
        self.xspeed = x_speed_local + (self.xspeed - x_speed_local) * f
        self.yspeed = self.yspeed * f






