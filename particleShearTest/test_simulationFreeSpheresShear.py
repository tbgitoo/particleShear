import unittest
from particleShear import *
from tkinter import *
import math


def getSimulationFreeSpheresShear(theAmplitude=0.2,theMu=0.01,
                    cut_lines=5,Young_modulus_spheres=8000,
                    N=150,packing_fraction=1.5,density=50,bimodal_factor=1.4,
                    relative_viscosity=0.1,relative_transversal_link_strength=1,relative_frequency=0.025,
                    avoid_horizontal_angle_degree=15,interface_reenforcement_central=1,interface_reenforcement_tangential=1,
                    keep_viscosity_coefficients_constant=False,avoid_height_spanning_particles=True,cut_top_bottom=False,
                    imageFileType ="jpg",
                    remove_link_fraction=0,edge_fuzziness=0,
                    central_repulsion_coefficient=1,
                    doCutByTriangulation=True,doDrawing=True,relative_y_scale_force = 1e8,
                    pre_periods=2,periods=3,post_periods=1,cool_factor=0.5):



    root_folder = ""
    do_permanent_links = False
    saveOutputImages = False
    saveData = False



    theSimulation=Simulation_interlocking_rheology(
        root_folder, do_permanent_links=do_permanent_links, cut_lines=cut_lines, N=N,
        packing_fraction=packing_fraction,
        density=density,
        bimodal_factor=bimodal_factor,
        amplitude=theAmplitude, Young_modulus_spheres=Young_modulus_spheres, mu=theMu,
        relative_y_scale_force=relative_y_scale_force, relative_frequency=relative_frequency, relative_viscosity=relative_viscosity,
        relative_transversal_link_strength=relative_transversal_link_strength,
        central_repulsion_coefficient=central_repulsion_coefficient,
        avoid_horizontal_angle_degree=avoid_horizontal_angle_degree,
        interface_reenforcement_central=interface_reenforcement_central,
        interface_reenforcement_tangential=interface_reenforcement_tangential,
        keep_viscosity_coefficients_constant=keep_viscosity_coefficients_constant,
        avoid_height_spanning_particles=avoid_height_spanning_particles,
        cut_top_bottom=cut_top_bottom,
        doCutByTriangulation=doCutByTriangulation,
        remove_link_fraction=remove_link_fraction,
        edge_fuzziness=edge_fuzziness,
        doDrawing=doDrawing,
        saveData=saveData
    )
    theSimulation.function_call = theSimulation.function_call + \
                                  "\n\ttheSimulation.baseline_pre_periods = " + str(pre_periods) + \
                                  "\n\ttheSimulation.baseline_post_periods = " + str(post_periods) + \
                                  "\n\ttheSimulation.saveOutputImages = " + str(saveOutputImages) + \
                                  "\n\ttheSimulation.imageFileType = " + str(imageFileType) + \
                                  "\n\ttheSimulation.runSimulation(periods=" + str(periods) + ", cool_factor=" + \
                                  str(cool_factor) + ")"

    theSimulation.baseline_pre_periods = pre_periods
    theSimulation.baseline_post_periods = post_periods

    theSimulation.saveOutputImages = saveOutputImages
    theSimulation.imageFileType = imageFileType

    return(theSimulation)


