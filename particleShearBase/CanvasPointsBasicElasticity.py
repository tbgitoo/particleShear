from tkinter import *
import random
import math
from .Force_register import Force_register
from .Graphical_output_configuration import Graphical_output_configuration
from .CanvasPointsShear import CanvasPointsShear



class CanvasPointsBasicElasticity(CanvasPointsShear):
    """Canvas for placing `particleShear.CircleBasicElasticity` objects (referred to as spheres).
       This class maintains a list of objects of type
       `particleShear.CircleBasicElasticity` or derived and adds basic functions to handle this collection"""

    def __init__(self, size_x, size_y, theCanvas=False, doDrawing=False, k=1, nu=0.01,m=1):
        """Initialize self

                - **parameters**\n
                    `size_x` Width of area to be used in pixels = micrometers for the simulation\n
                    `size_y` Height of area to be used in pixels = micrometers for the simulation\n
                    `theCanvas` possibility to transmit a `tkinter` `Canvas` object for graphical output\n
                    `doDrawing` Flag to indicate whether graphical output should be produced or not\n
                    `k` Spring constant in (mg/s^2)/m of depth;
                    so F=-k*x*L with L the depth of the stack (the simulation is 2D) and x the compression\n
                    `nu` Viscosity force constant in (mg/s)/m of depth. This is to have F=nu*v*L, L again the depth\n
                    `m` is the mass per unit of depth in mg/m of depth"""

        self.k = k
        """Central spring constant in (mg/s^2)/m of depth"""
        self.nu = nu
        """Central viscosity constant in (mg/s)/m of depth"""

        self.central_repulsion_coefficient=0
        """Central repulsion coefficient to help avoid spheres being able to fully penetrate and cross each other.
         
        The central_repulsion_coeffiecient is chosen from 0 (only linear law) to 1 
        (highest proportion of central repulsion). 
        When central_repulsion_coefficient>0, there is a 1/x contribution to induce very strong repulsion when 
         the spheres approach total compression and thus to avoid crossing of the spheres. For small compressions, 
         even if central_repulsion_coefficient>0, the equations are chosen to give a dF/dx law with a slope of -k 
         when the spheres just touch. See `particleShear.CircleBasicElasticity.get_elastic_force` for details"""

        super(CanvasPointsBasicElasticity,self).__init__(size_x=size_x,size_y=size_y,theCanvas=theCanvas,doDrawing=doDrawing,m=m)




    def particle_info(self):
        return "CanvasPointsBasicElasticity: Basic elastic and neighbor behaviour"



    def elastic_force(self):
        """Let all spheres calculate the central elastic force acting on them; this will check for contact and so is more time
        consuming than `particleShear.CanvasPointsBasicElasticity.elastic_force_from_neighbors`

        This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""
        for sphereIndex in range(len(self.sphereList)):
            for sphereIndex2 in range(len(self.sphereList)):
                if sphereIndex != sphereIndex2:
                    self.sphereList[sphereIndex].elastic_force(self.sphereList[sphereIndex2], self.k)


    def elastic_force_from_neighbors(self):
        """Let all spheres calculate the central elastic force acting on from their known neighbors.

           This is quicker than `particleShear.CanvasPointsBasicElasticity.elastic_force`
           but necessitates the neighbor relations to be already established via
           `particleShear.CanvasPointsNeighbors.test_neighbor_relation`\n
           This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""


        for sphereIndex in range(len(self.sphereList)):
            self.sphereList[sphereIndex].elastic_force_from_neighbors(self.k)

    def central_viscous_force(self):
        """Let all spheres calculate the central viscous force acting on them.

        This will check for contact and so is more time
        consuming than `particleShear.CanvasPointsBasicElasticity.central_viscous_force_from_neighbors`.\n
        This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""
        for sphereIndex in range(len(self.sphereList)):
            for sphereIndex2 in range(len(self.sphereList)):
                if sphereIndex != sphereIndex2:
                    self.sphereList[sphereIndex].central_viscous_force(self.sphereList[sphereIndex2],
                                                                       self.nu)

    def central_viscous_force_from_neighbors(self):
        """Let all spheres calculate the central viscous force acting on from their known neighbors.

            This is quicker than `particleShear.CanvasPointsBasicElasticity.central_viscous_force`
            but necessitates the neighbor relations to be already established via
            `particleShear.CanvasPointsNeighbors.test_neighbor_relation`\n
            This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""
        for sphereIndex in range(len(self.sphereList)):
            self.sphereList[sphereIndex].central_viscous_force_from_neighbors(self.nu)


    def mechanical_simulation_step(self, cool_factor=0.97, dt=1):
        """ Perform full mechanical simulation step.

            This corresponds to the events associated with time advancing by dt.
            For this class, this includes resetting all forces to zero, calculation and summation of
            central and tangential forces on all particles, and calculation of the resulting
            acceleration, rotational acceleration, linear and rotational movement, including Lees-Edwards boundary
            conditions and adaption to change of shear rate
            The step can also include cooling (translational and rotational) by cool_factor.
            Forces are registered in the `particleShear.CanvasPointsMass.force_register`\n
            This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""

        self.mechanical_simulation_step_calculate_forces()
        self.record_total_particle_forces()
        self.mechanical_simulation_step_calculate_acceleration(cool_factor=cool_factor,dt=dt)
        self.mechanical_simulation_step_calculate_movement(dt=dt)



    def mechanical_simulation_step_calculate_forces(self):
        """ Calculate the forces acting on the spheres

        This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""
        self.reset_force_register()
        self.test_neighbor_relation()
        self.elastic_force_from_neighbors()
        self.central_viscous_force_from_neighbors()



    def mechanical_simulation_step_calculate_acceleration(self,cool_factor=0.97,dt=1):
        """Calculate the accelerations resulting from the forces

        This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""
        self.do_linear_acceleration(dt)
        self.cool(cool_factor)


    def mechanical_simulation_step_calculate_movement(self,dt=1):
        """ Calculate the displacement resulting from the sphere movement

        This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""
        self.move(dt)
        self.boundary_conditions()
        self.t = self.t + dt
        if self.applyingShear:
            self.shear = self.shear + self.shear_rate * dt



    def mechanical_relaxation(self,N=1000,cool_factor=0.97,dt=1,theTk=False,StressTensorEvaluator=False):
        """N times repeated `particleShear.CanvasPointsBasicElasticity.mechanical_simulation_step` with graphical
        update

        This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""
        for i in range(N):
            self.mechanical_simulation_step(cool_factor,dt)
            if self.doDrawing:
                theTk.update()
            if(StressTensorEvaluator):
                self.evaluate_stress_tensors(StressTensorEvaluator)

    def set_central_repulsion_coefficient(self,central_repulsion_coefficient=0):
        """Transmit the `particleShear.CanvasPointsBasicElasticity.central_repulsion_coefficient` to the spheres.

        This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""
        self.central_repulsion_coefficient=central_repulsion_coefficient
        for theSphere in self.sphereList:
            theSphere.central_repulsion_coefficient=central_repulsion_coefficient
