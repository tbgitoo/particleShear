from .Force_register import Force_register
from .Graphical_output_configuration import Graphical_output_configuration


class StressTensorEvaluation():
    """Class to evaluate mean stress tensor components from a `particleShear.Force_register`

    This class implements different expressions to evaluate mean force tensor components from the spatially localized
    force vectores as stored in  `particleShear.Force_register` variables\n
    Defined in sub-package particleShearBase"""


    def __init__(self,size_x,size_y,theCanvas=False):
        """ Initialize by setting all the mean stress tensor expression to 2x2 zero matrices"""
        self.size_x=size_x
        """ Width of the simulation area in micrometers"""
        self.size_y=size_y
        """ Height of the simulation area in micrometers"""

        self.overall_stress_tensor=[[0,0],[0,0]]
        """ Primary internal stress tensor, here implemented to be identical to 
        `particleShear.StressTensorEvaluation.stress_tensor_LW`"""


        self.stress_tensor_LW = [[0,0],[0,0]]
        """ Love-Weber definition of the stress tensor (see for instance
        eq. 18 of Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet, On the definition of the stress tensor 
        in granular media. International Journal of Solids and Structures, 
        2013. 50(14-15): p. 2508-2517.) Soil mechanics convention: normal is stress is positive for compression"""
        self.stress_tensor_unbalanced_forces = [[0, 0], [0, 0]]
        """ Non-compensated acceleration stress tensor (see for instance
        eq. 6 of Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet, On the definition of the stress tensor 
        in granular media. International Journal of Solids and Structures, 
        2013. 50(14-15): p. 2508-2517.) Soil mechanics convention: normal is stress is positive for compression"""
        self.stress_tensor_linear_acceleration_otsuki = [[0, 0], [0, 0]]
        """ Inertia compensation term given by eq. 15 of Otsuki, 
        M. and H. Hayakawa, Discontinuous change of shear modulus for frictional
        jammed granular materials. Phys Rev E, 2017. 95(6-1): p. 062902.
        We do not use this term as compared to Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet, On the definition of the stress tensor 
        in granular media. International Journal of Solids and Structures, 
        2013. 50(14-15): p. 2508-2517, acceleration seems to be missing."""

        self.stress_tensor_linear_acceleration=[[0, 0], [0, 0]]
        """ Linear acceleration stress tensor. Here, we neglect the effects of gravity, so the linear 
         acceleration is linked solely to the unbalanced force (see for instance
        eq. 6 of Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet, On the definition of the stress tensor 
        in granular media. International Journal of Solids and Structures, 
        2013. 50(14-15): p. 2508-2517.). We consider therefore that `particleShear.StressTensorEvaluation.stress_tensor_linear_acceleration` 
         is equal `particleShear.StressTensorEvaluation.stress_tensor_unbalanced_forces`. Soil mechanics convention: 
         normal is stress is positive for compression (which would lead to acceleration away from the center of the assembly)"""


        self.stress_tensor_with_external_forces=[[0,0],[0,0]]
        """Force stress tensor ascribed to external force (see 
                eq. 6 of Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet, On the definition of the stress tensor 
                in granular media. International Journal of Solids and Structures, 
                2013. 50(14-15): p. 2508-2517.) Soil mechanics convention: normal is stress is positive for compression"""

        self.stress_tensor_spin_kinetic_energy=[[0,0],[0,0]]
        """Tensile stress tensor reflecting centrifugal forces from the rotation of the particles.
            This is the last of of eq. 34 of Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet, On the definition of the stress tensor 
            in granular media. International Journal of Solids and Structures, 
            2013. 50(14-15): p. 2508-2517.), Corrected here by 
            replacing the 2/3 coefficient by a coefficient of 1 (we think there is an error 
            in Nicot et al. regarding the inertia matrix: eq. 29 in Nicot et al. should read 
            Xij=1/5.mp.rp^2.delta_ij=1/2.Jp.delta_ij instead of Xij=2/15.mp.rp^2.delta_ij=1/3.Jp.delta_ij).\n\n 
            We also reverse the sign 
             due to using the Soil mechanics convention: normal is stress is positive for compression, so this 
            is by definition negative for rotation rates different from 0
        """

        self.stress_tensor_unbalanced_torque = [[0, 0], [0, 0]]
        """Asymmetric stress tensor reflecting the unbalanced torques causing rotational acceleration of the particles.
            This is the second last term of eq. 34 of Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet, 
            On the definition of the stress tensor 
            in granular media. International Journal of Solids and Structures, 
            2013. 50(14-15): p. 2508-2517.), corrected here by 
            replacing the 2/3 coefficient by a coefficient of 1 (we think there is an error 
            in Nicot et al. regarding the inertia matrix: eq. 29 in Nicot et al. should read 
            Xij=1/5.mp.rp^2.delta_ij=1/2.Jp.delta_ij instead of Xij=2/15.mp.rp^2.delta_ij=1/3.Jp.delta_ij).\n\n 
             We also reverse the sign 
             due to using the Soil mechanics convention
        """

        self.stress_tensor_internal_torque = [[0, 0], [0, 0]]
        """Asymmetric stress tensor reflecting the purely internal interaction torques 
        causing rotational acceleration of the particles.
        With restriction to the purely internal torques (vs. externally applied ones), 
        this is the second last term of eq. 34 of Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet, 
        On the definition of the stress tensor 
        in granular media. International Journal of Solids and Structures, 
        2013. 50(14-15): p. 2508-2517.). We corrected here the expression given by Nicot et al. by 
        replacing the 2/3 coefficient by a coefficient of 1 (we think there is an error 
        in Nicot et al. regarding the inertia matrix: eq. 29 in Nicot et al. should read 
        Xij=1/5.mp.rp^2.delta_ij=1/2.Jp.delta_ij instead of Xij=2/15.mp.rp^2.delta_ij=1/3.Jp.delta_ij) 
        We also reverse the sign 
        due to using the Soil mechanics convention
        """

        self.theCanvas=theCanvas
        """Reference to Tkinter canvas for drawing forces"""
        self.graphical_output_configuration=Graphical_output_configuration()
        """`particleShear.Graphical_output_configuration` to configure drawing"""
        self.toDeleteList=[]
        """To move lines on Tkinter displays, one needs to delete them and redraw them, this is to keep track of 
        the currently active lines"""

    def evaluate_force_stress_tensors(self, force_register):
        """Evaluate the stress tensors linked to forces

        This method evaluates the terms `particleShear.StressTensorEvaluation.stress_tensor_LW`,
        `particleShear.StressTensorEvaluation.stress_tensor_unbalanced_forces` and
        `particleShear.StressTensorEvaluation.stress_tensor_with_external_forces` from the forces and locations
        stored in the force_register argument (of type `particleShear.Force_register`)

        The `particleShear.StressTensorEvaluation.stress_tensor_LW` is evaluated from the internal
        forces acting between pairs of spheres. This information is stored in the
        `particleShear.Force_register.pair_register` field of the `particleShear.Force_register`.
        The sign convention is such that if the spheres are excerting
         each repulsive forces on each other, positive normal (diagonal) elements result in
         `particleShear.StressTensorEvaluation.stress_tensor_LW`. Since repulsion arises if the ensemble is compressed,
         this means that the sign convention associates positive normal stress with a compressive state. This is the
         Soil mechanics sign convention (Fortin, J., O. Millet, and G. de Saxce,
         Construction of an averaged stress tensor for a granular medium.
         European Journal of Mechanics a-Solids, 2003. 22(4): p. 567-582.)

         The `particleShear.StressTensorEvaluation.stress_tensor_unbalanced_forces` is evaluated from the net
         forces acting on the individual internal spheres. This information is stored in the
        `particleShear.Force_register.total_particle_force_register` field of the `particleShear.Force_register`.
         The sign convention is such that if the spheres are being pushed away from the center of the assembly,
         positive normal (diagonal) elements result in `particleShear.StressTensorEvaluation.stress_tensor_unbalanced_forces`.
         Such net repulsion arises on a compressed, but not spatially restricted assembly; a typical situation would be
          free boundaries that allow the spheres to move away from ech other and a compressed initial assembly that then
          expands into the free available space.
         Since the sign convention followed here associates positive normal stress with a compressive state, this means
          that the Soil mechanics sign convention is followed (Fortin, J., O. Millet, and G. de Saxce,
         Construction of an averaged stress tensor for a granular medium.
         European Journal of Mechanics a-Solids, 2003. 22(4): p. 567-582.

         The `particleShear.StressTensorEvaluation.stress_tensor_with_external_forces` is evaluated from the boundary
        forces acting through the domain boundaries or via spheres on the boundaries with imposed movement.
        This information is stored in the
        `particleShear.Force_register.external_force_register` field of the `particleShear.Force_register`.
        The sign convention is such that if the spheres
        are on the average pushed inward, positive normal (diagonal) elements result in
         `particleShear.StressTensorEvaluation.stress_tensor_with_external_forces`. Average inward forces
          mean that the assembly is kept in a compressive state by the external forces. Association between compressive
          state and positive normal stresses corresponds to the
         Soil mechanics sign convention (Fortin, J., O. Millet, and G. de Saxce,
         Construction of an averaged stress tensor for a granular medium.
         European Journal of Mechanics a-Solids, 2003. 22(4): p. 567-582.)

         There is a particularity when using Lees-Edwards boundary conditions and Sllod stabilization of motion
         in oscillatory shear experiments (i.e. the primary conditions used here and in
         Otsuki, M. and H. Hayakawa, Discontinuous change of shear modulus for frictional
         jammed granular materials. Phys Rev E, 2017. 95(6-1): p. 062902.). The Sllod stabilization means that one
         considers only the excess momentum compared to the anticipated movement due to the general shearing of the
         assembly (see the peculiar momenta in Otsuki et al.; for the implementation of the shear speed change, see
          `particleShear.CanvasPointsBasicElasticityLeesEdwards.adjust_sphere_speed_to_shear_rate_change`
          in class  `particleShear.CanvasPointsBasicElasticityLeesEdwards`
          ). This means that the inertial forces that would be needed to accelerate
         the overall assembly to the
         local shearing speeds are ignored. For low frequencies and amplitudes, this becomes negligeable, but at higher
         shear and frequencies, the simulation will not take into account a large part of the inertial forces, whereas
         a rheological measurement would, at least before correction for inertia.

        `particleShear.StressTensorEvaluation.stress_tensor_linear_acceleration`
         is set equal to  `particleShear.StressTensorEvaluation.stress_tensor_unbalanced_forces`
         since we neglect gravity here

        Method defined in `particleShear.StressTensorEvaluation`"""
        self.stress_tensor_LW = [[0, 0], [0, 0]]
        self.stress_tensor_unbalanced_forces = [[0, 0], [0, 0]]
        self.stress_tensor_linear_acceleration = [[0, 0], [0, 0]]
        self.stress_tensor_with_external_forces = [[0, 0], [0, 0]]

        for pair in force_register.pair_register:
            target=pair[0]

            source=pair[1]

            force=pair[2]

            delta_x = [target.x-source.x, target.y-source.y]



            for i in range(2):
                for j in range(2):
                    self.stress_tensor_LW[i][j] = self.stress_tensor_LW[i][j] + force[i]*1e-12 * delta_x[j] * 1e-6 / 2

        for i in range(2):
            for j in range(2):
                self.stress_tensor_LW[i][j] = self.stress_tensor_LW[i][j]/(self.size_x*1e-6)/(self.size_y*1e-6)

        for single in force_register.total_particle_force_register:
            target = single[0]
            force = single[1]
            delta_x = [target.x-self.size_x/2 , target.y-self.size_y/2 ]



            for i in range(2):
                for j in range(2):
                    self.stress_tensor_unbalanced_forces[i][j] = self.stress_tensor_unbalanced_forces[i][j] + force[i]*1e-12 * delta_x[j] * 1e-6

        for i in range(2):
            for j in range(2):
                self.stress_tensor_unbalanced_forces[i][j] = self.stress_tensor_unbalanced_forces[i][j]/(self.size_x*1e-6)/(self.size_y*1e-6)



        if self.theCanvas:
            for theLine in self.toDeleteList:
                self.theCanvas.delete(theLine)



        for external_force in force_register.external_force_register:
            target = external_force[0]
            force = external_force[1]

            r = [target.x-self.size_x/2, target.y-self.size_y/2]

            if self.theCanvas and self.graphical_output_configuration.draw_boundary_forces:
                self.toDeleteList.append(
                    self.theCanvas.create_line(target.x,target.y,target.x+force[0]*1000,target.y+force[1]*1000,fill="darkorchid"))

            for i in range(2):
                for j in range(2):
                    self.stress_tensor_with_external_forces[i][j] = self.stress_tensor_with_external_forces[i][j]\
                                                                    -force[i]*1e-12 * r[j] * 1e-6



        for i in range(2):
            for j in range(2):
                self.stress_tensor_with_external_forces[i][j] = \
                    self.stress_tensor_with_external_forces[i][j]/(self.size_x*1e-6)/(self.size_y*1e-6)


        for i in range(2):
            for j in range(2):
                # These are synonyms as we do not include gravity
                self.stress_tensor_linear_acceleration[i][j]=self.stress_tensor_unbalanced_forces[i][j]

    def evaluate_spin_kinetic_energy_stress_tensor(self,theSphereList):
        """Evaluate the stress tensor associated with the centrifugal forces arising by rotation of the
        spheres around their axis

        The tensile stress tensor reflects the centrifugal forces from the rotation of the particles.
        This is the spin kinetic term in eq. 34 of Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet,
        On the definition of the stress tensor
        in granular media. International Journal of Solids and Structures,
        2013. 50(14-15): p. 2508-2517.),
        corrected by replacing the 2/3 coefficient by a coefficient of 1. See instance
        variable `particleShear.StressTensorEvaluation.stress_tensor_spin_kinetic_energy`.\n\n
        We also reverse the sign due to using the Soil mechanics convention:
        normal is stress is positive for compression, so this
        is by definition negative for rotation rates different from 0\n\n
        Method defined in `particleShear.StressTensorEvaluation`
        """



        self.stress_tensor_spin_kinetic_energy = [[0, 0], [0, 0]]

        for theSphere in theSphereList:
            # The moment of inertia is in mg*micrometers^2, but we need it in kg*m^2 here. The
            # unit conversion factor is therefore 10^(-18)

            moment_of_inertia = theSphere.inertia * 1e-18
            K = theSphere.omega *theSphere.omega / 2 * moment_of_inertia
            for i in range(2):
                self.stress_tensor_spin_kinetic_energy[i][i] = self.stress_tensor_spin_kinetic_energy[i][i] - K
        # Now, with respect to the sampling volume
        for i in range(2):
            for j in range(2):
                self.stress_tensor_spin_kinetic_energy[i][j] = self.stress_tensor_spin_kinetic_energy[i][j] \
                                                               / (self.size_x * 1e-6) / (self.size_y * 1e-6)


    def evaluate_unbalanced_torque_stress_tensor(self,force_register):
        """Evaluate the stress tensor associated with overall unbalanced torques acting on the particle

         The unbalanced torque stress tensor reflects the asymmetric contribution of torques leading
          to acceleration or deceleration of the rotation of the particles.
          This is the moment term in eq. 34 of Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet,
          On the definition of the stress tensor
          in granular media. International Journal of Solids and Structures,
          2013. 50(14-15): p. 2508-2517.),
          corrected by replacing the 2/3 coefficient by a coefficient of 1. See instance
          variable `particleShear.StressTensorEvaluation.stress_tensor_unbalanced_torque`.\n\n
          We also reverse the sign due to using the Soil mechanics convention, implying sign reversal as
          compared to Nicot et al.\n\n
          Method defined in `particleShear.StressTensorEvaluation`
          """


        self.stress_tensor_unbalanced_torque= [[0, 0], [0, 0]]

        # The spring constant is in mg/s-2/m of depth, and is multiplied with micrometers to get the forces
        # So the force have the units micrometers*mg/s-2/m
        # For the torque, this is further multiplied by micrometers, so that makes
        # micrometers^2/mg/s-2/m of depth

        for unbalanced_torque in force_register.unbalanced_moment_register:
            M = unbalanced_torque[1]*1e-18
            self.stress_tensor_unbalanced_torque[0][1]=self.stress_tensor_unbalanced_torque[0][1]-M/2
            self.stress_tensor_unbalanced_torque[1][0] =self.stress_tensor_unbalanced_torque[1][0]+M/2
            # Now, with respect to the sampling volume
        for i in range(2):
            for j in range(2):
                self.stress_tensor_unbalanced_torque[i][j] = self.stress_tensor_unbalanced_torque[i][j] \
                                                               / (self.size_x * 1e-6) / (self.size_y * 1e-6)

    def evaluate_internal_torque_stress_tensor(self,force_register):
        """Evaluate the stress tensor associated with internal unbalanced torques acting on the particle

        The internal unbalanced torque stress tensor reflects the asymmetric contribution of torques arising
        from frictional particle-particle interaction strictly within the simulation area.
        This is the moment term in eq. 34 of Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet,
        On the definition of the stress tensor
        in granular media. International Journal of Solids and Structures,
        2013. 50(14-15): p. 2508-2517.), restricted to the internal torques, and
        corrected by replacing the 2/3 coefficient by a coefficient of 1. See instance
        variable `particleShear.StressTensorEvaluation.stress_tensor_internal_torque`.\n\n
        We also reverse the sign due to using the Soil mechanics convention, implying sign reversal as
        compared to Nicot et al.\n\n
        Method defined in `particleShear.StressTensorEvaluation`
        """


        self.stress_tensor_internal_torque= [[0, 0], [0, 0]]

        # The spring constant is in mg/s-2/m of depth, and is multiplied with micrometers to get the forces
        # So the force have the units micrometers*mg/s-2/m
        # For the torque, this is further multiplied by micrometers, so that makes
        # micrometers^2/mg/s-2/m of depth

        for internal_torque in force_register.internal_moment_register:
            M = internal_torque[2]*1e-18
            self.stress_tensor_internal_torque[0][1]=self.stress_tensor_internal_torque[0][1]-M/2
            self.stress_tensor_internal_torque[1][0] =self.stress_tensor_internal_torque[1][0]+M/2
            # Now, with respect to the sampling volume
        for i in range(2):
            for j in range(2):
                self.stress_tensor_internal_torque[i][j] = self.stress_tensor_internal_torque[i][j] \
                                                               / (self.size_x * 1e-6) / (self.size_y * 1e-6)

    def evaluate_rotational_stress_tensors(self,force_register,theSphereList):
        """Evaluate the rotational stress tensors

        This function invokes `particleShear.StressTensorEvaluation.evaluate_spin_kinetic_energy_stress_tensor`,
        `particleShear.StressTensorEvaluation.evaluate_unbalanced_torque_stress_tensor` and
        `particleShear.StressTensorEvaluation.evaluate_internal_torque_stress_tensor`. The results are stored in the
        instance variables `particleShear.StressTensorEvaluation.stress_tensor_spin_kinetic_energy`, `particleShear.StressTensorEvaluation.stress_tensor_unbalanced_torque`
        and `particleShear.StressTensorEvaluation.stress_tensor_internal_torque` \n\n
        Method defined in `particleShear.StressTensorEvaluation`
        """

        self.evaluate_spin_kinetic_energy_stress_tensor(theSphereList)
        self.evaluate_unbalanced_torque_stress_tensor(force_register)
        self.evaluate_internal_torque_stress_tensor(force_register)



    def evaluate_peculiar_momentum_transport_for_linear_acceleration_tensor(self,theSphereList,shear_rate):
        """ Evaluate the inertial compensation term defined by Otsuki et al.

        This term is the inertial compensation term (second righthand term) in eq. 15 of Otsuki, M. and H. Hayakawa,
        Discontinuous change of shear modulus for frictional
        jammed granular materials. Phys Rev E, 2017. 95(6-1): p. 062902. We provide this term for completeness. This term
        does not appear as such in other main references on shear tensors in granular media (Nicot, F., N. Hadda,
        M. Guessasma, J. Fortin, and O. Millet,
        On the definition of the stress tensor in granular media.
        International Journal of Solids and Structures, 2013. 50(14-15): p. 2508-2517.), and it seems to have
        unphysical aspects. Consider a simplified assembly made from a single sphere without applied shear,
        moving linearly without applied force. All elements of the stress tensor should be zero for such a freely moving
        sphere free from any applied external force.
        If the speed of the sphere is not exactly along the x- or y-direction, the inertial compensation term by Otsuki et al.
        is non-zero, and this should not be.
        So while we provide the inertial term by Otsuki et al. for completeness, we do not
        recommend using it.

        Method defined in `particleShear.StressTensorEvaluation`"""

        self.stress_tensor_linear_acceleration_otsuki = [[0, 0], [0, 0]]


        for theSphere in theSphereList:
            # Units: forces are in N
            # the mass is in mg
            # the length scales are in micrometer
            # so here to kgm/s one needs to multiply by 10^-12
            px=(theSphere.xspeed-shear_rate*(theSphere.y-self.size_y/2))*theSphere.m*1e-12
            py=theSphere.yspeed*theSphere.m*1e-12
            p=[px,py]

            for i in range(2):
                for j in range(2):
                    # Eq. 15 of Otsuki, M. and H. Hayakawa, Discontinuous change of shear modulus for frictional
                    # jammed granular materials. Phys Rev E, 2017. 95(6-1): p. 062902.
                    # This doesn't seem to be quite right as it doesn't seem to involve acceleration
                    self.stress_tensor_linear_acceleration_otsuki[i][j] = self.stress_tensor_linear_acceleration_otsuki[i][j]-\
                                                                   p[i]*p[j]/theSphere.m*1e6


        for i in range(2):
            for j in range(2):
                self.stress_tensor_linear_acceleration_otsuki[i][j] = \
                    self.stress_tensor_linear_acceleration_otsuki[i][j]/(self.size_x*1e-6)/(self.size_y*1e-6)


    def evaluate_stress_tensors(self,force_register,theSphereList,shear_rate):
        """Evaluate the stress tensor expressions

        This is the main method to be called for stress tensor evaluation. It uses the forces stored in the various
        fields of the force_register to evaluate the stress tensor expressions linked to forces via
        `particleShear.StressTensorEvaluation.evaluate_force_stress_tensors`. The method also calls
        `particleShear.StressTensorEvaluation.evaluate_peculiar_momentum_transport_for_linear_acceleration_tensor`,
        see these two methods for further details.

        Finally, the relevant overall internal force stress tensor
        (`particleShear.StressTensorEvaluation.overall_stress_tensor`) is set equal to the Love-Weber expression. This
         intrinsically compensates for inertia by local acceleration, but it
        ignores the spin terms (rotation of the spheres and change in rotation rate). The approximation is justified by
        the quasistatic conditions used in the simulations, but may need improved implementation in the future for
        simulations with rapidly spinning ("rolling") particles.

        Method defined in `particleShear.StressTensorEvaluation`"""


        self.evaluate_force_stress_tensors(force_register)
        self.evaluate_peculiar_momentum_transport_for_linear_acceleration_tensor(theSphereList,shear_rate)
        self.evaluate_rotational_stress_tensors(force_register,theSphereList)

        self.overall_stress_tensor=[[0,0],[0,0]]
        for i in range(2):
            for j in range(2):
                # Compensation for linear acceleration as in Nicot, F., N. Hadda, M. Guessasma, J. Fortin, and O. Millet, On
                # the definition of the stress tensor in granular media.
                # International Journal of Solids and Structures, 2013. 50(14-15): p. 2508-2517.
                # Also, taking into account only internal torque
                self.overall_stress_tensor[i][j] = self.overall_stress_tensor[i][j]+self.stress_tensor_LW[i][j] \
                                                   +self.stress_tensor_internal_torque[i][j]\
                                                   +self.stress_tensor_spin_kinetic_energy[i][j]




    def evaluate_quasistatic_shear_stress(self):
        """Evaluate the internal shear stress

        From the stress tensor (`particleShear.StressTensorEvaluation.overall_stress_tensor`) calculated from the
        internal forces, evaluate the shear stress (xy element). Since an external measurement apparatus would
        have to provide a force opposing the shear stress force arising at the surface, we invert signs and return the
        negative of the xy element of `particleShear.StressTensorEvaluation.overall_stress_tensor`.

        Method defined in `particleShear.StressTensorEvaluation`"""


        return (-self.overall_stress_tensor[0][1])

    def evaluate_externally_applied_shear_stress(self):
        """Evaluate the shear stress from the external forces acting on the ensemble

        From the external force stress tensor
        (`particleShear.StressTensorEvaluation.stress_tensor_with_external_forces`) calculated from the
        externally acting forces, evaluate the shear stress (xy element). To account for the fact that
        the force on an external measurement apparatus would be the inverse of the force applied on the
        boundary paraticles, we return the negative of the xy element of the
        `particleShear.StressTensorEvaluation.stress_tensor_with_external_forces`.

         Method defined in `particleShear.StressTensorEvaluation`"""


        return (-self.stress_tensor_with_external_forces[0][1])