def initiateSimulationFreeSpheresShear(theSimulation, cool_factor=1, periods=2, plotStress=True):

    theSimulation.initEnsemble(do_debug=True)

    model = theSimulation.theEnsemble.model

    y_scale_force = theSimulation.relative_y_scale_force / model.k / theSimulation.amplitude

    final_dt = theSimulation.theEnsemble.dt

    # if theSimulation.amplitude<0.01:

    #    final_dt=final_dt/(1-2*(math.log10(theSimulation.amplitude)+2))
    #    print("Small amplitude: Adjusted to dt=", final_dt)

    print("Setting relative frequency: " + str(theSimulation.relative_frequency))
    theSimulation.f = theSimulation.relative_frequency / model.time_constant

    fileName = theSimulation.file_path()

    if theSimulation.saveOutputImages:
        theSimulation.imageOutputFolder = theSimulation.image_folder_path(fileName)
        theSimulation.imageBaseFileName = "image"

    theFile = False
    if theSimulation.saveData:
        theFile = open(fileName, "w")

    theSimulation.write_information_on_simulation_to_file(theFile)

    print("Creating oscillatory shear experiment, dt = ", final_dt, " max dt = ", theSimulation.theEnsemble.dt_max)
    theExperiment = OscillatoryShearExperiment(theSimulation.theEnsemble, final_dt,
                                               theSimulation.f, theSimulation.amplitude, theFile,
                                               force_scale=y_scale_force,
                                               TkSimulation=theSimulation.theEnsemble.theTkSimulation,
                                               dt_max=theSimulation.theEnsemble.dt_max,
                                               imageOutputFolder=theSimulation.imageOutputFolder,
                                               imageBaseFileName=theSimulation.imageBaseFileName,
                                               imageFileType=theSimulation.imageFileType,
                                               plotStress=plotStress)

    theExperiment.periods = periods
    theExperiment.baseline_pre_periods = theSimulation.baseline_pre_periods
    theExperiment.baseline_post_periods = theSimulation.baseline_post_periods

    theExperiment.do_preequilibration_with_fixed_boundaries = True

    N_pre_equilibration_fixed_boundaries = 25 * theSimulation.adjustment_factor_for_bounded_preequilibration_steps()

    N_per_period = 1 / theSimulation.f / final_dt

    cf_per_dt = math.pow(cool_factor, 1 / N_per_period)

    # The idea here is that we have always the same attenuation per period
    print("cool factor per dt=", cf_per_dt)

    theSimulation.theExperiment = theExperiment

    theSimulation.cool_factor_per_dt = cf_per_dt




