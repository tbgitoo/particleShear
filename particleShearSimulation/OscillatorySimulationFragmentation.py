from particleShearObjects import particle_shear_model_parameters
from .OscillatoryShearExperiment import OscillatoryShearExperiment
from .OscillatorySimulation import OscillatorySimulation
import math
from tkinter import *
from pathlib import Path



class OscillatorySimulationFragmentation(OscillatorySimulation):

    def __init__(self,root_folder,do_permanent_links=True,cut_lines=5,N=150,packing_fraction=2,amplitude=0.5,
                 Young_modulus_spheres=1000,mu=0.1,
                 relative_y_scale_force=5e-4,relative_frequency=0.05,doDrawing=True,saveData=False):
        self.packing_fraction = packing_fraction
        self.N = N

        super(OscillatorySimulationFragmentation,self).__init__(
            root_folder,amplitude=amplitude,
            relative_y_scale_force=relative_y_scale_force,relative_frequency=relative_frequency,doDrawing=doDrawing,
            saveData=saveData)
        self.do_permanent_links=do_permanent_links
        self.cut_lines=cut_lines



        self.Young_modulus_spheres=Young_modulus_spheres
        self.mu=mu
        self.theEnsemble=False

        self.model=False

        self.packing_fraction=packing_fraction

        self.function_call="OscillatorySimulationFragmentation(root_folder="+str(root_folder)+",do_permanent_links="+\
            str(do_permanent_links)+",cut_lines="+str(cut_lines)+",N="+str(N)+\
            "packing_fraction="+str(packing_fraction)+",amplitude="+str(amplitude)+\
            ",Young_modulus_spheres="+str(Young_modulus_spheres)+",mu="+str(mu)+\
            ",relative_y_scale_force="+str(relative_y_scale_force)+",relative_frequency="+str(relative_frequency)+\
            ",doDrawing=" + str(doDrawing) + ")"

    def adjustment_factor_for_bounded_preequilibration_steps(self):
        if self.mu > 0 and self.mu<=1:
            return int(2 - math.log10(self.mu))
        return 1

    # Here the ensemble needs to be initiated, but this needs to be done in the subclasses
    def initEnsemble(self):

        if self.doDrawing and not self.theTkSimulation:
            self.theTkSimulation=Tk()



    def file_path(self):
        if not self.root_folder:
            return False
        fname = "dermal_filler"

        if self.do_permanent_links:
            if not (self.cut_lines > 0):
                fname = fname + "_bulk"
        else:
            fname = fname + "_uncrosslinked"

        fname = fname + str(self.mu) + "_f_" + str(round(self.f*10000)/10000) + "_strain_" +\
                str(round(self.amplitude*100000)/100000) + "_nr_"

        fnum = 1

        while Path(self.root_folder + "/" + fname + str(fnum) + ".txt").is_file():
            fnum = fnum + 1

        return self.root_folder + "/" + fname + str(fnum) + ".txt"

    def write_information_on_simulation_to_file(self,theFile):
        if not self.saveData:
            return


        if self.do_permanent_links:
            if self.cut_lines > 0:
                theFile.write("Dermal filler Ensemble: \n")
                theFile.write("\tCutting lines used to generate the particles" + str(self.cut_lines) + "\n")
            else:
                theFile.write("Dermal filler control ensemble: no cut lines \n")
        else:
            theFile.write("Dermal filler control ensemble: No permanent links\n")

        theFile.write("\tN=" + str(self.N) + " spheres, nominal packing density = " + str(self.packing_fraction) + "\n")

        theFile.write("\tYoung modulus of the individual spheres = " + str(self.Young_modulus_spheres) + " Pa \n")

        theFile.write("\tFriction coefficient = " + str(self.mu) + "\n\n")

        theFile.write("\n\nFunction call : \n" + self.function_call+"\n\n")



