from particleShearLinkableObjects import EnsembleCompactParticlesFromModelParameters
from particleShearObjects import particle_shear_model_parameters
from .OscillatoryShearExperiment import OscillatoryShearExperiment
import math
from tkinter import *

from .OscillatorySimulationFragmentation import OscillatorySimulationFragmentation



class Simulation_dermal_filler_rheology(OscillatorySimulationFragmentation):

    def __init__(self,root_folder,do_permanent_links=True,cut_lines=5,N=150,packing_fraction=2,
                 bimodal_factor=1.4,
                 amplitude=0.5,
                 Young_modulus_spheres=1000,
                 density=50,
                 mu=0.1,relative_viscosity=0.01,
                 relative_y_scale_force=5e-4,relative_frequency=0.05, relative_transversal_link_strength=1,
                 central_repulsion_coefficient=1,
                 avoid_horizontal_angle_degree=0,avoid_height_spanning_particles=False,
                 doCutByTriangulation=True,doDrawing=True,saveData=False):

        self.avoid_horizontal_angle_degree=avoid_horizontal_angle_degree
        self.avoid_height_spanning_particles=avoid_height_spanning_particles
        self.doCutByTriangulation=doCutByTriangulation
        self.bimodal_factor=bimodal_factor
        self.central_repulsion_coefficient=central_repulsion_coefficient
        self.density=density

        super(Simulation_dermal_filler_rheology,self).__init__(
            root_folder,do_permanent_links=do_permanent_links,cut_lines=cut_lines,
            N=N,packing_fraction=packing_fraction,amplitude=amplitude,
                 Young_modulus_spheres=Young_modulus_spheres,mu=mu,
                 relative_y_scale_force=relative_y_scale_force,relative_frequency=relative_frequency,
                 doDrawing=doDrawing,saveData=saveData)

        self.relative_viscosity=relative_viscosity
        self.relative_transversal_link_strength=relative_transversal_link_strength

        self.function_call = "Simulation_dermal_filler_rheology(root_folder=" + str(root_folder) + ",do_permanent_links=" + \
                             str(do_permanent_links) + ",cut_lines=" + str(cut_lines) + ",N=" + str(N) + \
                             ",packing_fraction=" + str(packing_fraction) + \
                             ",bimodal_factor="+str(bimodal_factor)+\
                             ",amplitude=" + str(amplitude) + \
                             ",Young_modulus_spheres=" + str(Young_modulus_spheres) + \
                             ",density=" + str(density) + ",mu=" + str(mu) +  \
                             ",relative_viscosity="+str(relative_viscosity)+\
                             ",relative_y_scale_force=" + str(relative_y_scale_force) + ",relative_frequency=" + \
                             str(relative_frequency) +\
                             ",relative_transversal_link_strength="+str(relative_transversal_link_strength)+ \
                             ",central_repulsion_coefficient=" + str(central_repulsion_coefficient) + \
                             ",avoid_horizontal_angle_degree="+str(avoid_horizontal_angle_degree)+\
                             ",avoid_height_spanning_particles=" + str(self.avoid_height_spanning_particles) + \
                             ",doCutByTriangulation="+str(self.doCutByTriangulation) + \
                             ",doDrawing=" + str(doDrawing) + ")"




    def adjustment_factor_for_bounded_preequilibration_steps(self):
        f=1
        if self.mu<=0.1:
            f=f*1.5
        if self.mu<=0.01:
            f=f*2
        if self.mu<=0.001:
            f=f*2
        if self.amplitude<=0.01:
            f=f*(1-(math.log10(self.amplitude)+2))
        if self.amplitude<=0.005:
            f=f*2
        if self.relative_viscosity<=0.1:
            f=f*2
        print("Adjustment factor of pre-equilibration time for low amplitude and friction:",f)
        return int(f)


    def initEnsemble(self,do_debug=False):
        super(Simulation_dermal_filler_rheology,self).initEnsemble()

        self.theEnsemble = EnsembleCompactParticlesFromModelParameters(
            cut_lines=self.cut_lines,N=self.N,packing_fraction=self.packing_fraction,
            Young_modulus_spheres=self.Young_modulus_spheres,
            density=self.density,bimodal_factor=self.bimodal_factor,
            do_permanent_links=self.do_permanent_links,mu=self.mu,theTk=self.theTkSimulation,do_pre_equilibration=True,
            relative_viscosity=self.relative_viscosity,central_repulsion_coefficient=self.central_repulsion_coefficient,
            anticipated_amplitude=self.amplitude,relative_transversal_link_strength=self.relative_transversal_link_strength,
            avoid_horizontal_angle_degree=self.avoid_horizontal_angle_degree,
            avoid_height_spanning_particles=self.avoid_height_spanning_particles,
            doCutByTriangulation=self.doCutByTriangulation,doDrawing=self.doDrawing,
            do_debug=do_debug)

        self.dt=self.theEnsemble.dt
        self.dt_max = self.theEnsemble.dt_max










