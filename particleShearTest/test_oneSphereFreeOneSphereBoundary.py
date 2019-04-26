import unittest
from particleShear import *
from tkinter import *
import math



class TestoneSphereFreeOneSphereBoundary(unittest.TestCase):

    def setUp(self):



        size_x = 500
        size_y = 500

        theTk = Tk()
        theCanvas = Canvas(theTk, width=size_x, height=size_y)

        theCanvas.pack()

        theEnsemble = EnsembleLinkable(500, 500, 0, 0.8, theCanvas, True, k=1, nu=1, k_t=1, nu_t=1, mu=0.5)

        theEnsemble.sphereList.append(SphereLinkable("GREY", 150, 80, 120, m=1, my_index=1, theCanvas=theCanvas,
                                                     doDrawing=True, force_register=theEnsemble,
                                                     size_x=theEnsemble.size_x,
                                                     size_y=theEnsemble.size_y))

        theEnsemble.sphereList[0].xspeed = 10

        theEnsemble.sphereList.append(SphereLinkable("BLUE", 300, 10, 120, m=1, my_index=2, theCanvas=theCanvas,
                                                     doDrawing=True, force_register=theEnsemble,
                                                     size_x=theEnsemble.size_x,
                                                     size_y=theEnsemble.size_y))

        theEnsemble.sphereList[1].xspeed = -10

        theEnsemble.sphereList[1].omega = 0

        theEnsemble.applyingShear=True

        graphical = theEnsemble.graphical_output_configuration

        graphical.draw_rotation_line = True

        graphical.color_spheres_boundary="Green"

        graphical.draw_permanent_connections=True

        theEnsemble.set_graphical_output_configuration(graphical)

        #theEnsemble.sphereList[0].establish_permanent_link(theEnsemble.sphereList[1])

        theTk.update()

        theEvaluator = StressTensorEvaluation(size_x, size_y)

        self.theEvaluator = theEvaluator
        self.theEnsemble = theEnsemble
        self.theTk=theTk




        self.dt=0.1
        self.cool_factor=1

        for i in range(70):
            self.theEnsemble.mechanical_simulation_step_calculate_forces()

            self.theEnsemble.record_total_particle_forces()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)


            self.theEnsemble.mechanical_simulation_step_calculate_acceleration(cool_factor=self.cool_factor, dt=self.dt)
            self.theEnsemble.mechanical_simulation_step_calculate_movement(dt=self.dt)
            self.theTk.update()


    def tearDown(self):
        self.theTk.destroy()
        self.theTk = False





    def test_stress_tensor_LW(self):






        LW = self.theEvaluator.stress_tensor_LW





        self.assertTrue(LW[0][0]==0 and LW[0][1]==0 and LW[1][0]==0 and LW[1][1]==0)


    def test_overall_stress_tensor(self):



        overall = self.theEvaluator.overall_stress_tensor

        # Overall should be diagonal, with equal, negative diagonal elements

        self.assertTrue(overall[0][0]==overall[1][1])

        self.assertTrue(overall[0][1] == 0 and overall[1][0]==0)



    def test_external_stress_tensor(self):


        external = self.theEvaluator.stress_tensor_with_external_forces


        self.assertTrue(
            abs(external[0][0]) > 0 or abs(external[0][1]) > 0 or abs(external[1][0])>0
            or abs(external[1][1])>0)

    def test_unbalanced_forces_stress_tensor(self):




        unbalanced = self.theEvaluator.stress_tensor_unbalanced_forces

        external = self.theEvaluator.stress_tensor_with_external_forces


        external_tot = abs(external[0][0])+abs(external[0][1])+abs(external[1][0])+abs(external[1][1])


        self.assertTrue(
            abs(external[0][0] +unbalanced[0][0])/external_tot <1e-15)








if __name__ == '__main__':
    unittest.main()