from tkinter import *
import random
import math

from .PointLeesEdwards import PointLeesEdwards
from .Graphical_output_configuration import Graphical_output_configuration


#
class Circle(PointLeesEdwards):
    """Provide a circle that can draw itself according to the graphical drawing convention

        Inherits from `particleShear.PointLeesEdwards`, so will respect Lees-Edwards boundary conditions
        provided `particleShear.PointLeesEdwards.use_lees_edwards` is set to True (default: False)"""

    def __init__(self, color, x, y, diameter, theCanvas=False, doDrawing=False,use_lees_edwards=False):
        """Initialize self

        - **parameters**\n
        `x` The x-position of the center of the circle (in pixels, assumed micrometers for the simulation)\n
        `y` The y-position of the center of the circle (in pixels, assumed micrometers for the simulation)\n
        `diameter` The diameter of the circle  (in pixels, assumed micrometers for the simulation)\n
        `theCanvas` Tkinter canvas; provide False if no Canvas is available or no drawing is desired\n
        `doDrawing` Explicit switch to turn of drawing\n
        `use_lees_edwards` Explicit Shoud Lees-Edwards boundary conditions be used?\n
        """
        super(Circle,self).__init__(x,y,use_lees_edwards=use_lees_edwards)

        self.theCanvas = theCanvas
        """tkinter canvas"""

        self.r = diameter / 2
        """Radius of the circle, in pixels (=micrometers for the simulations)"""
        self.doDrawing = doDrawing
        """Flag to indicate whether graphical output should be produced or not"""

        self.shape=False
        """Shape on the Tkinter canvas when actively drawing"""
        self.color=color
        """Color of the spheres"""
        self.graphical_output_configuration = Graphical_output_configuration()
        """`particleShear.Graphical_output_configuration` to set options how the spheres and their neighboring relations
                are displayed"""
        self.graphical_output_configuration.color_spheres_volume= color
        self.graphical_output_configuration.color_spheres_boundary = color


        self.set_graphical_output_configuration(self.graphical_output_configuration)

        self.initiate_drawing()




    def set_graphical_output_configuration(self, graphical_output_configuration):
        """Set new `particleShear.Graphical_output_configuration`

        This method is defined in class `particleShear.Circle`"""
        self.deleteDrawing()
        self.graphical_output_configuration=graphical_output_configuration
        self.color=self.graphical_output_configuration.color_spheres_volume
        self.initiate_drawing()

    def coordinates(self):
        """Return the current coordinates: vector of three elements, which are (x,y,radius)

        This method is defined in class `particleShear.Circle`"""
        return [self.x, self.y, self.r]


    def initiate_drawing(self):
        """Instiante the shapes representing this object on  `particleShear.Circle.theCanvas`.

        This method only has an effect if `particleShear.Circle.doDrawing` is True. If a shape is created, the reference to
        the circle on the canvas is stored in `particleShear.Circle.shape`"""
        self.deleteDrawing()

        self.shape = False

        if self.doDrawing:
            if self.graphical_output_configuration.draw_spheres_as=="spheres":
                self.shape = self.theCanvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r,
                                               fill=self.color)
            if self.graphical_output_configuration.draw_spheres_as=="dots":
                self.shape = self.theCanvas.create_oval(self.x - 2, self.y - 2, self.x + 2,
                                                        self.y + 2,
                                                        fill=self.color)


    def move(self, dt=1):
        """Move for time interval dt, including the graphical shape if present

        This method is defined in class `particleShear.Circle`"""
        super(Circle,self).move(dt)
        if self.doDrawing:
            self.moveDrawing(dt)




    def moveDrawing(self, dt):
        """Move for the drawing on the Tkinter canvas

        This method is defined in class `particleShear.Circle`"""
        self.theCanvas.move(self.shape, self.xspeed * dt, self.yspeed * dt)

    def deleteDrawing(self):
        """Delete drawing on the Tkinter canvas

        This method is defined in class `particleShear.Circle`"""
        if self.theCanvas:
            self.theCanvas.delete(self.shape)

    def tangential_speed(self, theSphere):
        """Tangential component of the relative speed of a given sphere relative to this object.

        The other sphere object needs to be of type `particleShear.Point` or derived. Returns a scalar,
        describing the relative speed component parallel to a tangential vector with counter-clockwise orientation.
        The speed is returned in pixels/s (= micrometers/s for the simulation). This method uses
        `particleShear.Circle.tangential_vector` internally.\n
         This method is defined in class `particleShear.Circle`"""
        v_rel = self.relative_speed(theSphere)
        vx_rel = v_rel[0]
        vy_rel = v_rel[1]

        t_vector = self.tangential_vector(theSphere)
        vt = vx_rel * t_vector[0] + vy_rel * t_vector[1]
        return vt


    def tangential_vector(self, theSphere):
        """Return tangential interface vector of given sphere relative to this object.

        Calculates the tangential vector describing the direction and orientation of interface located perpendicalurlay
        to the line relying the centers of the spheres. Counter-clock wise orientation (but: attention to the
        orientation of the computer graphics device, which often invert the y-axis!)\n
         This method is defined in class `particleShear.Circle`"""
        n_vector = self.n(theSphere)
        return [-n_vector[1], n_vector[0]]





