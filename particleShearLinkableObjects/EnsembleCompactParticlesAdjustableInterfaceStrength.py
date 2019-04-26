from tkinter import *
import random
import math
from .SphereLinkableAdjustableInterfaceStrength import SphereLinkableAdjustableInterfaceStrength
from .EnsembleCompactParticles import EnsembleCompactParticles
from .CanvasPointsLinkable import CanvasPointsLinkable
from particleShearObjects import r_estimate
from particleShearObjects import adjust_m
from particleShearObjects import particle_shear_model_parameters


class EnsembleCompactParticlesAdjustableInterfaceStrength(EnsembleCompactParticles):

    def __init__(self, size_x, size_y, N, packing_fraction=0.8, theCanvas=False, doDrawing=False,
                 k=1, nu=0.01,m=1,
                 bimodal_factor=1.4,
                 k_t=1,nu_t=0.01,mu=0.1,dt=1,dt_max=10,theTkSimulation=False,avoid_horizontal_angle_degree=0,
                 permanent_ratio_central=1, permanent_ratio_tangential=1, keep_viscosity_coefficients_constant=True):


        # The idea here is that we can specifically increase the central or tangential forces for the crosslinked particles
        # as compared to the normal frictional contact

        self.permanent_ratio_central=permanent_ratio_central
        self.permanent_ratio_tangential=permanent_ratio_tangential
        self.keep_viscosity_coefficients_constant=keep_viscosity_coefficients_constant

        self.cut_top_bottom=False





        super(EnsembleCompactParticlesAdjustableInterfaceStrength, self).__init__(
            size_x, size_y,N=0,packing_fraction=packing_fraction, theCanvas=theCanvas, doDrawing=False,
                 k=k, nu=nu,m=m,bimodal_factor=bimodal_factor,
                 k_t=k_t,nu_t=nu_t,mu=mu,dt=dt,
                 dt_max=dt_max,theTkSimulation=theTkSimulation,avoid_horizontal_angle_degree=avoid_horizontal_angle_degree)



        self.N = N

        self.sphereList = []
        self.doDrawing = doDrawing

        r=self.size_y/2

        if N > 0:
            r = r_estimate(self.size_x, self.size_y, packing_fraction, N,
                           bimodal_upper=self.bimodal_upper,
                           bimodal_lower=self.bimodal_lower)

        self.r_max = 0

        for i in range(N):
            r_sphere = self.random_radius_bimodal(r)
            if r_sphere > self.r_max:
                self.r_max = r_sphere
            self.sphereList.append(SphereLinkableAdjustableInterfaceStrength("grey",
                                                  random.randrange(0, size_x),
                                                  random.randrange(0, size_y), r_sphere * 2,
                                                  adjust_m(m, r_sphere, r),
                                                  i, theCanvas, False, self, self.size_x, self.size_y,
                                                  permanent_ratio_central=self.permanent_ratio_central,
                                                  permanent_ratio_tangential=self.permanent_ratio_tangential,
                                                  keep_viscosity_coefficients_constant=keep_viscosity_coefficients_constant
                                                  ))
        self.setShearInSpheres()
        self.setShearRateInSpheres()

        self.set_graphical_output_configuration(
            self.graphical_output_configuration)  # To propagate it also to the spheres

        self.initiateGraphics()




    def particle_info(self):
        return "Frictional spheres under Lees-Edwards boundary conditions, organized in fixed particles, adjustment of" \
               "strength between permament and temporary interfaces\n" \
               "\tSpheres with, bimodal distribution, equal probability, \n\tr1="+\
               str(self.r_max*0.8/1.2)+"r2="+str(self.r_max)+"\n\tidentical mass="+str(self.sphereList[0].m)+"mg"







