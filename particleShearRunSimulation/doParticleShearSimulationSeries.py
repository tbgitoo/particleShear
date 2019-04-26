from .doParticleShearSimulation import doParticleShearSimulation


def doParticleShearSimulationSeries(root_folder="",amplitudes=[0.2],mu=[0.01],cut_lines=5,Young_modulus_spheres=8000,
                    do_bulk_control=False,do_uncrosslinked_control=False,
                    do_non_frictional_control=False,N_repetitions=6,
                    N=150,packing_fraction=1.5,
                    density=50,
                    bimodal_factor=1.4,
                    relative_viscosity=0.1,relative_transversal_link_strength=1,
                    relative_frequency=0.025,
                    avoid_horizontal_angle_degree=15,
                    interface_reenforcement_central=1,interface_reenforcement_tangential=1,
                    keep_viscosity_coefficients_constant=False,
                    avoid_height_spanning_particles=True,cut_top_bottom=False,
                    doCutByTriangulation=True,
                    saveOutputImages=False,imageFileType = "jpg",
                    remove_link_fraction=0,
                    edge_fuzziness=0,central_repulsion_coefficient=1,
                    doDrawing=True,saveData=False,saveStressTensorData=True,plotStress=True,
                    pre_periods=2, periods=3, post_periods=1, cool_factor=0.5):

    for i in range(N_repetitions):
        for theAmplitude in amplitudes:


            for theMu in mu:
                # Control: Bulk (this is the same as the biomaterial call, but cut_lines=0
                if do_bulk_control:

                    doParticleShearSimulation(root_folder,theAmplitude=theAmplitude,
                        theMu=theMu,do_permanent_links=True,cut_lines=0,
                        Young_modulus_spheres=Young_modulus_spheres,
                        N=N,packing_fraction=packing_fraction,
                        density=density,
                        bimodal_factor=bimodal_factor,
                        relative_viscosity=relative_viscosity,
                        relative_transversal_link_strength=relative_transversal_link_strength,
                        relative_frequency=relative_frequency,
                        avoid_horizontal_angle_degree=avoid_horizontal_angle_degree,
                        interface_reenforcement_central=interface_reenforcement_central,
                        interface_reenforcement_tangential=interface_reenforcement_tangential,
                        keep_viscosity_coefficients_constant=keep_viscosity_coefficients_constant,
                        avoid_height_spanning_particles=avoid_height_spanning_particles,cut_top_bottom=cut_top_bottom,
                        saveOutputImages=saveOutputImages,imageFileType =imageFileType,
                        remove_link_fraction=remove_link_fraction,
                        edge_fuzziness=edge_fuzziness,
                        central_repulsion_coefficient=central_repulsion_coefficient,
                        doCutByTriangulation=doCutByTriangulation,
                        doDrawing=doDrawing,
                        saveData=saveData,
                        saveStressTensorData=saveStressTensorData,
                        plotStress=plotStress,
                        pre_periods=pre_periods,periods=periods,post_periods=post_periods,cool_factor=cool_factor)




                # Actual biomaterial: crosslinked but cut into particles
                doParticleShearSimulation(root_folder, theAmplitude=theAmplitude,
                    theMu=theMu, do_permanent_links=True, cut_lines=cut_lines,
                    Young_modulus_spheres=Young_modulus_spheres,
                    N=N, packing_fraction=packing_fraction,
                    density=density,
                    bimodal_factor=bimodal_factor,
                    relative_viscosity=relative_viscosity,
                    relative_transversal_link_strength=relative_transversal_link_strength,
                    relative_frequency=relative_frequency,
                    avoid_horizontal_angle_degree=avoid_horizontal_angle_degree,
                    interface_reenforcement_central=interface_reenforcement_central,
                    interface_reenforcement_tangential=interface_reenforcement_tangential,
                    keep_viscosity_coefficients_constant=keep_viscosity_coefficients_constant,
                    avoid_height_spanning_particles=avoid_height_spanning_particles,
                    cut_top_bottom=cut_top_bottom,
                    saveOutputImages=saveOutputImages,imageFileType =imageFileType,
                    remove_link_fraction=remove_link_fraction,
                    edge_fuzziness=edge_fuzziness,
                    central_repulsion_coefficient=central_repulsion_coefficient,
                    doCutByTriangulation=doCutByTriangulation,
                    doDrawing=doDrawing,
                    saveData=saveData,
                    saveStressTensorData=saveStressTensorData,
                    plotStress=plotStress,
                    pre_periods=pre_periods, periods=periods, post_periods=post_periods,
                    cool_factor=cool_factor)

                # Control: uncrosslinked spheres only
                if do_uncrosslinked_control:
                    doParticleShearSimulation(root_folder, theAmplitude=theAmplitude,
                        theMu=theMu, do_permanent_links=False, cut_lines=0,
                        Young_modulus_spheres=Young_modulus_spheres,
                        N=N, packing_fraction=packing_fraction,
                        density=density,
                        bimodal_factor=bimodal_factor,
                        relative_viscosity=relative_viscosity,
                        relative_transversal_link_strength=relative_transversal_link_strength,
                        relative_frequency=relative_frequency,
                        avoid_horizontal_angle_degree=avoid_horizontal_angle_degree,
                        interface_reenforcement_central=interface_reenforcement_central,
                        interface_reenforcement_tangential=interface_reenforcement_tangential,
                        keep_viscosity_coefficients_constant=keep_viscosity_coefficients_constant,
                        avoid_height_spanning_particles=avoid_height_spanning_particles,
                        cut_top_bottom=cut_top_bottom,
                        saveOutputImages=saveOutputImages,imageFileType =imageFileType,
                        remove_link_fraction=remove_link_fraction,
                        edge_fuzziness=edge_fuzziness,
                        central_repulsion_coefficient=central_repulsion_coefficient,
                        doCutByTriangulation=doCutByTriangulation,
                        doDrawing=doDrawing,
                        saveData=saveData,
                        saveStressTensorData=saveStressTensorData,
                        plotStress=plotStress,
                        pre_periods=pre_periods, periods=periods, post_periods=post_periods,
                        cool_factor=cool_factor)


                # Control: non-frictional
                if do_non_frictional_control:
                    doParticleShearSimulation(root_folder, theAmplitude=theAmplitude,
                        theMu=0, do_permanent_links=True, cut_lines=cut_lines,
                        Young_modulus_spheres=Young_modulus_spheres,
                        N=N, packing_fraction=packing_fraction,
                        density=density,
                        bimodal_factor=bimodal_factor,
                        relative_viscosity=relative_viscosity,
                        relative_transversal_link_strength=relative_transversal_link_strength,
                        relative_frequency=relative_frequency,
                        avoid_horizontal_angle_degree=avoid_horizontal_angle_degree,
                        interface_reenforcement_central=interface_reenforcement_central,
                        interface_reenforcement_tangential=interface_reenforcement_tangential,
                        keep_viscosity_coefficients_constant=keep_viscosity_coefficients_constant,
                        avoid_height_spanning_particles=avoid_height_spanning_particles,
                        cut_top_bottom=cut_top_bottom,
                        saveOutputImages=saveOutputImages,imageFileType =imageFileType,
                        remove_link_fraction=remove_link_fraction,
                        edge_fuzziness=edge_fuzziness,
                        central_repulsion_coefficient=central_repulsion_coefficient,
                        doCutByTriangulation=doCutByTriangulation,
                        doDrawing=doDrawing,
                        saveData=saveData,
                        saveStressTensorData=saveStressTensorData,
                        plotStress=plotStress,
                        pre_periods=pre_periods, periods=periods, post_periods=post_periods,
                        cool_factor=cool_factor)


