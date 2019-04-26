from tkinter import *
import random
import math

from .Force_register import Force_register

from .neighbor_relation import neighbor_relation

from .Graphical_output_configuration import Graphical_output_configuration

from .CircleMassNeighbors import CircleMassNeighbors

#
class CircleBasicElasticity(CircleMassNeighbors):
    """Basic friction-less sphere with drawing functions.

    In the 2D approach chosen here, this a circle endowed with a central repulsive elastic force along with viscous
     dissipation if it comes into contact with another sphere.
    Inherits from `particleShear.PointLeesEdwards`, so will respect Lees-Edwards boundary conditions
    provided `particleShear.PointLeesEdwards.use_lees_edwards` is set to True (default: False)"""
    def __init__(self, color, x, y, diameter, m=1,theCanvas=False, doDrawing=False,force_register=Force_register(),
                 use_lees_edwards=False):
        """Initialize self

        - **parameters**\n
        `x` The x-position of the center of the circle (in pixels, assumed micrometers for the simulation)\n
        `y` The y-position of the center of the circle (in pixels, assumed micrometers for the simulation)\n
        `diameter` The diameter of the circle  (in pixels, assumed micrometers for the simulation)\n
        `m` Mass of the sphere in mg (per m of depth). For the 2D representation, this is typically the mass in mg of a 1m high
        cylinder of diameter `diameter` in micrometers\n
        `theCanvas` Tkinter canvas; provide False if no Canvas is available or no drawing is desired\n
        `doDrawing` Explicit switch to turn of drawing\n
        `force_register`Possibility to provide a reference to a `particleShear.Force_register` variable to register the
        forces calculated during simulation\n
        `use_lees_edwards` Explicit Shoud Lees-Edwards boundary conditions be used?\n
        """

        super(CircleBasicElasticity,self).__init__(color,x,y,diameter,m=m, theCanvas=theCanvas,
                                                   doDrawing=doDrawing,force_register=force_register,
                                                   use_lees_edwards=use_lees_edwards)

        self.central_repulsion_coefficient=0
        """Central repulsion coefficient to help avoid spheres being able to fully penetrate and cross each other.

        The central_repulsion_coeffiecient is chosen from 0 (only linear law) to 1 
        (highest proportion of central repulsion). 
        When central_repulsion_coefficient>0, there is a 1/x contribution to induce very strong repulsion when 
        the spheres approach total compression and thus to avoid crossing of the spheres. For small compressions, 
        even if central_repulsion_coefficient>0, the equations are chosen to give a dF/dx law with a slope of -k 
        when the spheres just touch. See `particleShear.CircleBasicElasticity.get_elastic_force` further details"""






    #

    def get_elastic_force(self,theSphere,k=1):
        """Calculate magnitude of the central elastic force

        Scalar value of the elastic force exerted on this sphere. A negative value signifies that the current object
        is pushed back by the other sphere, a positive value signifies attraction (possible only with permanent
        interaction, not implemented in `particleShear.CircleBasicElasticity` but in some subclasses).\n
        Implementation of a central repulsive force: at large shear amplitudes and a strictly linear repulsion law,
        it may happen that spheres cross each other because the force is not enough to step movement despite the centers
        become nearly, or fully, identical. This is unphysical, and leads to entanglement between particles that we do
        no observe in this way. To avoid the effect, we need to add a component to the central elastic repulsive force that
        becomes very strong when the centers of the spheres get too close. At the same time, for small indentations, we
        aim at conserving a linear Hookes law (as in the paper underlying this implementation: see
        Eq. 2 from Otsuki, M. and H. Hayakawa,Discontinuous change of shear modulus for frictional
        jammed granular materials. Phys Rev E, 2017. 95(6-1): p. 062902.). Based on a 1/x law, we proceed as follows:\n
        The linear part is F=k*(x-xeq), providing the desired negative values for repulsion for x<xeq \n
        The nonlinear part is F=k*xeq*(1-xeq/x), which is also negative for xeq/x\n
        At x=xeq, both laws have dF/dx=k so that combining them in arbitrary mixing ratios does not change Hookes law
        for small indentations.\n
        This method is defined in class `particleShear.CircleBasicElasticity`"""

        d = self.d(theSphere)
        pos = theSphere.coordinates()
        r = pos[2]
        if d > r + self.r:
            return 0

        linear_force=-k*(1-self.central_repulsion_coefficient) * (self.r + r - d)
        nonlinear_addition=-k*self.central_repulsion_coefficient*(self.r + r)*((self.r+r)/max(d,(self.r + r)/1000)-1)


        return(linear_force+nonlinear_addition)






    def elastic_force(self, theSphere, k):
        """Calculate and apply elastic force excerted on this sphere by `theSphere`

        This method will check for contact and so is more time
        consuming than `particleShear.CircleBasicElasticity.elastic_force_from_neighbors` \n
        This method is defined in class `particleShear.CircleBasicElasticity`"""
        d = self.d(theSphere)
        pos = theSphere.coordinates()
        r = pos[2]
        if d < r + self.r:
            force = self.get_elastic_force(theSphere,k)
            n_vector=self.n(theSphere)


            self.applyInternalForceAndRegister([force*n_vector[0], force*n_vector[1]],theSphere)






    def elastic_force_from_neighbors(self,k):
        """
        Calculate the central elastic force from known neighbors.

        For this function, the neighbor relations need to be already established (via
        `particleShear.CircleMassNeighbors.test_neighbor_relation`).\n
        This method is defined in class `particleShear.CircleBasicElasticity`"""
        for neighbor in self.neighbors:
            self.elastic_force(neighbor.theSphere,k)

    # Eq. 3 from Otsuki, M. and H. Hayakawa,
    # Discontinuous change of shear modulus for frictional
    # jammed granular materials. Phys Rev E, 2017. 95(6-1): p. 062902.

    def central_viscous_force(self, theSphere, nu):
        """Calculate and apply the central viscous force on this sphere by a given sphere (`theSphere`)

        Eq. 3 from Otsuki, M. and H. Hayakawa,
        Discontinuous change of shear modulus for frictional
        jammed granular materials. Phys Rev E, 2017. 95(6-1): p. 062902. This method will check for contact and so is more time
        consuming than `particleShear.CircleBasicElasticity.central_viscous_force_from_neighbors`\n
        This method is defined in class `particleShear.CircleBasicElasticity`.
        """

        force = self.get_central_viscous_force(theSphere,nu)

        n_vector = self.n(theSphere)
        self.xforce = self.xforce + force * n_vector[0]
        self.yforce = self.yforce + force * n_vector[1]
        self.force_register.record_individual_internal_force(self,theSphere,[force * n_vector[0], force * n_vector[1]])

        return [force * n_vector[0], force * n_vector[1]]

    def get_central_viscous_force(self, theSphere, nu):
        """Calculate and apply the central viscous force on this sphere by a given sphere (`theSphere`)

        Eq. 3 from Otsuki, M. and H. Hayakawa,
        Discontinuous change of shear modulus for frictional
        jammed granular materials. Phys Rev E, 2017. 95(6-1): p. 062902. The magnitude of the viscous force depends
        on the relative speed. The convention is similar to the central elastic force (
        `particleShear.CircleBasicElasticity.get_elastic_force`). If the current object is
        repulsed by an approaching sphere (`theSphere`), a negative force is returned.\n
        This method is defined in class `particleShear.CircleBasicElasticity`.
        """
        v_rel = self.relative_speed(theSphere)

        vx_rel = v_rel[0]
        vy_rel = v_rel[1]

        norm_vector = self.n(theSphere)
        v_norm = vx_rel * norm_vector[0] + vy_rel * norm_vector[1]

        force = nu * v_norm

        return force


    def central_viscous_force_from_neighbors(self, nu):
        """Calculate the central viscous force from known neighbors.

        For this function, the neighbor relations need to be already established (via
        `particleShear.CircleMassNeighbors.test_neighbor_relation`).\n
        This method is defined in class `particleShear.CircleBasicElasticity`"""
        for neighbor in self.neighbors:
            self.central_viscous_force(neighbor.theSphere,nu)