def EnsembleCompactParticlesAdjustableInterfaceStrengthFromModelParameters(size_x=500,size_y=500,N=100,packing_fraction=1,mu=1,
                                                Young_modulus_spheres=10000,density=50,bimodal_factor=1.4,
                                                cut_lines=5,do_permanent_links=True,theTk=False,do_pre_equilibration=True,
                                                relative_viscosity=0.01,central_repulsion_coefficient=0,anticipated_amplitude=0.1,
                                                relative_transversal_link_strength=1,avoid_horizontal_angle_degree=0,
                                                avoid_height_spanning_particles=False,
                                                interface_reenforcement_central=1,interface_reenforcement_tangential=1,
                                                keep_viscosity_coefficients_constant=True,cut_top_bottom=True,
                                                doCutByTriangulation=True,remove_link_fraction=0,edge_fuzziness=0,doDrawing=True,
                                                do_debug=False):



    

    # First, some logics: with permanent links but insufficient tools to cut them, height spanning particles cannot be avoided

    if avoid_height_spanning_particles and ((doCutByTriangulation and cut_lines <= 1) or ((not doCutByTriangulation)
                                                                                          and cut_Lines <= 0)):
        avoid_height_spanning_particles = False
        print("Cannot avoid height spanning particles for bulk ensembles")

    theCanvas = False

    if doDrawing and not theTk:
        theTk = Tk()

    if doDrawing:
        theCanvas = Canvas(theTk, width=size_x, height=size_y)

        theCanvas.pack()

        theTk.title("Interface: tangential=" + str(interface_reenforcement_tangential) + " central=" + \
                    str(interface_reenforcement_central) + " A=" + str(anticipated_amplitude) + " mu=" + str(mu))




    model = particle_shear_model_parameters(size_x=size_x, size_y=size_y, N=N,
                                            packing_fraction=packing_fraction,
                                            Young_modulus_spheres=Young_modulus_spheres,density=density,
                                            bimodal_factor=1)

    print("Characteristic time constant [s] ",model.time_constant)

    final_dt = 0.1 * model.time_constant/bimodal_factor

    print("dt from model before adapation",final_dt)
    if mu<=1 or relative_transversal_link_strength<1:
        final_dt=final_dt/2
    if  anticipated_amplitude<=0.05:
        final_dt=final_dt/2
    if mu <=0.1 or relative_transversal_link_strength<0.1:
        final_dt = final_dt / 2
    if anticipated_amplitude<=0.005:
        final_dt = final_dt / 2
    if anticipated_amplitude>=0.5:
        final_dt = final_dt / 2
    dt_max = 0.25 * model.time_constant/bimodal_factor



    # Special delicate situations with little viscous components, either central or tangential, and thus
    # tendency for the ensemble to oscillate
    if relative_viscosity<=0.1 and mu<0.1 or relative_transversal_link_strength<0.1 or relative_transversal_link_strength>5:

        dt_max = 0.125 * model.time_constant/bimodal_factor
        print("Relative viscosity below 0.1, adapting dt_max to ",dt_max)
    if relative_viscosity<0.01 and mu<0.01 or relative_transversal_link_strength<0.01:

        dt_max = 0.04 * model.time_constant/bimodal_factor
        print("Relative viscosity below 0.01, adapting dt_max to", dt_max)

    if final_dt > dt_max:
        final_dt=dt_max


    print("dt from model after adaptaion for friction (mu=", mu,") and amplitude (A=",anticipated_amplitude,"):",final_dt)

    if relative_viscosity>1:
        dt_max=dt_max/relative_viscosity

    # Here, the situation is expressed in terms of interface re-enforcement. So since the
    # permanent_ratio_central and permanent_ratio_tangential
    # parameters will be smaller than 1, we need to artificially re-enforce the corresponding k, nu, k_t and nu_t parameters
    # Then, only the values for the permanent links will be multiplied with the smaller constants, and
    # so they reach their intended base level in the permanent links. In the non-permanent (interfacial links),
    # they will remain higher

    nu_for_ensemble=relative_viscosity*model.k * model.time_constant
    # Switch to decide whether viscosity constant should remain globally constant or vary the same way as the elastic ones
    if not keep_viscosity_coefficients_constant:
        nu_for_ensemble=nu_for_ensemble*interface_reenforcement_central

    nu_t_for_ensemble = relative_viscosity*model.k * model.time_constant*relative_transversal_link_strength
    # Switch to decide whether viscosity constant should remain globally constant or vary the same way as the elastic ones
    if not keep_viscosity_coefficients_constant:
        nu_t_for_ensemble = relative_viscosity * model.k * model.time_constant * \
                            relative_transversal_link_strength * interface_reenforcement_tangential



    theEnsemble = EnsembleCompactParticlesAdjustableInterfaceStrength(size_x, size_y, N, packing_fraction,
                                           theCanvas, doDrawing=doDrawing, k=model.k*interface_reenforcement_central,
                                           nu= nu_for_ensemble,
                                           m=model.m,
                                           bimodal_factor=bimodal_factor,
                                           k_t=model.k*relative_transversal_link_strength*interface_reenforcement_tangential,
                                           nu_t=nu_t_for_ensemble ,
                                           mu=mu,
                                           dt=final_dt, dt_max= dt_max, theTkSimulation=theTk,
                                           avoid_horizontal_angle_degree=avoid_horizontal_angle_degree,
                                           permanent_ratio_central=1/interface_reenforcement_central,
                                           permanent_ratio_tangential=1/interface_reenforcement_tangential,
                                           keep_viscosity_coefficients_constant=keep_viscosity_coefficients_constant
                                           )



    print("Turning on enhanced central repulsion, coefficient = ",central_repulsion_coefficient)
    theEnsemble.set_central_repulsion_coefficient(central_repulsion_coefficient)

    print("Avoiding full height spanning particles:", avoid_height_spanning_particles)
    theEnsemble.avoid_height_spanning_particles = avoid_height_spanning_particles  # Record this parameter for file saving

    theEnsemble.model=model


    reduction_factor=1

    if(do_debug):
        reduction_factor=10

    if do_pre_equilibration:

        theEnsemble.dt=final_dt

        mdt=0.25*model.time_constant/bimodal_factor
        if relative_viscosity <= 0.1:
            mdt = 0.2 * model.time_constant/bimodal_factor

        theEnsemble.dt_max=mdt

        if theEnsemble.packing_fraction > 2:
            theEnsemble.dt_max = theEnsemble.dt_max / 2


        if theEnsemble.permanent_ratio_central==1:
            theEnsemble.free_pre_equilibration(N=int(300/reduction_factor))
        else:
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))

        if anticipated_amplitude<=0.01 or relative_transversal_link_strength<0.1:
            if theEnsemble.permanent_ratio_central == 1:
                theEnsemble.free_pre_equilibration(N=int(300/reduction_factor))
            else:
                theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))



        theEnsemble.dt = final_dt
        theEnsemble.dt_max = dt_max

        if theEnsemble.permanent_ratio_central == 1:
            theEnsemble.free_pre_equilibration(N=int(200/reduction_factor))
        else:
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))
        if anticipated_amplitude <= 0.01 and theEnsemble.permanent_ratio_central==1:
            theEnsemble.free_pre_equilibration(N=int(200/reduction_factor))
        if anticipated_amplitude <= 0.001 and theEnsemble.permanent_ratio_central==1:
            theEnsemble.free_pre_equilibration(N=int(200/reduction_factor))

    if do_permanent_links:
        theEnsemble.makeAllLinksPermanent()
        if cut_top_bottom:
            theEnsemble.cutTopBottomEdge()
            theEnsemble.cut_top_bottom=True

        if(doCutByTriangulation):
            print("Preparing particles by triangulation; relative fuzziness on edges=",edge_fuzziness)
            theEnsemble.cutByTriangulation(cut_lines,edge_fuzziness=edge_fuzziness)
        else:
            print("Preparing particles by straight line cut")
            for i in range(cut_lines):
                theEnsemble.cutRandomLine()



        max_height=0

        if theEnsemble.avoid_height_spanning_particles:
            max_height=theEnsemble.maximal_particle_height()


        while theEnsemble.avoid_height_spanning_particles and max_height > theEnsemble.size_y*0.9:
            print("Discarded ensemble with full height spanning particles due to max height",max_height)
            print("\twith total particle count", len(theEnsemble.particles))
            theEnsemble.particles=[]  # Reset the particle registry in the particles
            theEnsemble.makeAllLinksPermanent()
            if cut_top_bottom:
                theEnsemble.cutTopBottomEdge()

            if doCutByTriangulation:
                print("Preparing particles by triangulation; relative fuzziness on edges=", edge_fuzziness)
                theEnsemble.cutByTriangulation(cut_lines,edge_fuzziness=edge_fuzziness)
            else:
                print("Preparing particles by straight line cut")
                for i in range(cut_lines):
                    theEnsemble.cutRandomLine()

            max_height = theEnsemble.maximal_particle_height()


        if remove_link_fraction>0:
            theEnsemble.remove_non_essential_links(max_fraction_to_remove=remove_link_fraction,physical_neighbors_only=True)

        theEnsemble.join_isolated_spheres()

        theEnsemble.dt_max = min(theEnsemble.dt*2,theEnsemble.dt_max)
        theEnsemble.dt = theEnsemble.dt

        if relative_transversal_link_strength>5 :
            theEnsemble.dt_max=theEnsemble.dt_max/2



        theEnsemble.free_pre_equilibration(N=int(300/reduction_factor))
        if anticipated_amplitude < 0.1:
            print("Extra equilibration for A<0.1")
            old_mu = theEnsemble.mu
            theEnsemble.mu = 0
            theEnsemble.free_pre_equilibration(N=int(150/reduction_factor))
            theEnsemble.mu = old_mu
            theEnsemble.free_pre_equilibration(N=int(150/reduction_factor))

        if anticipated_amplitude <= 0.01:
            print("Extra equilibration for A<=0.1")
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))
            old_mu = theEnsemble.mu
            theEnsemble.mu = 0
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))
            theEnsemble.mu = old_mu
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))

        if anticipated_amplitude <= 0.001:
            print("Extra equilibration for A<=0.001")
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))
            old_mu = theEnsemble.mu
            theEnsemble.mu = 0
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))
            theEnsemble.mu = old_mu
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))


        if anticipated_amplitude <= 0.0001:
            print("Extra equilibration for A<=0.0001")
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))
            old_mu = theEnsemble.mu
            theEnsemble.mu = 0
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))
            theEnsemble.mu = old_mu
            theEnsemble.free_pre_equilibration(N=int(100/reduction_factor))

        if anticipated_amplitude <= 0.001 and (not (interface_reenforcement_tangential==1) or not (interface_reenforcement_central==1)):
            theEnsemble.dt_max = theEnsemble.dt_max / 3
            print("Extra equilibration for A<=0.001")
            theEnsemble.free_pre_equilibration(N=int(200/reduction_factor))
            old_mu = theEnsemble.mu
            theEnsemble.mu = 0
            theEnsemble.free_pre_equilibration(N=int(200/reduction_factor))
            theEnsemble.mu = old_mu
            theEnsemble.free_pre_equilibration(N=int(200/reduction_factor))

    return theEnsemble



