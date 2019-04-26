from tkinter import *
import random
import math
from .Force_register import Force_register
from .Graphical_output_configuration import Graphical_output_configuration
from .CanvasPointsBasicElasticity import CanvasPointsBasicElasticity



class CanvasPointsBasicElasticityLeesEdwards(CanvasPointsBasicElasticity):
    """Canvas for placing `particleShear.CircleBasicElasticity` objects (referred to as spheres).
       This class maintains a list of objects of type
       `particleShear.CircleBasicElasticity` or derived and adds functions specific to Lees-Edwards
       boundary conditions"""

    def __init__(self, size_x, size_y, theCanvas=False, doDrawing=False, k=1, nu=0.01,m=1):

        super(CanvasPointsBasicElasticityLeesEdwards,self).__init__(size_x=size_x,size_y=size_y,
                                                                    theCanvas=theCanvas,doDrawing=doDrawing,k=k,nu=nu,m=m)



    def particle_info(self):
        return "CanvasPointsBasicElasticityLeesEdwards: Basic elastic properties and Lees-Edwards transmission of " \
               "force across boundary conditions"



    def setShear(self,theShear):
        """Set new shear value and transmit to the constituent spheres via
        `particleShear.CanvasPointsBasicElasticityLeesEdwards.setShearInSpheres`

        This method is defined in class `particleShear.CanvasPointsBasicElasticityLeesEdwards`"""
        self.shear=theShear
        self.setShearInSpheres()


    def setShearInSpheres(self):
        """Propage the shear value to the constituent spheres.

        This method is defined in class `particleShear.CanvasPointsBasicElasticityLeesEdwards`"""
        for theSphere in self.sphereList:
            theSphere.shear=self.shear



    def setShearRate(self, theShearRate):
        """set a new value for the shear rate and adjust movement of the constituent spheres
         correspondingly.

          This method is designed to respect the a priori deformation under the Lees-Edwards boundary conditions via
         `particleShear.CanvasPointsBasicElasticityLeesEdwards.adjust_sphere_speed_to_shear_rate_change`\n
         This method is defined in class `particleShear.CanvasPointsBasicElasticityLeesEdwards`"""

        delta_shear_rate=theShearRate-self.shear_rate

        self.adjust_sphere_speed_to_shear_rate_change(delta_shear_rate)

        self.shear_rate = theShearRate
        self.setShearRateInSpheres()

    def adjust_sphere_speed_to_shear_rate_change(self,delta_shear_rate):
        """ Adjust sphere speed via SLLOD stabilized equations of motion.

        The idea here is that when changing shear rate, we change the speed of the particles
        so that they conserve their relation compared to the local average speed.
        This avoids things like shock-wave propagation due to very large speed amplitude changes;
        similarly, the rotation rate is adjusted to reflect local average vorticity under shear\n
        This method is defined in class `particleShear.CanvasPointsBasicElasticityLeesEdwards`"""

        for theSphere in self.sphereList:
            theSphere.xspeed=theSphere.xspeed+(theSphere.y-self.size_y/2)*delta_shear_rate
            if hasattr(theSphere,"omega"):
                # http://www.mate.tue.nl/mate/pdfs/9614.pdf
                theSphere.omega=theSphere.omega-delta_shear_rate/2



    def setShearRateInSpheres(self):
        """Propagate shear rate to the spheres.

        To allow for SLLOD-type adjustment to the changed shear rate,
         `particleShear.CanvasPointsBasicElasticityLeesEdwards.setShearRate` is used.\n
         This method is defined in class `particleShear.CanvasPointsBasicElasticityLeesEdwards`"""
        for theSphere in self.sphereList:
            theSphere.shear_rate = self.shear_rate


    def record_individual_internal_force(self,target,source,force_vector):
        """Record individual force in the central `particleShear.CanvasPointsMass.force_register`.

         If a pair of spheres
        concerned is situated across a Lees-Edwards boundary (periodicity), the function counts this
        as external rather than internal force.\n
         This method is defined in class `particleShear.CanvasPointsBasicElasticityLeesEdwards`"""
        if not self.canMove(target):
            return
        if self.canMove(source):
            # Consider only physical pairs
            physical_distance = target.d_euclidian(source)

            simulation_distance = target.d(source)

            if physical_distance == simulation_distance:
                self.force_register.record_individual_internal_force(target,source,force_vector)
            else:

                self.force_register.record_external_force(target, force_vector)
        else:
            self.force_register.record_external_force(target,force_vector)


    def record_individual_internal_torque(self,target,source,moment):
        """Record individual torque in the central `particleShear.CanvasPointsMass.force_register`.

         If a pair of spheres
        concerned is situated across a Lees-Edwards boundary (periodicity), the function counts this
        as external rather than internal torque.\n
         This method is defined in class `particleShear.CanvasPointsBasicElasticityLeesEdwards`"""
        if not self.canMove(target):
            return
        if self.canMove(source):
            # Consider only physical pairs
            physical_distance = target.d_euclidian(source)

            simulation_distance = target.d(source)

            if physical_distance == simulation_distance:
                self.force_register.record_individual_internal_torque(target,source,moment)
            else:

                self.force_register.record_external_torque(target, moment)
        else:
            self.force_register.record_external_torque(target,moment)
















