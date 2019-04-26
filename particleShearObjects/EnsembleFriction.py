from tkinter import *
import random
import math
from .Ensemble import Ensemble
from particleShearBase import Force_register

class EnsembleFriction(Ensemble):
    """Ensemble of particles of type  `particleShear.SphereFriction`, with regular boundary conditions

            This class creates and maintains a list of objects of type
            `particleShear.SphereFriction`. These objects are generically
            referred to as spheres and are stored in `particleShear.CanvasPoints.sphereList`.\n
            The ensemble class does not implement proper Lees-Edwards boundaries, but emulates neighboring spheres by
            creating replicates of the spheres near the boundares displaced by one positive or negative multiple of the
            xy dimensions of the simulation area.\n
            Class defined in subpackage particleShearObjects"""

    def __init__(self, size_x, size_y, N, packing_fraction=0.8, theCanvas=FALSE, doDrawing=FALSE, k=1, nu=0.01,m=1,
                 bimodal_factor=1.4,
                 k_t=1,nu_t=0.01,mu=0.1):

        """Initialize self

                - **parameters**\n
                `size_x` Width of area to be used in pixels = micrometers for the simulation\n
                `size_y` Height of area to be used in pixels = micrometers for the simulation\n
                `N` The number of spheres to place
                `packing_fraction` The packing fraction indicating the density; this is defined as the area occupied by the
                non-compressed spheres as compared to the actual available area (size_x times size_y)
                `theCanvas` possibility to transmit a `tkinter` `Canvas` object for graphical output\n
                `doDrawing` Flag to indicate whether graphical output should be produced or not
                `k` Central spring constant in (mg/s^2)/m of depth;
                so F=-k*x*L with L the depth of the stack (the simulation is 2D) and x the compression\n
                `nu` Central viscosity force constant in (mg/s)/m of depth. This is to have F=nu*v*L, L again the depth\n
                `m` is the average mass per unit of depth in mg/m of depth\n
                `bimodal_factor` is ratio of radii of the smaller and larger spheres in the bimodal distribution\n
                `k_t` Tangential spring constant in (mg/s^2)/m of depth;
                relevant for locked or permanent interfaces but not for slipping interfaces\n
                `nu_t` Central viscosity force constant in (mg/s)/m of depth.
                 Relevant for frictionally locked and permanent interfaces but not slipping ones\n
                `mu` Friction coefficient, describes the maximum interface force for non-permanent interfaces by
                 F_tangential_max = F_central*mu
                """

        super(EnsembleFriction, self).__init__(size_x, size_y, N, packing_fraction, theCanvas, doDrawing, k, nu,m,
                                               bimodal_factor=bimodal_factor)

        self.N = N
        """Number of spheres"""
        self.packing_fraction = packing_fraction
        """Packing fraction: relative area occupied by the uncompressed spheres as compared to the available area"""

        self.k_t=k_t
        """Transversal spring constant in (mg/s^2)/m of depth"""

        self.nu_t=nu_t
        """Transversal viscosity constant in (mg/s)/m of depth"""

        self.mu=mu
        """Friction coefficient"""

    def particle_info(self):
        """Provide short description of particle type of inclusion into output file

        Method defined in `particleShear.EnsembleFriction` """
        return "Frictional spheres, \n\tbimodal distribution, equal probability, \n\tr1="+\
               str(self.r_max*0.8/1.2)+"r2="+str(self.r_max)+"\n\tidentical mass="+str(self.sphereList[0].m)+"mg"



    def tangential_force(self):
        """Let all spheres calculate the total tangental force acting on them.

                 This will check for contact and so is more time
                 consuming than `particleShear.EnsembleFriction.tangential_force_from_neighbors`.
                 For this function to work, the spheres must be of type `particleShear.SphereFriction`or a
                 subclass thereof, or otherwise possess a method `tangential_force`\n
                 This method is defined in class `particleShear.EnsembleFriction`"""


        for sphereIndex in range(len(self.sphereList)):
            for sphereIndex2 in range(len(self.sphereList)):
                if sphereIndex != sphereIndex2:
                    self.sphereList[sphereIndex].tangential_force(self.sphereList[sphereIndex2],
                                                                  self.nu_t,self.mu,self.k,self.k_t)
            for sphereIndexBoundary in range(len(self.spheres_boundary)):
                self.sphereList[sphereIndex].tangential_force(self.spheres_boundary[sphereIndexBoundary],
                                                              self.nu_t,self.mu,self.k,self.k_t)
    def tangential_force_from_neighbors(self):
        """Let all spheres calculate the total tangential force acting on from their known neighbors.

                This is quicker than `particleShear.EnsembleFriction.tangential_force`
                but necessitates the neighbor relations to be already established via
                `particleShear.CanvasPointsNeighbors.test_neighbor_relation`.
                For this function to work, the spheres must be of type `particleShear.SphereFriction`or a
                subclass thereof, or otherwise possess a method `tangential_force_from_neighbors`.\n
                This method is defined in class `particleShear.EnsembleFriction`"""

        for sphereIndex in range(len(self.sphereList)):
            self.sphereList[sphereIndex].tangential_force_from_neighbors(self.nu_t,self.mu,self.k,self.k_t)

    def do_rotational_acceleration(self, dt):
        """Have the spheres calculate their rotational acceleration from the tangential forces.

                For this function to work,
                the spheres must be of type `particleShear.SphereFriction` or subclass thereof, or alternatively,
                possess a method `do_rotational_acceleration`\n
                This method is defined in class `particleShear.EnsembleFriction`"""
        for theSphere in self.sphereList:
            theSphere.do_rotational_acceleration(dt)


    def mechanical_simulation_step_calculate_forces(self):
        """ Calculate the forces acting on the spheres

        This method is defined in class `particleShear.EnsembleFriction`"""
        super(EnsembleFriction,self).mechanical_simulation_step_calculate_forces()
        self.tangential_force_from_neighbors()


    def mechanical_simulation_step_calculate_acceleration(self,cool_factor=0.97,dt=1):
        """Calculate the accelerations resulting from the forces

        This method is defined in class `particleShear.EnsembleFriction`"""
        self.do_linear_acceleration(dt)
        self.do_rotational_acceleration(dt)
        self.cool(cool_factor)























