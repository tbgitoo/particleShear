from particleShearSimulation import Simulation_interlocking_rheology


def doParticleShearSimulation(root_folder="",theAmplitude=0.2,theMu=0.01,do_permanent_links=True,
                    cut_lines=5,Young_modulus_spheres=8000,
                    N=150,packing_fraction=1.5,density=50,bimodal_factor=1.4,
                    relative_viscosity=0.1,relative_transversal_link_strength=1,relative_frequency=0.025,
                    avoid_horizontal_angle_degree=15,interface_reenforcement_central=1,interface_reenforcement_tangential=1,
                    keep_viscosity_coefficients_constant=False,avoid_height_spanning_particles=True,cut_top_bottom=False,
                    saveOutputImages=False,imageFileType ="jpg",
                    remove_link_fraction=0,edge_fuzziness=0,
                    central_repulsion_coefficient=1,
                    doCutByTriangulation=True,doDrawing=True,saveData=False,
                    saveStressTensorData=True,
                    plotStress=True,relative_y_scale_force = 1e8,
                    pre_periods=2,periods=3,post_periods=1,cool_factor=0.5):


    #if theAmplitude < 0.005:
    #    relative_y_scale_force = relative_y_scale_force * theAmplitude / 0.005



    theSimulation = Simulation_interlocking_rheology(
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
                                  "\n\ttheSimulation.baseline_pre_periods = " + str(pre_periods) +\
                                  "\n\ttheSimulation.baseline_post_periods = " + str(post_periods)+ \
                                  "\n\ttheSimulation.saveOutputImages = " + str(saveOutputImages)+ \
                                  "\n\ttheSimulation.imageFileType = " + str(imageFileType) + \
                                  "\n\ttheSimulation.runSimulation(periods="+str(periods)+", cool_factor="+\
                                  str(cool_factor)+")"

    theSimulation.baseline_pre_periods = pre_periods
    theSimulation.baseline_post_periods = post_periods

    theSimulation.saveOutputImages = saveOutputImages
    theSimulation.imageFileType = imageFileType


    theSimulation.saveStressTensorData=saveStressTensorData

    return(theSimulation.runSimulation(periods=periods, cool_factor=cool_factor,plotStress=plotStress))



