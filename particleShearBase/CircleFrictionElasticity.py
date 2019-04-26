from tkinter import *
import random
import math

from .Force_register import Force_register

from .neighbor_relation import neighbor_relation

from .Graphical_output_configuration import Graphical_output_configuration

from .CircleBasicElasticity import CircleBasicElasticity

# Basic friction-less sphere with drawing functions
class CircleFrictionElasticity(CircleBasicElasticity):
    """Basic sphere with frictional interaction with drawing functions.

        In the 2D approach chosen here, this is a circle endowed with a central viscous and elastic forces (inherited), and
        additionnally tangential friction forces and rotational movement.
        Inherits from `particleShear.PointLeesEdwards`, so will respect Lees-Edwards boundary conditions
        provided `particleShear.PointLeesEdwards.use_lees_edwards` is set to True (default: False)"""

    def __init__(self, color, x, y, diameter, m=1, theCanvas=FALSE, doDrawing=FALSE,force_register=Force_register(),
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
        `use_lees_edwards` Explicit Should Lees-Edwards boundary conditions be used?\n
        """


        self.phi = -math.pi/2
        """Rotational position"""
        self.rotation_line = False
        """Should a line be drawn to indicate the current rotational position?"""

        self.omega=0
        """Current rotation speed, in rad/s"""
        self.torque=0
        """Current torque, in microN*m / (m of depth) for the simulation"""


        super(CircleFrictionElasticity, self).__init__(color, x, y, diameter, m,  theCanvas, doDrawing, force_register,
                                             use_lees_edwards=use_lees_edwards)
        self.inertia = self.m * self.r * self.r / 2
        """Rotational moment of inertia in mg*micrometers^2 / (m of depth)"""

    def cool(self,f=0.8,shear_rate_to_rotation_rate_coefficient=0):
        """Cool by decreasing local speed and rotation rate

         By inheritage from `particleShear.PointLeesEdwards` this includes SLLOD type of cooling, where only
         movement relative to the shearing environment is performed. This function adds cooling on particle rotation.
         There is some incertitude in the literature as to how the rotational aspect of shear should be counted, this
         can be addressed by introducing a conversion of shear rate to anticipated local rotation. By default, this is
         not used and rotation damped towards zero (shear_rate_to_rotation_rate_coefficient=0).\n
         This method is defined in class `particleShear.CircleFrictionElasticity`"""
        super(CircleFrictionElasticity,self).cool(f)
        omega_local = (self.shear_rate*(self.y-self.size_y/2))*shear_rate_to_rotation_rate_coefficient

        self.omega=omega_local+f*(self.omega-omega_local)

    def initiate_drawing(self):
        """Instiante the shapes representing this object on  `particleShear.Circle.theCanvas`.

        This method only has an effect if `particleShear.Circle.doDrawing` is True. If a shape is created, the reference to
        the circle on the canvas is stored in `particleShear.Circle.shape`. Compared to its parent method (
        `particleShear.Circle.initiate_drawing` defined in `particleShear.Circle`), here,
        a line indicating the rotational position `particleShear.CircleFrictionElasticity.phi` is optionnally added.
        This method is defined in class `particleShear.CircleFrictionElasticity`"""
        if self.doDrawing:
            super(CircleFrictionElasticity,self).initiate_drawing()
            if self.graphical_output_configuration.draw_rotation_line:
                pos = self.coordinates()
                x = pos[0]
                y = pos[1]
                self.rotation_line = self.theCanvas.create_line(x, y, x + self.r * math.cos(self.phi),
                                                                y + self.r * math.sin(self.phi),
                                                                fill=self.graphical_output_configuration.color_rotation_line
                                                                )

    def moveDrawing(self, dt):
        """Move for the drawing on the Tkinter canvas

        This method is defined in class `particleShear.CircleFrictionElasticity`"""
        super(CircleFrictionElasticity, self).moveDrawing(dt)
        self.theCanvas.delete(self.rotation_line)
        if self.graphical_output_configuration.draw_rotation_line:
            pos = self.coordinates()
            x = pos[0]
            y = pos[1]
            self.rotation_line = self.theCanvas.create_line(x, y, x + self.r * math.cos(self.phi),
                                                            y + self.r * math.sin(self.phi),
                                                            fill=self.graphical_output_configuration.color_rotation_line)

    def deleteDrawing(self):
        """Delete drawing on the Tkinter canvas

        This method is defined in class `particleShear.CircleFrictionElasticity`"""
        super(CircleFrictionElasticity, self).deleteDrawing()
        if self.theCanvas:
            self.theCanvas.delete(self.rotation_line)



    def tangential_speed(self, theSphere):
        """Tangential component of the relative speed of a given sphere relative to this object.

        The other sphere object needs to be of type `particleShear.CircleFrictionElasticity` or derived. Returns a scalar,
        describing the relative speed component parallel to a tangential vector with counter-clockwise orientation.
        The speed is returned in pixels/s (= micrometers/s for the simulation).\n
        This method adds to different origins of tangential velocity, as explained by eq. 6 in
        Otsuki, M. and H. Hayakawa,
        Discontinuous change of shear modulus for
        frictional jammed granular materials. Phys Rev E, 2017. 95(6-1): p. 062902: The first contribution is the
        difference in linear velocity of the two involved spheres, projected onto the common tangential  interface. This
        contribution is evaluated by invoking the parent method `particleShear.Circle.tangential_speed`
        defined in `particleShear.Circle`. The second part arises due to the rotation of the two neighboring spheres;
        this part is calculated and added here.\n
        This method is defined in class `particleShear.CircleFrictionElasticity`"""
        vt=super(CircleFrictionElasticity,self).tangential_speed(theSphere)

        pos=theSphere.coordinates()
        r=pos[2]

        return vt-(self.r*self.omega+r*theSphere.omega)


    def tangential_force(self, theSphere, nu,mu,k,k_t):
        """Calculate and appropriately distribute the tangential force of `theSphere` on the current object

        The calculation of the tangential force is calculated in a manner to ensure a high level of conservation of
        angular and linear momentum, including possible rounding errors. For this, it is safest to distribute the forces
        in a manner that conserves angular momentum and linear momentum rather than anticipating that an opposing force
        will arise when the same interface is considered from the point of view of the partner sphere. It could for instance
        happen that the other sphere considers the same interface as slipping while here it is locked and so the magnitude
        of force would be different.\n
        So when calculating the interface from the perspective of the current sphere, we
        count half the force but distribute it immediately and with conservation of both linear and angular momentum to the
        two involved spheres, by using the `particleShear.CircleFrictionElasticity.distribute_tangential_couple`. The same
        interface will be visited again from the perspective of `theSphere`, but even if the force magnitude is slightly
        different due to numerical or simulation imprecision, this will not generate a net linear or angular momentum.
        \n
        To further reduce chances of erroneous calculation, changes in slip / locked status of the interface are immediately
        transmitted to the partner interface under control of the partner sphere.\n
        Compared to Otsuki, M. and H. Hayakawa,
        Discontinuous change of shear modulus for frictional jammed granular materials.
        Phys Rev E, 2017. 95(6-1): p. 062902, this is intended to be the same torque compensation mechanism (eq. 8 of
        Otsuki et al.) except
        for that the actual separation distance is used and so angular momentum is conserved exactly,
        not just approximately.\n
        This method is defined in class `particleShear.CircleFrictionElasticity`
        """
        d = self.d(theSphere)
        pos = theSphere.coordinates()
        r = pos[2]

        foundNeighborIndex=self.findNeighborIndex(theSphere)

        found = foundNeighborIndex >= 0


        if found:

            # Check whether symmetric backlink exists

            backlink=self.neighbors[foundNeighborIndex].theSphere.findNeighborIndex(self)

            if(not backlink>=0):
                print("SphereLinkable: Asymmetric neighbor problem")




        if d < r + self.r:


            if not found:
                print("tangential_force: Problem with neighbors, found touching sphere not in neighbors list")
                return


            viscous_force=self.tangential_force_viscous(theSphere,nu)



            if abs(viscous_force-theSphere.tangential_force_viscous(self,nu)) > 1e-15:
                print("viscous force mis-match",viscous_force-theSphere.tangential_force_viscous(self,nu))





            elastic_force=self.tangential_force_elastic(theSphere,k_t)


            total_adherence_force = viscous_force+elastic_force
            friction_force=self.get_elastic_force(theSphere, k)*mu


            sig=1
            if(total_adherence_force<0):
                sig=-1

            if(abs(total_adherence_force)<=abs(friction_force)):
                self.neighbors[foundNeighborIndex].interface_type = "stick"
                theSphere.neighbors[backlink].interface_type = "stick"
            else:
                self.neighbors[foundNeighborIndex].interface_type = "slip"
                self.neighbors[foundNeighborIndex].friction_position=0
                theSphere.neighbors[backlink].interface_type = "slip"
                theSphere.neighbors[backlink].friction_position = 0

            force=min(abs(total_adherence_force),abs(friction_force))

            force=force*sig

            # The idea here is that the same friction point will be visited again when the neighboring sphere is examined,
            # so we assign only half the force here
            # The distribution is a bit complicated because of the conservation of angular momentum, so we use a dedicated function
            self.distribute_tangential_couple(theSphere, force/2)








    def tangential_force_from_neighbors(self, nu,mu,k,k_t):
        """Calculate and appropriately distribute the tangential forces from all known neighbors

        This method is defined in class `particleShear.CircleFrictionElasticity`
        """
        for neighbor in self.neighbors:
            self.tangential_force(neighbor.theSphere,nu,mu,k,k_t)


    def tangential_force_viscous(self, theSphere, nu):
        """Return the scalar value of the tangential vicous drag force on the current object by `theSphere

        This method is defined in class `particleShear.CircleFrictionElasticity`
        """
        d = self.d(theSphere)
        pos=theSphere.coordinates()
        r=pos[2]
        if d < r + self.r:
            return nu*self.tangential_speed(theSphere)
        else:
            return 0





    def distribute_tangential_couple(self, theSphere, force):
        """Distribution of a frictional couple on the two involved spheres

        The distribution of a frictional (tangential) couple of forces
        is a bit complicated because of the necessity of conservation of angular momentum. The friction force couple arises
        at a single point at the common contact surface of the two spheres, so it adds zero total angular momentum change as
        it ought to be for an internal force. It leads however to acceleration of the involved spheres, simulated by forces
        applied to the sphere center. This centrally applied force couple DOES apply a total torque, this is
        separation_distance * force. The separation_distance can be quite different from r1 + r2 since the spheres
        can be quite substantially compressed in the case of large packing densities, and so applying a compensatory torque of
        -r1*force respectively -r2*force as proposed by Otsuki et al. only partially solves the issue and leads to a net
        angular momentum that may add spuriously to the measured stress since this tends to turn the entire ensemble.\n
        The question of the actual distribution of the torque to the two spheres is a tricky one, since it is not a priori
        clear where the actual contact line will be (unequal compression of the two partners). To simplify, and for
        consistence with the solution by Otsuki et al. which is correct for non-compressed spheres, we distribute
        the torque proportional to the original particle radii\n
        This method is defined in class `particleShear.CircleFrictionElasticity`\n
        Otsuki et al. is Otsuki, M. and H. Hayakawa,
        Discontinuous change of shear modulus for frictional jammed granular materials.
        Phys Rev E, 2017. 95(6-1): p. 062902
        """

        t_vector = self.tangential_vector(theSphere)

        self.xforce = self.xforce + force * t_vector[0]
        self.yforce = self.yforce + force * t_vector[1]

        theSphere.xforce = theSphere.xforce - force * t_vector[0]
        theSphere.yforce = theSphere.yforce - force * t_vector[1]

        self.force_register.record_individual_internal_force(self,
                                                             theSphere,
                                                             [force * t_vector[0], force * t_vector[1]]
                                                             )

        self.force_register.record_individual_internal_force(theSphere,
                                                             self,
                                                             [-force * t_vector[0], -force * t_vector[1]]
                                                             )
        separation_distance=self.d(theSphere)
        # The equal distribution of the torque is an approximation that is OK if the spheres have about the same size
        # This might need reconsideration if spheres of very different sizes are used. However, the most important
        # is conservation of angular momentum, so the sum of the distribution factors must necessarily be 1.

        T_self = separation_distance * force*self.r/(self.r+theSphere.r)
        T_theSphere = separation_distance * force*theSphere.r/(self.r+theSphere.r)

        self.torque = self.torque + T_self
        theSphere.torque = theSphere.torque+T_theSphere

        self.force_register.record_individual_internal_torque(self,theSphere,T_self)
        self.force_register.record_individual_internal_torque(theSphere,self,T_theSphere)


    def tangential_force_elastic(self, theSphere, k_t):
        """Return the scalar value of the tangential elastic force on the current object by `theSphere`

        This method implements the elastic part of eq. 5 in Otsuki et al.
        This method is defined in class `particleShear.CircleFrictionElasticity`\n
         Otsuki et al. is Otsuki, M. and H. Hayakawa,
        Discontinuous change of shear modulus for frictional jammed granular materials.
        Phys Rev E, 2017. 95(6-1): p. 062902
        """
        d = self.d(theSphere)
        pos=theSphere.coordinates()
        r=pos[2]
        if d < r + self.r:
            found = FALSE
            foundNeighborIndex = -1
            for theNeighborIndex in range(len(self.neighbors)):
                theNeighbor = self.neighbors[theNeighborIndex]
                if (theSphere == theNeighbor.theSphere):
                    foundNeighborIndex = theNeighborIndex
                    found = TRUE
            if not found:
                print("Problem with neighbors, found touching sphere not in neighbors list")
            else:

                return k_t*self.neighbors[foundNeighborIndex].friction_position
        else:
            return 0

    def do_rotational_acceleration(self, dt):
        """Calculate and apply rotational accelaration from the accumulated torque

        This method is defined in class `particleShear.CircleFrictionElasticity`
        """
        self.omega = self.omega + self.torque/self.inertia*dt
        self.force_register.record_unbalanced_moment(self,self.torque)
        self.torque = 0

    def move(self, dt=1):
        """Move for time interval dt, including rotation, and including the graphical shape if present

        This method is defined in class `particleShear.CircleFrictionElasticity`"""

        self.phi = self.phi + self.omega * dt
        for theNeighbor in self.neighbors:
            if theNeighbor.interface_type=="stick" or theNeighbor.interface_type=="permanent":
                # This is not correct, to be corrected
                theNeighbor.friction_position=theNeighbor.friction_position+self.tangential_speed(theNeighbor.theSphere)*dt
        super(CircleFrictionElasticity, self).move(dt)



