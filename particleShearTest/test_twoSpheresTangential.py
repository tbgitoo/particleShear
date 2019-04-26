import unittest
from particleShear import *
from tkinter import *
import math



class TestTwoSpheresTangential(unittest.TestCase):

    def setUp(self):



        size_x = 500
        size_y = 500

        theTk = Tk()
        theCanvas = Canvas(theTk, width=size_x, height=size_y)

        theCanvas.pack()

        theEnsemble = EnsembleLinkable(500, 500, 0, 0.8, theCanvas, True, k=1, nu=1, k_t=1, nu_t=1, mu=0.01)

        theEnsemble.sphereList.append(SphereLinkable("GREY", 150, 200, 120, m=1, my_index=1, theCanvas=theCanvas,
                                                     doDrawing=True, force_register=theEnsemble,
                                                     size_x=theEnsemble.size_x,
                                                     size_y=theEnsemble.size_y))

        theEnsemble.sphereList[0].xspeed = 0

        theEnsemble.sphereList.append(SphereLinkable("BLUE", 220, 260, 120, m=1, my_index=2, theCanvas=theCanvas,
                                                     doDrawing=True, force_register=theEnsemble,
                                                     size_x=theEnsemble.size_x,
                                                     size_y=theEnsemble.size_y))

        theEnsemble.sphereList[1].xspeed = 0

        theEnsemble.sphereList[1].omega = 0.25

        graphical = theEnsemble.graphical_output_configuration

        graphical.draw_rotation_line = True

        graphical.draw_permanent_connections=True

        theEnsemble.set_graphical_output_configuration(graphical)

        theEnsemble.sphereList[0].establish_permanent_link(theEnsemble.sphereList[1])

        theTk.update()

        theEvaluator = StressTensorEvaluation(size_x, size_y)

        self.theEvaluator = theEvaluator
        self.theEnsemble = theEnsemble
        self.theTk=theTk
        self.theEnsemble.k = 0
        self.theEnsemble.nu = 0


        self.dt=0.01
        self.cool_factor=1

        for i in range(50):
            self.theEnsemble.mechanical_simulation_step_calculate_forces()

            self.theEnsemble.record_total_particle_forces()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)

            # Chosen evaluation step: Take the coordinates before moving the spheres, these coordinates serve for the
            # basis of force calculation. The inter-sphere vector is
            self.L = [self.theEnsemble.sphereList[1].x - self.theEnsemble.sphereList[0].x,
                      self.theEnsemble.sphereList[1].y - self.theEnsemble.sphereList[0].y]


            # Generally, due to the change of friction position, the force can vary. This is only an issue with
            # k_t
            self.Ft1=self.theEnsemble.force_register.pair_register[6][2]
            self.Ft2 = self.theEnsemble.force_register.pair_register[5][2]
            self.Ft=[(self.Ft1[0]+self.Ft2[0])/2,(self.Ft1[1]+self.Ft2[1])/2 ]


            self.Ft_abs = math.sqrt(self.Ft[0] * self.Ft[0] + self.Ft[1] * self.Ft[1])
            self.L_abs = math.sqrt(self.L[0] * self.L[0] + self.L[1] * self.L[1])

            self.theEnsemble.mechanical_simulation_step_calculate_acceleration(cool_factor=self.cool_factor, dt=self.dt)
            self.theEnsemble.mechanical_simulation_step_calculate_movement(dt=self.dt)
            self.theTk.update()


    def tearDown(self):
        self.theTk.destroy()
        self.theTk = False





    def test_stress_tensor_LW(self):





        self.assertTrue(abs((self.Ft[0]*self.L[0]+self.Ft[1]*self.L[1])/self.L_abs/self.Ft_abs)<1e-15)

        test_tensor = [[0, 0], [0, 0]]

        # The idea here is that the reported transversal forces in the pair register are half of the force
        # because they are split between the two pairs

        test_tensor[0][0] = self.Ft[0] * self.L[0] * 1e-18 * 2 / (self.theEnsemble.size_x * 1e-6) / (
                    self.theEnsemble.size_y * 1e-6)
        test_tensor[0][1] = self.Ft[0] * self.L[1] * 1e-18 * 2 / (self.theEnsemble.size_x * 1e-6) / (
                self.theEnsemble.size_y * 1e-6)
        test_tensor[1][0] = self.Ft[1] * self.L[0] * 1e-18 * 2 / (self.theEnsemble.size_x * 1e-6) / (
                self.theEnsemble.size_y * 1e-6)
        test_tensor[1][1] = self.Ft[1] * self.L[1] * 1e-18 * 2 / (self.theEnsemble.size_x * 1e-6) / (
                self.theEnsemble.size_y * 1e-6)

        LW = self.theEvaluator.stress_tensor_LW





        self.assertTrue(abs(LW[0][0])>0 or abs(LW[0][1])>0 or abs(LW[1][0])>0 or abs(LW[1][1])>0)

        self.assertTrue(abs((LW[0][0]-test_tensor[0][0])/test_tensor[0][0])<1e-15 and
                        abs((LW[1][0] - test_tensor[1][0]) / test_tensor[1][0]) < 1e-15 and
                        abs((LW[0][1] - test_tensor[0][1]) / test_tensor[0][1]) < 1e-15 and
                        abs((LW[1][1] - test_tensor[1][1]) / test_tensor[1][1]) < 1e-15)

    def test_overall_stress_tensor(self):



        overall = self.theEvaluator.overall_stress_tensor

        overall_tot = abs(overall[0][0])+abs(overall[0][1])+abs(overall[1][0])+abs(overall[1][1])

        self.assertTrue(abs((overall[0][1] - overall[1][0]) / overall_tot) < 1e-15)

    def test_unbalanced_forces_stress_tensor(self):




        unbalanced = self.theEvaluator.stress_tensor_unbalanced_forces

        LW = self.theEvaluator.stress_tensor_LW


        LW_tot=abs(LW[0][0])+abs(LW[0][1])+abs(LW[1][0])+abs(LW[1][1])

        self.assertTrue(abs(LW[0][0] - unbalanced[0][0])/LW_tot < 1e-15 and
                        abs(LW[0][1] - unbalanced[0][1]) / LW_tot < 1e-15 and
                        abs(LW[1][0] - unbalanced[1][0]) / LW_tot < 1e-15 and
                        abs(LW[1][1] - unbalanced[1][1]) / LW_tot < 1e-15
                        )

    def test_external_stress_tensor(self):


        external = self.theEvaluator.stress_tensor_with_external_forces
        self.assertTrue(
            external[0][0] == 0 and external[0][1] == 0 and external[1][0] == 0 and external[1][1] == 0)

    def test_peculiar_acceleration_stress_tensor(self):


        peculiar = self.theEvaluator.stress_tensor_linear_acceleration_otsuki

    def test_stress_tensor_spin_kinetic_energy(self):

        stress_tensor_spin = self.theEvaluator.stress_tensor_spin_kinetic_energy

        # In theory, the spin kinetic energy should be I omega*w^2

        self.assertTrue(
            stress_tensor_spin[0][1] == stress_tensor_spin[1][0] )

    def test_stress_tensor_unbalanced_torque(self):

        for i in range(20):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)

        stress_tensor_torque = self.theEvaluator.stress_tensor_unbalanced_torque

        self.assertTrue(
             stress_tensor_torque[0][1] == -stress_tensor_torque[1][0])


    def test_conservation_linear_momentum(self):

        self.theEnsemble.mechanical_simulation_step_calculate_forces()

        self.theEnsemble.record_total_particle_forces()
        self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)
        theHandler = EvaluationHandler()

        theHandler.record(self.theEnsemble, self.theEvaluator)

        self.theEnsemble.mechanical_simulation_step_calculate_acceleration(cool_factor=self.cool_factor, dt=self.dt)
        self.theEnsemble.mechanical_simulation_step_calculate_movement(dt=self.dt)
        self.theTk.update()

        old_linear_momentum = theHandler.total_mass * theHandler.v_mean

        for i in range(100):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()

        self.theEnsemble.mechanical_simulation_step_calculate_forces()

        self.theEnsemble.record_total_particle_forces()
        self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)
        theHandler = EvaluationHandler()

        theHandler.record(self.theEnsemble, self.theEvaluator)

        self.theEnsemble.mechanical_simulation_step_calculate_acceleration(cool_factor=self.cool_factor, dt=self.dt)
        self.theEnsemble.mechanical_simulation_step_calculate_movement(dt=self.dt)
        self.theTk.update()

        new_linear_momentum = theHandler.total_mass * theHandler.v_mean

        if(math.sqrt(new_linear_momentum[0]*new_linear_momentum[0]+\
                                        new_linear_momentum[1]*new_linear_momentum[1])>1e-5):

            self.assertTrue(abs(old_linear_momentum[0] - new_linear_momentum[0]) \
                            / math.sqrt(new_linear_momentum[0]*new_linear_momentum[0]+\
                                        new_linear_momentum[1]*new_linear_momentum[1]) < 1e-15)

            self.assertTrue(abs(old_linear_momentum[1] - new_linear_momentum[1]) \
                            / math.sqrt(new_linear_momentum[0]*new_linear_momentum[0]+\
                                        new_linear_momentum[1]*new_linear_momentum[1]) < 1e-15)

        else:
            self.assertTrue(abs(old_linear_momentum[0]-new_linear_momentum[0])<1e-15)
            self.assertTrue(abs(old_linear_momentum[1] - new_linear_momentum[1]) < 1e-15)

    def test_conservation_angular_momentum(self):

        self.theEnsemble.mechanical_simulation_step_calculate_forces()

        self.theEnsemble.record_total_particle_forces()
        self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)
        theHandler = EvaluationHandler()

        theHandler.record(self.theEnsemble, self.theEvaluator)

        self.theEnsemble.mechanical_simulation_step_calculate_acceleration(cool_factor=self.cool_factor, dt=self.dt)
        self.theEnsemble.mechanical_simulation_step_calculate_movement(dt=self.dt)
        self.theTk.update()

        old_angular_momentum = theHandler.angular_momentum_around_origin

        for i in range(100):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()

        self.theEnsemble.mechanical_simulation_step_calculate_forces()

        self.theEnsemble.record_total_particle_forces()
        self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)
        theHandler = EvaluationHandler()

        theHandler.record(self.theEnsemble, self.theEvaluator)

        self.theEnsemble.mechanical_simulation_step_calculate_acceleration(cool_factor=self.cool_factor, dt=self.dt)
        self.theEnsemble.mechanical_simulation_step_calculate_movement(dt=self.dt)
        self.theTk.update()

        new_angular_momentum = theHandler.angular_momentum_around_origin


        self.assertTrue(abs((old_angular_momentum - new_angular_momentum) / new_angular_momentum) < 1e-14)


if __name__ == '__main__':
    unittest.main()