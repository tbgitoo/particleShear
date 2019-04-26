from tkinter import *
import random
import math

from .Force_register import Force_register

from .Graphical_output_configuration import Graphical_output_configuration

from .Circle import Circle


class CircleMass(Circle):
    """Provide a circle with an attribued mass

    Describes a sphere (circle in 2D) that possess a mass and stores the forces acting on the sphere. \n
    In a simulation, the concept is that before each
     simulation step, the force known to each sphere itself (the ìnstance variables `particleShear.CircleMass.xforce` and
    `particleShear.CircleMass.yforce`) are reset to 0; as the spheres are meant to be associated with a simulation
     area object derived from `particleShear.CanvasPointsMass`, this typically happens through a call to the method
     `particleShear.CanvasPointsMass.reset_force` of `particleShear.CanvasPointsMass` or relevant subclass.
     In addition, for the purpose of stress tensor evaluation, details about
     the forces are registered during the various calculations in a simulation step in the
     `particleShear.CircleMass.force_register`, which is provided through the canvas class (derived from
     `particleShear.CanvasPointsMass`). At the beginning of each simulation step, the force register common to all the
     spheres on a simulaton canvas also needs to be reset, this is done via the
     `particleShear.CanvasPointsMass.reset_force_register` of `particleShear.CanvasPointsMass` or relevant subclass.\n
     When running the simulation, forces are calculated in various ways, and attributed to the sphere particles by direct
     change of the instance variables `particleShear.CircleMass.xforce` and
    `particleShear.CircleMass.yforce`. Depending on their nature, they are also registered in various ways in the common
     `particleShear.Force_register` object,
     which is the instance variable `particleShear.CanvasPointsMass.force_register` of the relevant subclass of
     `particleShear.CanvasPointsMass`; for practical purposes, this very same `particleShear.Force_register` is also known
     to each sphere as its own instance variable `particleShear.CircleMass.force_register`.\n
    Once all the forces known after a complete simulation step, the net force can be
    converted to acceleration (by explicit call to `particleShear.CircleMass.do_linear_acceleration`). This then
    calculates the change in speed due to the acceleration, and resets the force for the particle at hand to zero.
    At this point, the `particleShear.CircleMass.force_register`, common to all the spheres,
    still contains the detailed information about the forces and can
    be exploited for stress tensor evaluation by a `particleShear.StressTensorEvaluation` object. The
    `particleShear.CircleMass.force_register` needs to be reset separately prior to the next simulation step, see above.\n
    Inherits from `particleShear.PointLeesEdwards`, so will respect Lees-Edwards boundary conditions
    provided `particleShear.PointLeesEdwards.use_lees_edwards` is set to True (default: False)"""

    def __init__(self, color, x, y, diameter, m=1, theCanvas=False, doDrawing=False,force_register=Force_register(),
                 use_lees_edwards=False):
        """Initialize self

        - **parameters**\n
        `x` The x-position of the center of the circle (in pixels, assumed micrometers for the simulation)\n
        `y` The y-position of the center of the circle (in pixels, assumed micrometers for the simulation)\n
        `diameter` The diameter of the circle  (in pixels, assumed micrometers for the simulation)\n
        `m` is the mass per unit of depth in mg/m of depth\n
        `theCanvas` Tkinter canvas; provide False if no Canvas is available or no drawing is desired\n
        `doDrawing` Explicit switch to turn of drawing\n
        `force_register`Possibility to provide a reference to a common `particleShear.Force_register` variable to register the
        forces calculated during simulation\n
        `use_lees_edwards` Explicit Shoud Lees-Edwards boundary conditions be used?\n
        """


        super(CircleMass,self).__init__(color,x,y,diameter, theCanvas=theCanvas, doDrawing=doDrawing,
                                        use_lees_edwards=use_lees_edwards)

        self.m = m
        """Mass of the particle, in mg/m of depth (2D simulaton)"""


        self.force_register = force_register
        """Reference to the common `particleShear.CanvasPointsMass.force_register` to store the forces acting on the spheres"""

        self.xforce = 0
        """x-component of the net force on this sphere, in N per m of depth in the 2D simulation"""
        self.yforce = 0
        """y-component of the net force on this sphere, in N per m of depth in the 2D simulation"""


    def record_total_particle_force(self):
        """ Record the current total force on this particle

        This functions transmits the current net force having served to do the
        calculation to the `particleShear.CircleMass.force_register`

        This method is defined in class `particleShear.CircleMass`"""

        self.force_register.record_total_particle_force(self, [self.xforce, self.yforce])

    def do_linear_acceleration(self, dt):
        """ Apply the linear acceleration from the net force

        This method calculates the linear acceleration from F=m*a and applies it by dv=a*dt. It also transmits
        the current total force to the force register (via `particleShear.CircleMass.record_total_particle_force`) before
        resetting the net force to 0\n
        This method is defined in class `particleShear.CircleMass`"""
        self.record_total_particle_force()

        self.xspeed = self.xspeed + self.xforce * dt / self.m
        self.yspeed = self.yspeed + self.yforce * dt / self.m
        self.xforce = 0
        self.yforce = 0

    def applyInternalForceAndRegister(self,force_vector,source,register_homolog=False):
        """ Apply an internal force and update the `particleShear.CircleMass.force_register`

        This method adds a given force_vector to the net force acting on this particle.
        It also registers the force in the `particleShear.CircleMass.force_register` as an internal force
        (between two mobile spheres). If the `register_homolog` parameter is provided as True,
        then the opposing equal force is also registered  in the `particleShear.CircleMass.force_register`. Even in that
        case, the opposing equal reaction force has to be explicity applied on the `source` sphere elsewhere, this
        function never applies a force directly to the `source` sphere.\n
        This method is defined in class `particleShear.CircleMass`"""

        self.xforce = self.xforce + force_vector[0]
        self.yforce = self.yforce + force_vector[1]

        self.force_register.record_individual_internal_force(self, source,force_vector)
        if register_homolog:
            opposing_force = [-force_vector[0], -force_vector[1]]
            source.force_register.record_individual_internal_force(source, self, opposing_force)






