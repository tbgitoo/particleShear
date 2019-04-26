from tkinter import *
from particleShearBase import *
from particleShearObjects import *
from particleShearLinkableObjects import *
from .EvaluationHandlerPlotter import EvaluationHandlerPlotter
from .EvaluationHandler import  EvaluationHandler
import math
import io
from PIL import Image



class OscillatoryShearExperiment():
    # The plotStress variable serves as a switch to enable/disable output plotting, while leaving everything else the same
    def __init__(self, theEnsemble,dt,f,amplitude,output_file,dt_max=0,TkSimulation=False,force_scale=1,theTkOutput=False,
                 imageOutputFolder=False,imageBaseFileName=False,imageFileType = "jpg",plotStress=True,
                 saveStressTensorData=True):
        self.plotStress=plotStress
        print("OscillatoryShearExperiment: Plot stress graph:",self.plotStress)
        self.theEnsemble=theEnsemble
        self.amplitude=amplitude
        self.dt = dt
        self.f = f
        self.theTk = theTkOutput
        # The idea here is to be able to handle an external Tk so that the rest of the program can do something with the
        # graphical output
        self.external_output_Tk=False
        if self.theTk:
            self.external_output_Tk = True
        self.width=1000
        self.height=500
        self.outputCanvas = False
        self.output_file = False
        self.dt_max = 10*dt
        self.theTkSimulation=TkSimulation
        if dt_max>dt:
            self.dt_max = dt_max

        self.plotter = False
        self.theEvaluator = False
        self.baseline_pre_periods = 0 # Acquisition of stress data with 0
            # excitation amplitude to have a baseline before oscillatory shear
        self.baseline_post_periods = 0 # Acquisition of stress data with 0
        # excitation amplitude to have a baseline before oscillatory shear
        self.periods=2
        self.force_scale=force_scale
        self.output_file=output_file

        self.final_cool_factor=1

        self.do_preequilibration_with_fixed_boundaries=True


        self.imageOutputFolder=imageOutputFolder

        self.imageBaseFileName = imageBaseFileName

        self.imageFileType = imageFileType # can be either jpg or ps

        self.saveStressTensorData=saveStressTensorData





    def free_pre_equilibration(self):


        print("Free pre-equilibration, dt_max",self.dt_max, "dt = ",self.dt)
        self.theEnsemble.applyingShear = False
        dt=self.dt_max
        N = 10
        cool_factor=0.5
        if self.theEnsemble.mu > 0:
            N=int(20 * (2 - math.log10(self.theEnsemble.mu)))
        while dt>self.dt:
            print("dt=", dt)
            self.theEnsemble.mechanical_relaxation(dt=dt, theTk=self.theTkSimulation,
                    N=N, cool_factor=cool_factor)
            dt=dt/2
            cool_factor=(1+cool_factor)/2
            self.theEnsemble.correct_linear_drift()
        dt = self.dt
        print("dt=", dt)
        self.theEnsemble.mechanical_relaxation(dt=dt, theTk=self.theTkSimulation,
                    N=N, cool_factor=1)


    def pre_equilibrate(self,  N=25,cool_factor=0.99):

        print("Pre-equilibration under experimental conditions, Steps per dt:",N," max dt",self.dt_max," final dt",self.dt)

        self.theEnsemble.applyingShear = True
        dt = self.dt_max
        cf=0.5

        while dt > self.dt:
            print("dt=", dt)
            self.theEnsemble.mechanical_relaxation(dt=dt, theTk=self.theTkSimulation,
                                                   N=int(N/2), cool_factor=cf)
            dt = dt / 2
            cf = (1 + cf) / 2

        dt = self.dt
        print("  Setting final dt=", dt)
        self.theEnsemble.mechanical_relaxation(dt=dt, theTk=self.theTkSimulation,
                                               N=N*2, cool_factor=0.98)


        for i in range(N):
            self.theEnsemble.shear_rate = 0
            self.theEnsemble.mechanical_simulation_step(cool_factor, self.dt)
            self.theEnsemble.reset_force()
            if self.theEnsemble.doDrawing:
                self.theTkSimulation.update()


    def oscillatory_shear_experiment(self, cool_factor=1,N_pre_equilibration_fixed_boundaries=25):


        self.theEvaluator = StressTensorEvaluation(self.theEnsemble.size_x, self.theEnsemble.size_y,
                                              self.theEnsemble.theCanvas)

        self.final_cool_factor = cool_factor

        self.write_experiment_description_information_to_file()

        if(self.do_preequilibration_with_fixed_boundaries):
            self.pre_equilibrate(cool_factor=cool_factor,N=N_pre_equilibration_fixed_boundaries)

        self.theEnsemble.t=0

        self.theEnsemble.applyingShear = True

        if self.plotStress and not self.theTk:

            self.theTk=Tk()


        if self.plotStress:
            self.outputCanvas = Canvas(self.theTk, width=self.width, height=self.height)

            self.outputCanvas.pack()



        self.theEnsemble.t=0



        Time_required = (self.periods+self.baseline_pre_periods+self.baseline_post_periods) / self.f

        x_scale = self.width/Time_required



        self.plotter=EvaluationHandlerPlotter(self.theTk, self.outputCanvas, x_scale=x_scale,
                                 y_scale_force=self.force_scale,
                                 y_scale_strain=30 / self.amplitude, r=2, offset_x=0,
                                 offset_y=self.height / 2,plotStress=self.plotStress)



        N=int(Time_required/self.dt)

        print("Start application shear protocol, total N=",N," steps")

        # plan to output 200 images in total

        image_N=1

        if N>200:
            image_N=int(N/200)

        self.theEnsemble.t=0

        imageCounter=image_N

        if self.imageOutputFolder:
            print("Saving image every ",image_N," steps")

        for i in range(N):
            if i>=(self.baseline_pre_periods/self.f/self.dt) and i<=((self.periods+self.baseline_pre_periods)/self.f/self.dt):
                self.theEnsemble.setShearRate(
                    self.amplitude * self.out_of_phase_signal(self.theEnsemble.t)* self.f * 2 * math.pi)



            else:
                self.theEnsemble.setShearRate(0)

            # Calculate forces, this registers individual forces in the force register

            self.theEnsemble.mechanical_simulation_step_calculate_forces()

            # report net particles forces and moments in the force register
            self.theEnsemble.record_total_particle_forces()


            self.plotter.record(self.theEnsemble,self.theEvaluator)



            # Do linear and rotational acceleration
            self.theEnsemble.mechanical_simulation_step_calculate_acceleration(cool_factor=cool_factor, dt=self.dt)
            # Do linear and rotation movememnt
            self.theEnsemble.mechanical_simulation_step_calculate_movement(dt=self.dt)
            # reset forces for next round
            self.theEnsemble.reset_force()

            if self.theEnsemble.doDrawing:
                self.theTkSimulation.update()

            if imageCounter>=image_N:

                self.save_canvas_image(i)
                imageCounter=0

            imageCounter=imageCounter+1


        print("overall", self.plotter.overall_stress_tensor[len(self.plotter.shear_stress) - 1])


        print("overall", self.plotter.overall_stress_tensor[0])

        G=self.write_output_information_to_file()



        if not self.external_output_Tk:
            if self.theTk:
                self.theTk.destroy()
                self.theTk = False
                self.outputCanvas = False

        return(G)


    def  save_canvas_image(self,index):
        if not self.imageOutputFolder or not self.theEnsemble.doDrawing or not self.theEnsemble.theCanvas:
            return

        filename=self.imageOutputFolder+"/"+self.imageBaseFileName
        if index < 1e6:
            filename=filename+"0"
        if index < 1e5:
            filename=filename+"0"
        if index < 1e4:
            filename=filename+"0"
        if index < 1e3:
            filename=filename+"0"
        if index < 1e2:
            filename = filename + "0"
        if index < 1e1:
            filename = filename + "0"

        file = filename + str(index)

        if self.imageFileType=="jpg":
            file=file+ ".jpg"
        else:
            file=file+".ps"

        if self.imageFileType=="jpg":
            ps=self.theEnsemble.theCanvas.postscript(colormode="color")
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            img.save(file)
        else:
            self.theEnsemble.theCanvas.postscript(file=file,colormode="color")









    def in_phase_signal(self,t):
        return math.sin((t * self.f - self.baseline_pre_periods) * math.pi * 2)

    def out_of_phase_signal(self,t):
        return math.cos((t * self.f - self.baseline_pre_periods) * math.pi * 2)


    # Returns a vector of four elements: the demodulated stress (in phase), the demodulated stress (90 degress),
    # G' and G''
    def demodulation(self,t,shear_stress):
        t = t
        in_phase = []
        out_of_phase = []
        sum_in_phase = 0
        sum_out_of_phase = 0
        stress_in_phase = 0
        stress_out_of_phase = 0
        stress_in_phase_linear_drift_corrected = 0
        stress_out_of_phase_linear_drift_corrected = 0

        # If we have more than one period available, do not use the first one for evaluation as there are transitory
        # phenomena at the beginning
        equilibration_periods = 0
        if self.periods >= 2:
            equilibration_periods = 1

        lastIndex = len(shear_stress) - 1

        lastStressForDelta = shear_stress[lastIndex]
        firstStressForDelta = shear_stress[0]

        firstTForDelta = t[0]
        lastTForDelta = t[lastIndex]

        if self.baseline_pre_periods > 0:
            sum_stress = 0
            sum_t = 0
            N = 0
            for i in range(len(t)):
                if t[i] < (self.baseline_pre_periods / self.f) and t[i] >= (2 * self.baseline_pre_periods / self.f / 3):
                    N = N + 1
                    sum_stress = sum_stress + shear_stress[i]
                    sum_t = sum_t + t[i]
            firstStressForDelta = sum_stress / N
            firstTForDelta = sum_t / N

        if self.baseline_post_periods > 0:
            sum_stress = 0
            sum_t = 0
            N = 0
            for i in range(len(t)):
                if t[i] > (self.baseline_pre_periods + self.periods) / self.f and t[i] <= \
                        (self.baseline_pre_periods + self.periods + self.baseline_post_periods / 3) / self.f:
                    N = N + 1
                    sum_stress = sum_stress + shear_stress[i]
                    sum_t = sum_t + t[i]
            lastStressForDelta = sum_stress / N
            lastTForDelta = sum_t / N

        linear_drift_coefficient = (lastStressForDelta - firstStressForDelta) / (firstTForDelta - lastTForDelta)



        for i in range(len(t)):
            ip = 0
            op = 0
            if t[i] >= ((self.baseline_pre_periods + equilibration_periods) / self.f) and t[i] <= (
                    (self.baseline_pre_periods + self.periods) / self.f):
                ip = self.in_phase_signal(t[i])
                op = self.out_of_phase_signal(t[i])

            in_phase.append(ip)
            out_of_phase.append(op)

            sum_in_phase = sum_in_phase + ip * ip
            sum_out_of_phase = sum_out_of_phase + op * op

            stress_linear_drift_corrected = shear_stress[i] - (
                    t[i] - self.baseline_pre_periods / self.f) * linear_drift_coefficient

            stress_in_phase = stress_in_phase + shear_stress[i] * ip
            stress_out_of_phase = stress_out_of_phase + shear_stress[i] * op

            stress_in_phase_linear_drift_corrected = stress_in_phase_linear_drift_corrected + stress_linear_drift_corrected * ip
            stress_out_of_phase_linear_drift_corrected = stress_out_of_phase_linear_drift_corrected + stress_linear_drift_corrected * op


        return [stress_in_phase_linear_drift_corrected / sum_in_phase,
                stress_out_of_phase_linear_drift_corrected / sum_out_of_phase,
                stress_in_phase_linear_drift_corrected / sum_in_phase / self.amplitude,
                stress_out_of_phase_linear_drift_corrected / sum_out_of_phase / self.amplitude]


    def evaluateStressAndG(self,useExternalForce=False):
        if not useExternalForce:
            return self.demodulation(self.plotter.t,self.plotter.shear_stress)
        else:
            return self.demodulation(self.plotter.t, self.plotter.force)



    def write_experiment_description_information_to_file(self):

        if not self.output_file:
            print("Not saving experiment description to file ( no data file configured )")
            return
        file=self.output_file

        print("Saving simulation description to output file")

        file.write("Oscillatory shear experiment\n\n")


        if hasattr(self.theEnsemble,"model"):
            file.write("Model parameters\n")
            file.write("Width of simulation area size_x =")
            file.write(str(self.theEnsemble.model.size_x))
            file.write("micrometers\n")
            file.write("Height of simulation area size_y =")
            file.write(str(self.theEnsemble.model.size_y))
            file.write("micrometers\n")
            file.write("Nominal packing fraction = ")
            file.write(str(self.theEnsemble.model.packing_fraction))
            file.write("\n")
            file.write("Young modulus spheres = ")
            file.write(str(self.theEnsemble.model.Young_modulus_spheres))
            file.write("Pa\n")
            file.write("Relative density spheres = ")
            file.write(str(self.theEnsemble.model.density))
            file.write("kg/m^3\n")
            file.write("Characteristic time constant = ")
            file.write(str(self.theEnsemble.model.time_constant))
            file.write("s\n")
            file.write("Characteristic spring constant = ")
            file.write(str(self.theEnsemble.model.k))
            file.write("mg/s^2\n")
            file.write("Characteristic viscosity  = ")
            file.write(str(self.theEnsemble.model.k*self.theEnsemble.model.time_constant))
            file.write("mg/s\n\n")

        file.write("Ensemble parameters\n")

        file.write("Particle mass m = ")
        file.write(str(self.theEnsemble.m))
        file.write("mg\n")

        file.write("Central spring constant k = ")
        file.write(str(self.theEnsemble.k))
        file.write("mg*s^(-2)\n")

        file.write("Central viscosity constant nu = ")
        file.write(str(self.theEnsemble.nu))
        file.write("mg*s^(-1)\n")

        file.write("Lateral spring constant k_t = ")
        file.write(str(self.theEnsemble.k_t))
        file.write("mg*s^(-2)\n")

        file.write("Lateral viscosity constant nu_t = ")
        file.write(str(self.theEnsemble.nu_t))
        file.write("mg*s^(-1)\n")

        file.write("Friction coefficient mu = ")
        file.write(str(self.theEnsemble.mu))
        file.write("\n")

        file.write("Sample width = ")
        file.write(str(self.theEnsemble.size_x))
        file.write("micrometers\n")

        file.write("Sample height = Gap height = ")
        file.write(str(self.theEnsemble.size_y))
        file.write("micrometers\n")

        file.write("Particle number = ")
        file.write(str(self.theEnsemble.N))
        file.write("\n")

        file.write("Particle information\n\t")
        file.write(str(self.theEnsemble.particle_info()))
        file.write("\n")


        if hasattr(self.theEnsemble,"k_corner_torque"):
            file.write("Angular torque spring constant, per m of depth: k_corner_torque = ")
            file.write(str(self.theEnsemble.k_corner_torque))
            file.write("mg/m*micrometers^2/s^-2\n")

        if hasattr(self.theEnsemble, "nu_corner_torque"):
            file.write("Angular torque viscosity constant, per m of depth: nu_corner_torque = ")
            file.write(str(self.theEnsemble.nu_corner_torque))
            file.write("mg/m*micrometers^2/s^-1\n")


        if hasattr(self.theEnsemble,"central_repulsion_coefficient"):
            file.write("Nonlinear enhancement for repulsion near sphere center = ")
            file.write(str(self.theEnsemble.central_repulsion_coefficient))
            file.write("[-], 0=no enhancement, 1=maximum enhancement; see CircleBasicElasticity.get_elastic_force\n")


        if hasattr(self.theEnsemble,"permanent_ratio_central"):
            file.write("Adjustment coefficient for central force in permanent links = ")
            file.write(str(self.theEnsemble.permanent_ratio_central))
            file.write("[-], 0=no central force, 1=as in free interfaces; >1 re-enforcement of permanent over transient links\n")
            file.write("\tk_permanent=")
            file.write(str(self.theEnsemble.k * self.theEnsemble.permanent_ratio_central))
            file.write("mg*s^(-2)\n")

        if hasattr(self.theEnsemble,"permanent_ratio_tangential"):
            file.write("Adjustment coefficient for tangential force in permanent links = ")
            file.write(str(self.theEnsemble.permanent_ratio_tangential))
            file.write("[-], 0=no tangential force, 1=as in free interfaces; >1 re-enforcement of permanent over transient links\n")
            file.write("\tk_t_permanent=")
            file.write(str(self.theEnsemble.k_t * self.theEnsemble.permanent_ratio_tangential))
            file.write("mg*s^(-2)\n")


        if hasattr(self.theEnsemble,"keep_viscosity_coefficients_constant") and hasattr(self.theEnsemble,"permanent_ratio_tangential") \
                and hasattr(self.theEnsemble,"permanent_ratio_central"):
            if self.theEnsemble.keep_viscosity_coefficients_constant:
                file.write("Viscosity adjustment for permanent links:\n"
                           "\tNo adjustment: Impose constant viscosity regardless of the permanent link adjustment ")
                file.write("\n\tnu_permanent="+str(self.theEnsemble.nu))
                file.write("\n\tnu_t_permanent=" + str(self.theEnsemble.nu_t))
            else:
                file.write("Viscosity adjustment for permanent links:\n"
                           "\tAdjustment: Adjust viscosity (central and tangential) by same factor "+
                            "as the respective spring constant (k and k_t)")
                file.write("\n\tnu_permanent=" + str(self.theEnsemble.nu*self.theEnsemble.permanent_ratio_central))
                file.write("\n\tnu_t_permanent=" + str(self.theEnsemble.nu_t*self.theEnsemble.permanent_ratio_tangential))

        if not hasattr(self.theEnsemble,"avoid_height_spanning_particles"):
            file.write("\navoid_height_spanning_particles: Full height spanning particles allowed")
        else:
            if not self.theEnsemble.avoid_height_spanning_particles:
                file.write("\navoid_height_spanning_particles: Full height spanning particles allowed")
            else:
                file.write("\navoid_height_spanning_particles: Ensembles with full height spanning particles discarded")

        if hasattr(self.theEnsemble, "removed_fraction"):
            file.write("\nActual fraction of randomly removed non-essential permanent bonds = ")
            file.write(str(self.theEnsemble.removed_fraction))
            file.write(
                "[-]\n")

        if hasattr(self.theEnsemble, "edge_fuzziness"):
            file.write("\nEdge fuzziness for creating interlocking = ")
            file.write(str(self.theEnsemble.edge_fuzziness))
            file.write(
                "[-]\n")









        file.write("\n\nRheology experiment information\n")
        file.write("Simulated time = ")
        file.write(str(self.periods / self.f))
        file.write("s\n")

        file.write("Time step = ")
        file.write(str(self.dt))
        file.write("s\n")

        file.write("Frequency = ")
        file.write(str(self.f))
        file.write("Hz\n")

        file.write("Strain amplitude = ")
        file.write(str(self.amplitude*100))
        file.write("%\n")

        file.write("Damping factor = ")
        file.write(str(self.final_cool_factor))
        file.write(" [1 = no damping]\n")

        file.write("Pre-measurement periods = ")
        file.write(str(self.baseline_pre_periods))
        file.write(" [-]\n")

        file.write("Oscillatory shear periods = ")
        file.write(str(self.periods))
        file.write(" [-]\n")

        file.write("Post-measurement periods = ")
        file.write(str(self.baseline_pre_periods))
        file.write(" [-]\n")

        if hasattr(self.theEnsemble,"shear_rate_to_rotation_rate_coefficient"):
            file.write("Sllod equations: Anticipated adjustment of rotation for shear, with coefficient")
            file.write(str(self.theEnsemble.shear_rate_to_rotation_rate_coefficient))
            file.write(" [-]\n")

    def write_output_information_to_file(self):

        G=self.evaluateStressAndG(useExternalForce=False)
        G_external=self.evaluateStressAndG(useExternalForce=True)

        print("G'=")
        print(str(G[2]))
        print("Pa\n")
        print("G''=")
        print(str(G[3]))
        print("Pa\n")
        print("G'(by surface force)=")
        print(str(G_external[2]))
        print("Pa\n")
        print("G''(by surface force)=")
        print(str(G_external[3]))
        print("Pa\n")

        if not self.output_file:
            print("Not saving output to file (no data file configured)")
            return [G_external[2],G_external[3]]

        print("Saving simulation data to output file")
        file=self.output_file
        file.write("\n\nOutput data\nSummary data\n")
        file.write("In phase stress = ")
        file.write(str(G[0]))
        file.write("Pa\n")
        file.write("Out of phase stress = ")
        file.write(str(G[1]))
        file.write("Pa\n")
        file.write("Stress = ")
        file.write(str(math.sqrt(G[0]*G[0]+G[1]*G[1])))
        file.write("Pa\n")
        file.write("G'=")
        file.write(str(G[2]))
        file.write("Pa\n")
        file.write("G''=")
        file.write(str(G[3]))
        file.write("Pa\n")
        file.write("G'(by surface force)=")
        file.write(str(G_external[2]))
        file.write("Pa\n")
        file.write("G''(by surface force)=")
        file.write(str(G_external[3]))
        file.write("Pa\n")




        file.write("\n\nDetailed stress tensor data\n")

        if(not self.saveStressTensorData):

            print("Saving summary data only to file")

            file.write("\tNot saving detailed stress tensor data. If you wish to save this data, pass \n"+
                       "\t  saveStressTensorData=True")

        else:
            print("Saving stress tensor data to file")
            file.write("index\tt\tstrain\tstrain_rate\tstress_measured_at_surface\tshear_stress_internal_stress-tensor")
            file.write("\tstress_tensor_Love_Weber_00")
            file.write("\tstress_tensor_Love_Weber_01")
            file.write("\tstress_tensor_Love_Weber_10")
            file.write("\tstress_tensor_Love_Weber_11")
            file.write("\tstress_tensor_peculiar_acceleration_otsuki_00")
            file.write("\tstress_tensor_peculiar_acceleration_otsuki_01")
            file.write("\tstress_tensor_peculiar_acceleration_otsuki_10")
            file.write("\tstress_tensor_peculiar_acceleration_otsuki_11")
            file.write("\tstress_tensor_from_external_forces_00")
            file.write("\tstress_tensor_from_external_forces_01")
            file.write("\tstress_tensor_from_external_forces_10")
            file.write("\tstress_tensor_from_external_forces_11")
            file.write("\tstress_tensor_linear_acceleration_00")
            file.write("\tstress_tensor_linear_acceleration_01")
            file.write("\tstress_tensor_linear_acceleration_10")
            file.write("\tstress_tensor_linear_acceleration_11")
            file.write("\tstress_tensor_unbalanced_linear_forces_00")
            file.write("\tstress_tensor_unbalanced_linear_forces_01")
            file.write("\tstress_tensor_unbalanced_linear_forces_10")
            file.write("\tstress_tensor_unbalanced_linear_forces_11")
            file.write("\tstress_tensor_tangential_torque_00")
            file.write("\tstress_tensor_tangential_torque_01")
            file.write("\tstress_tensor_tangential_torque_10")
            file.write("\tstress_tensor_tangential_torque_11")
            file.write("\tstress_tensor_internal_tangential_torque_00")
            file.write("\tstress_tensor_internal_tangential_torque_01")
            file.write("\tstress_tensor_internal_tangential_torque_10")
            file.write("\tstress_tensor_internal_tangential_torque_11")
            file.write("\tstress_tensor_centrifugal_00")
            file.write("\tstress_tensor_centrifugal_01")
            file.write("\tstress_tensor_centrifugal_10")
            file.write("\tstress_tensor_centrifugal_11")
            file.write("\tstress_tensor_overall_00")
            file.write("\tstress_tensor_overall_01")
            file.write("\tstress_tensor_overall_10")
            file.write("\tstress_tensor_overall_11")

            p = self.plotter

            for ip in range(len(p.t)):
                file.write("\n" + str(ip))
                file.write("\t")
                file.write(str(p.t[ip]))
                file.write("\t")
                file.write(str(p.strain[ip]))
                file.write("\t")
                file.write(str(p.strain_rate[ip]))
                file.write("\t")
                file.write(str(p.force[ip]))
                file.write("\t")
                file.write(str(p.shear_stress[ip]))
                for i in range(2):
                    for j in range(2):
                        file.write("\t")
                        file.write(str(p.stress_tensor_LW[ip][i][j]))
                for i in range(2):
                    for j in range(2):
                        file.write("\t")
                        file.write(str(p.stress_tensor_linear_acceleration_otsuki[ip][i][j]))
                for i in range(2):
                    for j in range(2):
                        file.write("\t")
                        file.write(str(p.stress_tensor_with_external_forces[ip][i][j]))
                for i in range(2):
                    for j in range(2):
                        file.write("\t")
                        file.write(str(p.stress_tensor_linear_acceleration[ip][i][j]))
                for i in range(2):
                    for j in range(2):
                        file.write("\t")
                        file.write(str(p.stress_tensor_unbalanced_forces[ip][i][j]))
                for i in range(2):
                    for j in range(2):
                        file.write("\t")
                        file.write(str(p.stress_tensor_unbalanced_torque[ip][i][j]))
                for i in range(2):
                    for j in range(2):
                        file.write("\t")
                        file.write(str(p.stress_tensor_internal_torque[ip][i][j]))
                for i in range(2):
                    for j in range(2):
                        file.write("\t")
                        file.write(str(p.stress_tensor_spin_kinetic_energy[ip][i][j]))
                for i in range(2):
                    for j in range(2):
                        file.write("\t")
                        file.write(str(p.overall_stress_tensor[ip][i][j]))

        return [G_external[2],G_external[3]]