class TestSimulationFreeSpheresShear(unittest.TestCase):

    def setUp(self):

        self.imageOutputFolder=False

        self.theSimulation = getSimulationFreeSpheresShear(N=45,pre_periods=0.1)

        initiateSimulationFreeSpheresShear(self.theSimulation)


        self.theEnsemble = self.theSimulation.theEnsemble

        self.theExperiment = self.theSimulation.theExperiment


        N_pre_equilibration_fixed_boundaries=25

        self.theExperiment.final_cool_factor = 1

        self.theEvaluator = StressTensorEvaluation(self.theEnsemble.size_x, self.theEnsemble.size_y,
                                                   self.theEnsemble.theCanvas)


        self.theExperiment.pre_equilibrate(N=N_pre_equilibration_fixed_boundaries)

        self.theEnsemble.t = 0

        self.theEnsemble.applyingShear = True



        if self.theExperiment.plotStress and not self.theExperiment.theTk:
            self.theExperiment.theTk = Tk()

        if self.theExperiment.plotStress:
            self.theExperiment.outputCanvas = Canvas(
                self.theExperiment.theTk, width=self.theExperiment.width, height=self.theExperiment.height)

            self.theExperiment.outputCanvas.pack()

        self.theEnsemble.t = 0


        Time_required = (self.theExperiment.periods + self.theExperiment.baseline_pre_periods +\
                         self.theExperiment.baseline_post_periods) / self.theExperiment.f

        x_scale = self.theExperiment.width / Time_required

        self.theExperiment.plotter = EvaluationHandlerPlotter(self.theExperiment.theTk, self.theExperiment.outputCanvas, x_scale=x_scale,
                                                y_scale_force=self.theExperiment.force_scale,
                                                y_scale_strain=30 / self.theExperiment.amplitude, r=2, offset_x=0,
                                                offset_y=self.theExperiment.height / 2,
                                                plotStress=self.theExperiment.plotStress)

        N = int((self.theExperiment.periods*0.15 + self.theExperiment.baseline_pre_periods
                         ) / self.theExperiment.f / self.theExperiment.dt)

        print("Start application shear protocol, total N=", N, " steps")



        # ==============


        self.theEnsemble.t = 0



        for i in range(N):
            if i >= (self.theExperiment.baseline_pre_periods / self.theExperiment.f / self.theExperiment.dt) and i <= (
                    (self.theExperiment.periods + self.theExperiment.baseline_pre_periods) / self.theExperiment.f / self.theExperiment.dt):
                self.theEnsemble.setShearRate(
                    self.theExperiment.amplitude * self.theExperiment.out_of_phase_signal(self.theEnsemble.t) *
                    self.theExperiment.f * 2 * math.pi)
            else:
                self.theEnsemble.setShearRate(0)

            # Calculate forces, this registers individual forces in the force register

            self.theEnsemble.mechanical_simulation_step_calculate_forces()

            # report net particles forces and moments in the force register
            self.theEnsemble.record_total_particle_forces()

            self.theExperiment.plotter.record(self.theEnsemble, self.theEvaluator)

            # Do linear and rotational acceleration
            self.theEnsemble.mechanical_simulation_step_calculate_acceleration(cool_factor=
                                                                               self.theSimulation.cool_factor_per_dt,
                                                                               dt=self.theExperiment.dt)

            # Do linear and rotation movememnt
            self.theEnsemble.mechanical_simulation_step_calculate_movement(dt=self.theExperiment.dt)
            # reset forces for next round
            self.theEnsemble.reset_force()

            if self.theEnsemble.doDrawing:
                self.theExperiment.theTkSimulation.update()

        self.plotter = self.theExperiment.plotter








    def tearDown(self):
        if self.theSimulation.theEnsemble.theTkSimulation:
            self.theSimulation.theEnsemble.theTkSimulation.destroy()

        if self.theExperiment.theTk:
            self.theExperiment.theTk.destroy()

        self.theSimulation.theTkSimulation = False
        self.theExperiment.theTk = False



    def test_stress_tensors(self):


        theEvaluator=self.theEvaluator


        self.assertTrue(theEvaluator.stress_tensor_LW[0][0]>500 and theEvaluator.stress_tensor_LW[1][1]>500)
        self.assertTrue(abs(theEvaluator.stress_tensor_LW[0][1]/theEvaluator.stress_tensor_LW[0][0]) <0.1
                        and abs(theEvaluator.stress_tensor_LW[1][0]/theEvaluator.stress_tensor_LW[0][0]) <0.1)

        self.assertTrue(
            theEvaluator.overall_stress_tensor[0][0] > 500 and theEvaluator.overall_stress_tensor[1][1] > 500)

        self.assertTrue(abs(theEvaluator.overall_stress_tensor[0][1]-theEvaluator.overall_stress_tensor[1][0])/
              (abs(theEvaluator.overall_stress_tensor[0][0])+abs(theEvaluator.overall_stress_tensor[1][1]))<1e-15)


        linear_acceleration=self.theEvaluator.stress_tensor_linear_acceleration
        self.assertTrue(abs(linear_acceleration[0][0])<0.1*abs(theEvaluator.overall_stress_tensor[0][0]) and
                        abs(linear_acceleration[0][1]) < 0.1 * abs(theEvaluator.overall_stress_tensor[0][0]) and
                        abs(linear_acceleration[1][0]) < 0.1 * abs(theEvaluator.overall_stress_tensor[0][0]) and
                        abs(linear_acceleration[1][1]) < 0.1 * abs(theEvaluator.overall_stress_tensor[0][0]))

        external = self.theEvaluator.stress_tensor_with_external_forces
        self.assertTrue(abs((external[0][0]-theEvaluator.overall_stress_tensor[0][0])/theEvaluator.overall_stress_tensor[0][0])<0.1 and
                        abs((external[1][1]-theEvaluator.overall_stress_tensor[1][1])/theEvaluator.overall_stress_tensor[1][1]) < 0.1)

        print("external force")
        print(abs((external[0][0]-theEvaluator.overall_stress_tensor[0][0])/theEvaluator.overall_stress_tensor[0][0]))


if __name__ == '__main__':
    unittest.main()