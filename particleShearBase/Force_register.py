import math

class Force_register():
    """Provide accounting of the forces acting on the particles.

    Detailed accounting of the forces acting on the particles allows to calculate the relevant
    average stress tensors at each simulation time point by means of the
     `particleShear.StressTensorEvaluation` class.\n
     Sub-package particleShearBase"""

    def __init__(self):
        """Initialize the force register
        Provide default empty intance variables"""
        self.pair_register=[]
        """ Hold the elementary internal pairwise forces"""
        self.internal_moment_register = []
        """ Hold the fully internally generated torques"""
        self.total_particle_force_register=[]
        """ Hold the single total forces acting single particles"""
        self.external_force_register=[]
        """Hold single forces acting from the outside (across the canvas boudnary) on the particles"""
        self.external_moment_register = []
        """Hold single torques acting from the outside (across the canvas boudnary) on the particles"""
        self.unbalanced_moment_register = []
        """Hold the net torque moments causing rotational acceleration"""

    def reset_force_register(self):
        """Reset the force register to its original state

        This method is defined in class `particleShear.Force_register`"""

        self.pair_register = []

        self.total_particle_force_register = []  #

        self.external_force_register = []

        self.unbalanced_moment_register=[]

        self.internal_moment_register=[]

        self.external_moment_register = []

    def record_individual_internal_force(self,target,source,force_vector):
        """Record an individual internal force.

         The force magnitude and direction is described by the force_vector. The target describes the sphere on
         which the force acts (it is applied to the center); the source describes the sphere from which the force
         originates. Due to Newton's law of action an reaction, there should always be a second entry in the
         `particleShear.Force_register.pair_register` with opposing force vector, and exchanged source and target. However,
         this function does not check for the presence of such a homologous entry, this needs to be done in the code
         invoking this method.\n
         This method is defined in class `particleShear.Force_register`"""
        self.pair_register.append([target,source,force_vector])

    def record_total_particle_force(self,target,force_vector):
        """Record a net total particle force

        As there should be only one net particle force for each particle, the method first looks
        for an entry corresponding to target. If such an entry is found, the force is updated, otherwise a new
        entry is created

         Method defined in class `particleShear.Force_register`"""

        # First, look whether there is already an entry

        found_index = -1

        for ind in range(len(self.total_particle_force_register)):
            if self.total_particle_force_register[ind][0]==target:
                found_index=ind

        # If there is an entry, update it
        if(found_index>=0):
            self.total_particle_force_register[found_index][1]=force_vector
        else: # else add one
            self.total_particle_force_register.append([target,force_vector])

    def record_external_force(self, target, force_vector):
        """ Add an external force

        External forces are coming from either outside the area under examination or from that is not free to move
         (see `particleShear.CanvasPointsShear.canMove`)\n
         Method defined in class `particleShear.Force_register`"""

        self.external_force_register.append ([target, force_vector])

    def record_external_torque(self, target, moment):
        """ Add an external torque

        External torques are coming from either outside the area under examination or from that is not free to move
         (see `particleShear.CanvasPointsShear.canMove`)\n
         Method defined in class `particleShear.Force_register`"""

        self.external_moment_register.append ([target, moment])


    def record_individual_internal_torque(self,target,source,moment):
        """Record an individual internal moment.

         The torque is described by the moment argument. The target describes the sphere on
         which the torque acts (it is applied homogeneously to cause correct acceleration);
         the source describes the sphere which by frictional interaction has helped
         generate the moment (typically, in `particleShear.CircleFrictionElasticity.distribute_tangential_couple`).
         Since frictional interaction tends to generate
          torque on both partners, there is generally a second entry with target and source inversed. However,
         this function does not check for the presence of such a homologous entry, this needs to be done in the code
         invoking this method.\n
         This method is defined in class `particleShear.Force_register`"""
        self.internal_moment_register.append([target,source,moment])


    def record_unbalanced_moment(self,target,moment):
        """ Add net torque on a sphere

        As there should be only one net particle torque for each particle, the method first looks
        for an entry corresponding to target. If such an entry is found, the force is updated, otherwise a new
        entry is created

        Method defined in class `particleShear.Force_register`"""

        found_index = -1

        for ind in range(len(self.unbalanced_moment_register)):
            if self.unbalanced_moment_register[ind][0] == target:
                found_index = ind

        # If there is an entry, update it
        if (found_index >= 0):
            self.unbalanced_moment_register[found_index][1] = moment
        else:  # else add one
            self.unbalanced_moment_register.append([target, moment])





