from particleShearObjects import particle_shear_model_parameters
from .OscillatoryShearExperiment import OscillatoryShearExperiment
import math
from tkinter import *
from pathlib import Path
import os



class OscillatorySimulation():

    def __init__(self,root_folder,amplitude=0.5,relative_y_scale_force=5e-4,relative_frequency=0.05,doDrawing=True,
                 saveData=False):
        self.amplitude=amplitude
        self.doDrawing=doDrawing
        self.relative_y_scale_force=relative_y_scale_force
        self.relative_frequency=relative_frequency
        self.theTkSimulation=False
        self.f=-1 # Frequency, -1 before setting
        self.root_folder=root_folder
        self.saveData=saveData

        self.baseline_pre_periods = 0  # Acquisition of stress data with 0
        # excitation amplitude to have a baseline before oscillatory shear
        self.baseline_post_periods = 0  # Acquisition of stress data with 0
        # excitation amplitude to have a baseline before oscillatory shear

        self.imageOutputFolder = False

        self.imageBaseFileName = False

        self.saveOutputImages = False

        self.imageFileType="jpg"

        self.saveStressTensorData=True
        """Flag indicating whether we should save the detailed stress tensor data in the ASCII output files
        
        Relevant only if saveData==True"""

        self.function_call = "OscillatorySimulation(root_folder="+str(root_folder)+",amplitude="+str(amplitude)+\
            ",relative_y_scale_force="+str(relative_y_scale_force)+",relative_frequency="+str(relative_frequency)+")"

        self.theExperiment = False # To hold the shear experiment done

    # Here the ensemble needs to be initiated, but this needs to be done in the subclasses
    def initEnsemble(self):
        if not self.theTkSimulation and self.doDrawing:
            self.theTkSimulation=Tk()


    def file_path(self):
        if not self.root_folder:
            return False
        fname = "oscillatory_simulation_"

        fnum=1

        while Path(self.root_folder + "/" + fname + str(fnum) + ".txt").is_file():
            fnum = fnum + 1

        return self.root_folder + "/" + fname + str(fnum) + ".txt"

    def image_folder_path(self,fileName):
        folderName=fileName+"_images_folder"
        self.createFolder(folderName)
        return folderName

    def createFolder(self,directory):
        print("Creating image folder",directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("done")








    def write_information_on_simulation_to_file(self,theFile):
        if not self.saveData:
            return
        theFile.write("Basic oscillatory shear simulation")

    # To be implemented by subclasses, in some cases longer pre-equilibration is necessary (low friction coefficient, low amplitudes)
    # but this depends on the exact simulation to be run
    def adjustment_factor_for_bounded_preequilibration_steps(self):
        return 1


    def runSimulation(self,cool_factor=1,periods=2,plotStress=True):



        self.initEnsemble()




        model = self.theEnsemble.model

        y_scale_force = self.relative_y_scale_force / model.k / self.amplitude

        final_dt = self.theEnsemble.dt

        #if self.amplitude<0.01:

        #    final_dt=final_dt/(1-2*(math.log10(self.amplitude)+2))
        #    print("Small amplitude: Adjusted to dt=", final_dt)




        print("Setting relative frequency: "+str(self.relative_frequency))
        self.f = self.relative_frequency / model.time_constant

        fileName=self.file_path()

        if self.saveOutputImages:
            self.imageOutputFolder = self.image_folder_path(fileName)
            self.imageBaseFileName = "image"

        theFile=False
        if self.saveData:
            theFile = open(fileName, "w")



        self.write_information_on_simulation_to_file(theFile)

        print("Creating oscillatory shear experiment, dt = ",final_dt," max dt = ",self.theEnsemble.dt_max)
        theExperiment=OscillatoryShearExperiment(self.theEnsemble,final_dt,
                                         self.f,self.amplitude,theFile,force_scale=y_scale_force,
                                         TkSimulation=self.theEnsemble.theTkSimulation,dt_max=self.theEnsemble.dt_max,
                                         imageOutputFolder=self.imageOutputFolder,
                                         imageBaseFileName=self.imageBaseFileName,
                                         imageFileType=self.imageFileType,
                                         plotStress=plotStress,
                                         saveStressTensorData=self.saveStressTensorData)

        theExperiment.periods=periods
        theExperiment.baseline_pre_periods=self.baseline_pre_periods
        theExperiment.baseline_post_periods=self.baseline_post_periods






        theExperiment.do_preequilibration_with_fixed_boundaries=True

        N_pre_equilibration_fixed_boundaries=25*self.adjustment_factor_for_bounded_preequilibration_steps()


        N_per_period = 1/self.f/final_dt

        cf_per_dt = math.pow(cool_factor,1/N_per_period)

        # The idea here is that we have always the same attenuation per period
        print("cool factor per dt=",cf_per_dt)

        G=theExperiment.oscillatory_shear_experiment(
            cool_factor=cf_per_dt,N_pre_equilibration_fixed_boundaries=N_pre_equilibration_fixed_boundaries)


        if self.saveData:
            theFile.close()

        if  self.theEnsemble.theTkSimulation:
            self.theEnsemble.theTkSimulation.destroy()

        self.theTkSimulation=False

        self.theExperiment=theExperiment

        return(G)






