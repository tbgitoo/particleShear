from tkinter import *
import random
import math
from .Force_register import Force_register
from .CanvasPoints import CanvasPoints

class CanvasPointsMass(CanvasPoints):
    """Canvas for placing objects of type `particleShear.CircleMass` (or derived).

           This class maintains a list of objects of type
           `particleShear.CircleMass` or derived and adds functions to handle this collection.
           See `particleShear.CanvasPoints.sphereList` of the base class `particleShear.CanvasPoints`."""

    def __init__(self, size_x, size_y, theCanvas=FALSE, doDrawing=FALSE, m=1):
        """Initialize self

        - **parameters**\n
        `size_x` Width of area to be used in pixels = micrometers for the simulation\n
        `size_y` Height of area to be used in pixels = micrometers for the simulation\n
        `theCanvas` possibility to transmit a `tkinter` `Canvas` object for graphical output\n
        `doDrawing` Flag to indicate whether graphical output should be produced or not\n
        `m` is the mass per unit of depth in mg/m of depth"""
        super(CanvasPointsMass,self).__init__( size_x, size_y, theCanvas=theCanvas, doDrawing=doDrawing)

        self.t=0
        """Keep track of time elapsed during application of shear protocols"""


        self.force_register = Force_register()
        """The `particleShear.Force_register` to store the forces acting on the particles"""

        self.m=m
        """The mass (identical) for each of the spheres"""





    def reset_force_register(self):
        """Empty the `particleShear.CanvasPointsMass.force_register`

        This method is defined in class `particleShear.CanvasPointsMass`"""
        self.force_register.reset_force_register()

    def record_individual_internal_force(self,target,source,force_vector):
        """Record a force in the `particleShear.CanvasPointsMass.force_register`.

        Only forces resulting in actual motion (i.e. acting on mobile
        spheres, see `particleShear.CanvasPoints.canMove`) are accounted for. Also, the function detects
        external forces acting from immobilized boundary spheres and re-reroutes the call to
        `particleShear.CanvasPointsMass.record_external_force`.\n
        This method is defined in class `particleShear.CanvasPointsMass`"""
        if not self.canMove(target): # Sphere moved by boundary conditions with unknown force
            return
        if self.canMove(source):  # running internal spheres moving freely
            self.force_register.record_individual_internal_force(target, source, force_vector)
        else:
            self.record_external_force(target, force_vector)

    def record_individual_internal_torque(self, target, source, moment):
        """Record a torque in the `particleShear.CanvasPointsMass.force_register`.

        Only torques resulting in actual motion (i.e. acting on mobile
        spheres, see `particleShear.CanvasPoints.canMove`) are accounted for. Also, the function detects
        external torques acting from immobilized boundary spheres and re-reroutes the call to
        `particleShear.CanvasPointsMass.record_external_torque`.\n
        This method is defined in class `particleShear.CanvasPointsMass`"""

        if not self.canMove(target):  # Sphere moved by boundary conditions with unknown force
            return
        if self.canMove(source):  # running internal spheres moving freely
            self.force_register.record_individual_internal_torque(target, source, moment)
        else:
            self.record_external_torque(target, moment)


    def record_total_particle_forces(self):
        for theSphere in self.sphereList:
            force_vector = [theSphere.xforce, theSphere.yforce]
            self.record_total_particle_force(theSphere,force_vector)



    def record_total_particle_force(self,target,force_vector):
        """Record a total resultant particle force in the `particleShear.CanvasPointsMass.force_register`.

           Only forces resulting in actual motion (i.e. acting on mobile
           spheres, see `particleShear.CanvasPoints.canMove`) are accounted for.\n
           This method is defined in class `particleShear.CanvasPointsMass`"""
        if not self.canMove(target):
            return
        self.force_register.record_total_particle_force(target,force_vector)

    def record_external_force(self, target, force_vector):
        """Record an external force actin on a mobile sphere in the `particleShear.CanvasPointsMass.force_register`.

            Only forces resulting in actual motion (i.e. acting on mobile
            spheres, see `particleShear.CanvasPoints.canMove`) are accounted for.\n
            This method is defined in class `particleShear.CanvasPointsMass`"""
        if not self.canMove(target):
            return
        self.force_register.record_external_force(target, force_vector)

    def record_external_torque(self, target, moment):
        """Record an external torque acting on a mobile sphere in the `particleShear.CanvasPointsMass.torque_register`.

        Only torques resulting in actual motion (i.e. acting on mobile
        spheres, see `particleShear.CanvasPoints.canMove`) are accounted for.\n
        This method is defined in class `particleShear.CanvasPointsMass`"""

        if not self.canMove(target):
            return
        self.force_register.record_external_torque(target, moment)

    def record_unbalanced_moment(self,target,moment):
        """Record unbalanced (net) angular moment acting on a mobile sphere in the `particleShear.CanvasPointsMass.force_register`.

            Only forces resulting in actual motion (i.e. acting on mobile
            spheres, see `particleShear.CanvasPoints.canMove`) are accounted for.\n
            This method is defined in class `particleShear.CanvasPointsMass`"""
        if not self.canMove(target):
            return

        self.force_register.record_unbalanced_moment(target, moment)



    def particle_info(self):
        return "CanvasPointsMass: Graphical interface with force registry and acceleration"



    def evaluate_stress_tensors(self,StressTensorEvaluator):
        """Evaluate the stress tensors from the `particleShear.CanvasPointsMass.force_register`

        - **parameters**\n
        The StressTensorEvaluator is expected be of type `particleShear.StressTensorEvaluation` or derived.\n
        This method is defined in class `particleShear.CanvasPointsMass`"""

        StressTensorEvaluator.evaluate_stress_tensors(self.force_register, self.movableSphereList(), self.shear_rate)



    def reset_force(self):
        """Reset all actual forces on the spheres. Does not reset the `particleShear.CanvasPointsMass.force_register`.

        This method is defined in class `particleShear.CanvasPointsMass`"""
        for theSphere in self.sphereList:
            theSphere.xforce = 0
            theSphere.yforce = 0


