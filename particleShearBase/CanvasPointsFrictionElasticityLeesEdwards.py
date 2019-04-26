from tkinter import *
import random
import math
from .CanvasPointsBasicElasticityLeesEdwards import CanvasPointsBasicElasticityLeesEdwards
from .Force_register import Force_register

class CanvasPointsFrictionElasticityLeesEdwards(CanvasPointsBasicElasticityLeesEdwards):
    """Canvas for placing `particleShear.CircleFrictionElasticity` objects (referred to as spheres).
          This class maintains a list of objects of type
          `particleShear.CircleFrictionElasticity` or derived and adds functions for handling friction and associated
          non-central forces"""

    def __init__(self, size_x, size_y, theCanvas=FALSE, doDrawing=FALSE,
                 k=1, nu=0.01,m=1,k_t=1,nu_t=0.01,mu=0.1):
        """Initialize self

                        - **parameters**\n
                            `size_x` Width of area to be used in pixels = micrometers for the simulation\n
                            `size_y` Height of area to be used in pixels = micrometers for the simulation\n
                            `theCanvas` possibility to transmit a `tkinter` `Canvas` object for graphical output\n
                            `doDrawing` Flag to indicate whether graphical output should be produced or not\n
                            `k` Central spring constant in (mg/s^2)/m of depth;
                            so F=-k*x*L with L the depth of the stack (the simulation is 2D) and x the compression\n
                            `nu` Central viscosity force constant in (mg/s)/m of depth. This is to have F=nu*v*L, L again the depth\n
                            `m` is the mass per unit of depth in mg/m of depth\n
                            `k_t` Tangential spring constant in (mg/s^2)/m of depth;
                            relevant for locked or permanent interfaces but not for slipping interfaces\n
                            `nu_t` Central viscosity force constant in (mg/s)/m of depth.
                             Relevant for frictionally locked and permanent interfaces but not slipping ones\n
                            `mu` Friction coefficient, describes the maximum interface force for non-permanent interfaces by
                            F_tangential_max = F_central*mu"""



        super(CanvasPointsFrictionElasticityLeesEdwards, self).__init__( size_x, size_y, theCanvas, doDrawing,
                                                          k, nu, m)
        self.k_t=k_t
        """`k_t` Tangential spring constant in (mg/s^2)/m of depth;"""
        self.nu_t=nu_t
        """`nu_t` Central viscosity force constant in (mg/s)/m of depth."""
        self.mu=mu
        """`mu` Friction coefficient"""

    def particle_info(self):
        return "CanvaPointsFrictionElasticityLeesEdwards: Lees Edwards boundary conditions and stick-and-slip type friction"


    def tangential_force(self):
        """Let all spheres calculate the total tangental force acting on them.

         This will check for contact and so is more time
         consuming than `particleShear.CanvasPointsFrictionElasticityLeesEdwards.tangential_force_from_neighbors`.
         For this function to work, the spheres must be of type `particleShear.CircleFrictionElasticity`or a
         subclass thereof, or otherwise possess a method `tangential_force`\n
         This method is defined in class `particleShear.CanvasPointsFrictionElasticityLeesEdwards`"""

        for sphereIndex in range(len(self.sphereList)):
            for sphereIndex2 in range(len(self.sphereList)):
                if sphereIndex != sphereIndex2:
                    self.sphereList[sphereIndex].tangential_force(self.sphereList[sphereIndex2],
                                                                  self.nu_t, self.mu, self.k, self.k_t)

    def tangential_force_from_neighbors(self):
        """Let all spheres calculate the total tangential force acting on from their known neighbors.

        This is quicker than `particleShear.CanvasPointsFrictionElasticityLeesEdwards.tangential_force`
        but necessitates the neighbor relations to be already established via
        `particleShear.CanvasPointsNeighbors.test_neighbor_relation`.
        For this function to work, the spheres must be of type `particleShear.CircleFrictionElasticity`or a
        subclass thereof, or otherwise possess a method `tangential_force_from_neighbors`.\n
        This method is defined in class `particleShear.CanvasPointsFrictionElasticityLeesEdwards`"""
        for sphereIndex in range(len(self.sphereList)):
            self.sphereList[sphereIndex].tangential_force_from_neighbors(self.nu_t,self.mu,self.k,self.k_t)

    def do_rotational_acceleration(self, dt):
        """Have the spheres calculate their rotational acceleration from the tangential forces.

        For this function to work,
        the spheres must be of type `particleShear.CircleFrictionElasticity` or subclass thereof, or alternatively,
        possess a method `do_rotational_acceleration`\n
        This method is defined in class `particleShear.CanvasPointsFrictionElasticityLeesEdwards`"""
        for theSphere in self.sphereList:
            theSphere.do_rotational_acceleration(dt)


    def mechanical_simulation_step_calculate_forces(self,dt=1):
        super(CanvasPointsFrictionElasticityLeesEdwards,self).mechanical_simulation_step_calculate_forces()
        self.tangential_force_from_neighbors()

    def record_total_particle_forces(self):

        super(CanvasPointsFrictionElasticityLeesEdwards,self).record_total_particle_forces()

        for theSphere in self.sphereList:
            moment = theSphere.torque
            self.force_register.record_unbalanced_moment(theSphere,moment)

    def mechanical_simulation_step_calculate_movement(self,dt=1):

        self.move(dt)
        self.setShear(self.shear + self.shear_rate * dt)
        self.setShearRate(self.shear_rate)
        self.boundary_conditions()
        self.t = self.t + dt


    def mechanical_simulation_step_calculate_acceleration(self,cool_factor=0.97,dt=1):
        self.do_linear_acceleration(dt)
        self.do_rotational_acceleration(dt)
        self.cool(cool_factor)
























