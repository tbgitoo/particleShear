from particleShearLinkableObjects import EnsembleCompactParticlesAdjustableInterfaceStrengthFromModelParameters
from particleShearObjects import particle_shear_model_parameters
from .OscillatoryShearExperiment import OscillatoryShearExperiment
import math
from tkinter import *

from .Simulation_dermal_filler_rheology import Simulation_dermal_filler_rheology



class Simulation_interlocking_rheology(Simulation_dermal_filler_rheology):

    def __init__(self,root_folder,do_permanent_links=True,cut_lines=5,N=150,packing_fraction=2,
                 bimodal_factor=1.4,
                 amplitude=0.5,
                 Young_modulus_spheres=1000,
                 density=50,
                 mu=0.1,relative_viscosity=0.01,
                 relative_y_scale_force=5e-4,relative_frequency=0.05, relative_transversal_link_strength=1,
                 avoid_horizontal_angle_degree=15,avoid_height_spanning_particles=False,
                 interface_reenforcement_central=1,interface_reenforcement_tangential=1,
                 central_repulsion_coefficient=1,
                 keep_viscosity_coefficients_constant=True,cut_top_bottom=True,
                 doCutByTriangulation=True,remove_link_fraction=0,edge_fuzziness=0,doDrawing=True,saveData=False):



        self.avoid_horizontal_angle_degree=avoid_horizontal_angle_degree
        self.interface_reenforcement_central=interface_reenforcement_central
        self.interface_reenforcement_tangential=interface_reenforcement_tangential
        self.keep_viscosity_coefficients_constant=keep_viscosity_coefficients_constant
        self.cut_top_bottom=cut_top_bottom
        self.remove_link_fraction=remove_link_fraction
        self.edge_fuzziness=edge_fuzziness


        super(Simulation_interlocking_rheology,self).__init__(
            root_folder,do_permanent_links=do_permanent_links,cut_lines=cut_lines,
            N=N,packing_fraction=packing_fraction,
            bimodal_factor=bimodal_factor,
            amplitude=amplitude,
            Young_modulus_spheres=Young_modulus_spheres,
            density=density,
            mu=mu,relative_viscosity=relative_viscosity,
            relative_y_scale_force=relative_y_scale_force,relative_frequency=relative_frequency,
            relative_transversal_link_strength=relative_transversal_link_strength,
            central_repulsion_coefficient=central_repulsion_coefficient,
            avoid_horizontal_angle_degree=avoid_horizontal_angle_degree,
            avoid_height_spanning_particles=avoid_height_spanning_particles,
            doCutByTriangulation=doCutByTriangulation,
            doDrawing=doDrawing,saveData=saveData)



        self.function_call = "Simulation_interlocking_rheology(root_folder=" + str(root_folder) + ",do_permanent_links=" + \
                             str(do_permanent_links) + ",cut_lines=" + str(cut_lines) + ",N=" + str(N) + \
                             ",packing_fraction=" + str(packing_fraction) + \
                             ",bimodal_factor=" + str(bimodal_factor) + \
                             ",amplitude=" + str(amplitude) + \
                             ",Young_modulus_spheres=" + str(Young_modulus_spheres)  + \
                             ",density=" + str(density) + ",mu=" + str(mu) +  \
                             ",relative_viscosity="+str(relative_viscosity)+\
                             ",relative_y_scale_force=" + str(relative_y_scale_force) + ",relative_frequency=" + \
                             str(relative_frequency) +\
                             ",relative_transversal_link_strength="+str(relative_transversal_link_strength)+ \
                             ",central_repulsion_coefficient=" + str(central_repulsion_coefficient) + \
                             ",avoid_horizontal_angle_degree="+str(avoid_horizontal_angle_degree)+ \
                             ",avoid_height_spanning_particles=" + str(self.avoid_height_spanning_particles) + \
                             ",interface_reenforcement_central="+str(interface_reenforcement_central)+\
                             ",interface_reenforcement_tangential="+str(interface_reenforcement_tangential)+\
                             ",keep_viscosity_coefficients_constant="+str(keep_viscosity_coefficients_constant)+ \
                             ",cut_top_bottom=" + str(cut_top_bottom)+ \
                             ",doCutByTriangulation=" + str(self.doCutByTriangulation) + \
                             ",remove_link_fraction=" + str(self.remove_link_fraction) + \
                             ",edge_fuzziness=" + str(self.edge_fuzziness) + \
                             ",doDrawing=" + str(doDrawing)+")"







    def initEnsemble(self,do_debug=False):
        super(Simulation_dermal_filler_rheology,self).initEnsemble()

        print("Simulation_interlocking_rheology: initiating ensemble")



        self.theEnsemble = EnsembleCompactParticlesAdjustableInterfaceStrengthFromModelParameters(
            cut_lines=self.cut_lines,N=self.N,packing_fraction=self.packing_fraction,
            Young_modulus_spheres=self.Young_modulus_spheres,density=self.density,
            bimodal_factor=self.bimodal_factor,
            do_permanent_links=self.do_permanent_links,mu=self.mu,theTk=self.theTkSimulation,do_pre_equilibration=True,
            relative_viscosity=self.relative_viscosity,central_repulsion_coefficient=self.central_repulsion_coefficient,
            anticipated_amplitude=self.amplitude,relative_transversal_link_strength=self.relative_transversal_link_strength,
            avoid_horizontal_angle_degree=self.avoid_horizontal_angle_degree,
            avoid_height_spanning_particles=self.avoid_height_spanning_particles,
            interface_reenforcement_central=self.interface_reenforcement_central,
            interface_reenforcement_tangential=self.interface_reenforcement_tangential,
            keep_viscosity_coefficients_constant=self.keep_viscosity_coefficients_constant,
            cut_top_bottom=self.cut_top_bottom,doCutByTriangulation=self.doCutByTriangulation,
            remove_link_fraction=self.remove_link_fraction,
            edge_fuzziness=self.edge_fuzziness,
            doDrawing=self.doDrawing,
            do_debug=do_debug
            )

        self.dt=self.theEnsemble.dt
        self.dt_max = self.theEnsemble.dt_max










