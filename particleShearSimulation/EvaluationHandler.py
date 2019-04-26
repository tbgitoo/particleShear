from particleShearBase import StressTensorEvaluation
from particleShearBase import Force_register
import math

class EvaluationHandler():
    def __init__(self):
        self.strain = []
        self.strain_rate = []
        self.force = []
        self.t = []
        self.shear_stress=[]
        self.Gprime=0
        self.viscosity=0

        self.xg=[0,0] # Center of gravity, in microns
        self.total_mass = 0 # Total mass present, in mg
        self.v_mean=[0,0] # Mean speed, in micrometers/s

        self.angular_momentum_around_origin=0


        self.theEvaluator=False


        # Stress tensors to be stored

        self.stress_tensor_LW = []
        self.stress_tensor_linear_acceleration_otsuki = []
        self.stress_tensor_with_external_forces = []
        self.stress_tensor_linear_acceleration = []
        self.stress_tensor_unbalanced_forces = []
        self.stress_tensor_unbalanced_torque = []
        self.stress_tensor_internal_torque = []
        self.stress_tensor_spin_kinetic_energy = []
        self.overall_stress_tensor = []
        self.overall_stress_tensor2 = []

    def record(self, theEnsemble,theEvaluator=False):
        self.t.append(theEnsemble.t)


        if (not theEvaluator) and (not self.theEvaluator):
            self.theEvaluator=StressTensorEvaluation(theEnsemble.size_x,theEnsemble.size_y)
        if theEvaluator:
            self.theEvaluator=theEvaluator

        # Check whether the paired register is really paired


        sum_x = 0
        sum_y = 0
        total = 0
        for thePair in theEnsemble.force_register.pair_register:
            sum_x = sum_x + thePair[2][0]
            sum_y = sum_y + thePair[2][1]
            total = total + abs(thePair[2][0]+thePair[2][1])

        if total > 0:
            if not (abs(sum_x)/total<1e-14 and abs(sum_y)/total < 1e-14):
                print ("Stress tensor evaluation: Error in force register, paired forces do not match:",sum_x,sum_y)


        # Get the center of gravity:
        xg_x = 0
        xg_y = 0

        vm_x = 0
        vm_y = 0

        self.total_mass=0

        self.angular_momentum_around_origin=0

        for theSphere in theEnsemble.sphereList:
            self.total_mass=self.total_mass+theSphere.m
            xg_x = xg_x + theSphere.x*theSphere.m
            xg_y = xg_y + theSphere.y*theSphere.m

            vm_x = vm_x + theSphere.xspeed*theSphere.m
            vm_y = vm_y + theSphere.yspeed * theSphere.m

            self.angular_momentum_around_origin=self.angular_momentum_around_origin+\
                                                theSphere.m*theSphere.x*theSphere.yspeed-\
                                                theSphere.m*theSphere.y*theSphere.xspeed+\
                                                theSphere.omega*theSphere.inertia

        self.xg=[xg_x/self.total_mass,xg_y/self.total_mass]
        self.v_mean=[vm_x/self.total_mass,vm_y/self.total_mass]





        theEvaluator.evaluate_stress_tensors(theEnsemble.force_register,theEnsemble.movableSphereList(),theEnsemble.shear_rate)

        #print("EvaluationHandler: overall stress tensor ",theEvaluator.overall_stress_tensor)

        self.strain.append(theEnsemble.shear)
        self.strain_rate.append(theEnsemble.shear_rate)


        self.shear_stress.append(theEvaluator.evaluate_quasistatic_shear_stress()) # This is overall shear stress



        self.force.append(theEvaluator.evaluate_externally_applied_shear_stress()) # This is shear stress as theoretically defined by average surface force on
        # arbitrary sections.

        # Stress tensors to be stored
        self.stress_tensor_LW.append(theEvaluator.stress_tensor_LW)
        self.stress_tensor_linear_acceleration_otsuki.append(theEvaluator.stress_tensor_linear_acceleration_otsuki)
        self.stress_tensor_with_external_forces.append(theEvaluator.stress_tensor_with_external_forces)
        self.stress_tensor_linear_acceleration.append(theEvaluator.stress_tensor_linear_acceleration)
        self.stress_tensor_unbalanced_forces.append(theEvaluator.stress_tensor_unbalanced_forces)
        self.stress_tensor_unbalanced_torque.append(theEvaluator.stress_tensor_unbalanced_torque)
        self.stress_tensor_internal_torque.append(theEvaluator.stress_tensor_internal_torque)
        self.stress_tensor_spin_kinetic_energy.append(theEvaluator.stress_tensor_spin_kinetic_energy)
        self.overall_stress_tensor.append(theEvaluator.overall_stress_tensor)








        sum_strain=0
        sum_strain_rate=0

        self.Gprime=0
        self.viscosity=0

        for index in range(len(self.t)):
            sum_strain=sum_strain+self.strain[index]*self.strain[index]
            sum_strain_rate=sum_strain_rate+self.strain_rate[index]*self.strain_rate[index]
            self.Gprime=self.Gprime-self.strain[index]*self.shear_stress[index]
            self.viscosity=self.viscosity-self.strain_rate[index]*self.shear_stress[index]

        if sum_strain > 0:
            self.Gprime=self.Gprime/sum_strain
        if sum_strain_rate > 0:
            self.viscosity=self.viscosity/sum_strain_rate







