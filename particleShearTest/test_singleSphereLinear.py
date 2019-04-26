import unittest
from particleShear import *
from tkinter import *
import math



class TestSingleSphereLinear(unittest.TestCase):

    def setUp(self):

        size_x = 500
        size_y = 500

        theTk = Tk()
        theCanvas = Canvas(theTk, width=size_x, height=size_y)

        theCanvas.pack()

        theEnsemble = EnsembleLinkable(size_x=size_x, size_y=size_y, N=0, packing_fraction=1, theCanvas=theCanvas,
                                       doDrawing=True)

        theEnsemble.sphereList.append(SphereLinkable("GREY", 150, 200, 120, m=1, my_index=1, theCanvas=theCanvas,
                                                     doDrawing=theEnsemble.doDrawing))

        theEnsemble.sphereList[0].xspeed = 0.7
        theEnsemble.sphereList[0].yspeed = 0.3
        # theEnsemble.set_graphical_output_configuration(theEnsemble.graphical_output_configuration)
        theTk.update()

        theEvaluator = StressTensorEvaluation(size_x, size_y)

        self.theEvaluator = theEvaluator
        self.theEnsemble = theEnsemble
        self.theTk=theTk



    def tearDown(self):
        self.theTk.destroy()
        self.theTk = False


    def test_stress_tensor_LW(self):
        for i in range(20):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)


        LW = self.theEvaluator.stress_tensor_LW
        self.assertTrue(LW[0][0]==0 and LW[0][1]==0 and LW[1][0]==0 and LW[1][1]==0)


    def test_overall_stress_tensor(self):

        for i in range(20):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)



        overall = self.theEvaluator.overall_stress_tensor
        self.assertTrue(overall[0][0]==0 and overall[0][1]==0 and overall[1][0]==0 and overall[1][1]==0)


    def test_unbalanced_forces_stress_tensor(self):

        for i in range(20):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)



        unbalanced = self.theEvaluator.stress_tensor_unbalanced_forces
        self.assertTrue(unbalanced[0][0]==0 and unbalanced[0][1]==0 and unbalanced[1][0]==0 and unbalanced[1][1]==0)

    def test_external_stress_tensor(self):

        for i in range(20):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)

        external = self.theEvaluator.stress_tensor_with_external_forces
        self.assertTrue(
            external[0][0] == 0 and external[0][1] == 0 and external[1][0] == 0 and external[1][1] == 0)


    def test_peculiar_acceleration_stress_tensor(self):

        for i in range(20):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)

        peculiar = self.theEvaluator.stress_tensor_linear_acceleration_otsuki

        self.assertTrue(
            peculiar[0][0] == 0 and peculiar[0][1] == 0 and peculiar[1][0] == 0 and peculiar[1][1] == 0)

    def test_conservation_angular_momentum(self):

        for i in range(20):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)

        theHandler = EvaluationHandler()

        theHandler.record(self.theEnsemble, self.theEvaluator)

        old_angular_momentum=theHandler.angular_momentum_around_origin

        for i in range(20):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)

        theHandler = EvaluationHandler()

        theHandler.record(self.theEnsemble, self.theEvaluator)

        new_angular_momentum=theHandler.angular_momentum_around_origin


        self.assertTrue( abs((old_angular_momentum-new_angular_momentum)/new_angular_momentum)<1e-15)

    def test_conservation_linear_momentum(self):

        for i in range(20):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)

        theHandler = EvaluationHandler()

        theHandler.record(self.theEnsemble, self.theEvaluator)


        old_linear_momentum=theHandler.total_mass*theHandler.v_mean

        for i in range(20):
            self.theEnsemble.mechanical_simulation_step(cool_factor=1, dt=.1)
            self.theTk.update()
            self.theEvaluator.evaluate_stress_tensors(self.theEnsemble.force_register, self.theEnsemble.sphereList, 0)

        theHandler = EvaluationHandler()

        theHandler.record(self.theEnsemble, self.theEvaluator)

        new_linear_momentum=theHandler.total_mass*theHandler.v_mean


        self.assertTrue( abs((old_linear_momentum[0]-new_linear_momentum[0])/new_linear_momentum[0])<1e-15)

        self.assertTrue(abs((old_linear_momentum[1] - new_linear_momentum[1]) / new_linear_momentum[1]) < 1e-15)


if __name__ == '__main__':
    unittest.main()