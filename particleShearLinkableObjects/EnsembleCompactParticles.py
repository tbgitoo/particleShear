from tkinter import *
import random
import math

from .SphereLinkable import SphereLinkable
from .CanvasPointsLinkable import CanvasPointsLinkable
from particleShearBase import PointLeesEdwards
from particleShearObjects import r_estimate
from particleShearObjects import adjust_m
from particleShearObjects import particle_shear_model_parameters


class EnsembleCompactParticles (CanvasPointsLinkable):
    """Ensemble of `particleShear.SphereLinkable` objects (referred to as spheres), with possible crosslinking into
    distinct, compact particles

    This class maintains a list of objects of type
        `particleShear.SphereLinkable` and adds specific functions to the generation of the particles"""
    def __init__(self, size_x, size_y, N, packing_fraction=0.8, theCanvas=FALSE, doDrawing=False,
                 k=1, nu=0.01,m=1,
                 bimodal_factor=1.4,
                 k_t=1,nu_t=0.01,mu=0.1,dt=1,dt_max=10,theTkSimulation=False,avoid_horizontal_angle_degree=0):

        """Initialize self

                - **parameters**\n
                `size_x` Width of area to be used in pixels = micrometers for the simulation\n
                `size_y` Height of area to be used in pixels = micrometers for the simulation\n
                `N` The number of spheres to place
                `packing_fraction` The packing fraction indicating the density; this is defined as the area occupied by the
                non-compressed spheres as compared to the actual available area (size_x times size_y)
                `theCanvas` possibility to transmit a `tkinter` `Canvas` object for graphical output\n
                `doDrawing` Flag to indicate whether graphical output should be produced or not
                `k` Central spring constant in (mg/s^2)/m of depth;
                so F=-k*x*L with L the depth of the stack (the simulation is 2D) and x the compression\n
                `nu` Central viscosity force constant in (mg/s)/m of depth. This is to have F=nu*v*L, L again the depth\n
                `m` is the mass per unit of depth in mg/m of depth\n
                `bimodal_factor` is ratio of radii of the smaller and larger spheres in the bimodal distribution\n
                `k_t` Tangential spring constant in (mg/s^2)/m of depth;
                relevant for locked or permanent interfaces but not for slipping interfaces\n
                `nu_t` Central viscosity force constant in (mg/s)/m of depth.
                Relevant for frictionally locked and permanent interfaces but not slipping ones\n
                `mu` Friction coefficient, describes the maximum interface force for non-permanent interfaces by
                F_tangential_max = F_central*mu\n
                `dt` Time step for a single simulation step
                `dt_max` Maximal time step used during pre-equilibration, can be larger than `dt`\n
                `theTkSimulation` Tk master object associated with the `particleShear.CanvasPoints.theCanvas` used to trigger
                automatic update of the canvas in a simulation setting
                
                """

        self.bimodal_upper = math.sqrt(bimodal_factor)
        self.bimodal_lower = math.sqrt(1 / bimodal_factor)

        # The idea here is to be able to indicate an interval of angles near horizontal to be avoided in order not to generate
        # "pre-made" shear planes that would not be there in a larger ensemble
        # 0 or negative values indicate no restriction

        self.avoid_horizontal_angle_degree=avoid_horizontal_angle_degree
        self.avoid_height_spanning_particles=False # not an argument, just to register what has been done

        self.doCutByTriangulation = False
        self.removed_fraction=0 # For storing information about random link removal
        self.edge_fuzziness=0 # For storing information about making more fuzzy edges

        super(EnsembleCompactParticles, self).__init__(
            size_x, size_y, theCanvas=theCanvas, doDrawing=doDrawing,
                 k=k, nu=nu,m=m,k_t=k_t,nu_t=nu_t,mu=mu)
        self.N=N
        self.packing_fraction=packing_fraction
        self.dt=dt
        self.dt_max=dt_max
        self.theTkSimulation=theTkSimulation
        self.model=False

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
            self.sphereList.append(SphereLinkable("grey",
                                                  random.randrange(0, size_x),
                                                  random.randrange(0, size_y), r_sphere * 2,
                                                  adjust_m(m, r_sphere, r),
                                                  i, theCanvas, False, self, self.size_x, self.size_y))
        self.setShearInSpheres()
        self.setShearRateInSpheres()



        self.set_graphical_output_configuration(
            self.graphical_output_configuration)  # To propagate it also to the spheres

        self.initiateGraphics()
        # Particles are identified later on, once the spheres are redistributed and permanent links are formed
        self.particles = []



    def particle_info(self):
        return "Frictional spheres under Lees-Edwards boundary conditions, organized in fixed particles\n" \
               "\tSpheres with, bimodal distribution, equal probability, \n\tr1="+\
               str(self.r_max*0.8/1.2)+"r2="+str(self.r_max)+"\n\tidentical mass="+str(self.sphereList[0].m)+"mg"

    def random_radius_bimodal(self,r):
        return r*(self.bimodal_lower+(self.bimodal_upper-self.bimodal_lower)*random.randint(0, 1))




    def free_pre_equilibration(self,N=25):
        print("Unconstrained pre-equilibration ... N=",N,"dt =",self.dt,"max dt = ",self.dt_max)
        self.applyingShear = False
        dt=self.dt_max
        N = N
        cool_factor=0.5


        old_mu=self.mu

        self.mu=0

        print("Removing friction for initial equilibration")

        while dt>self.dt:

            self.mechanical_relaxation(dt=dt, theTk=self.theTkSimulation,
                    N=N, cool_factor=cool_factor)
            dt=dt/2
            cool_factor=(1+cool_factor)/2
            self.correct_linear_drift()
        dt = self.dt



        self.mechanical_relaxation(dt=dt, theTk=self.theTkSimulation,
                    N=N, cool_factor=1)

        self.mu = old_mu

        if self.mu>0:
            print("Initiate friction, mu=",self.mu)

        self.mechanical_relaxation(dt=dt, theTk=self.theTkSimulation,
                                   N=N, cool_factor=1)

        print("Done")


    def angle_OK(self,angle):
        if self.avoid_horizontal_angle_degree<=0:
            return True

        avoid_horizontal_angle = self.avoid_horizontal_angle_degree/180*math.pi

        # The angle that we are looking at is the angle between the norm vector and the x-axis

        # A first forbidden range is:
        # 90+/-avoid_horizontal_angle_degree (math.pi/2-avoid_horizontal_angle to math.pi/2+avoid_horizontal_angle)

        if angle>=math.pi/2-avoid_horizontal_angle and angle<=math.pi/2+avoid_horizontal_angle:
            return False

        # A second forbidden range is:
        # 270+/-avoid_horizontal_angle_degree (3*math.pi/2-avoid_horizontal_angle to 3*math.pi/2+avoid_horizontal_angle)

        if angle>=3*math.pi/2-avoid_horizontal_angle and angle<=3*math.pi/2+avoid_horizontal_angle:
            return False

        return True

    def maximal_particle_height(self):

        self.particles=[]
        self.identify_particles()



        max_height=0

        for theParticle in self.particles:
            if len(theParticle)>0:
                min_y = theParticle[0].y-theParticle[0].r
                max_y = theParticle[0].y+theParticle[0].r
                for theSphere in theParticle:
                    if theSphere.y-theSphere.r<min_y:
                        min_y=theSphere.y-theSphere.r
                    if theSphere.y+theSphere.r>max_y:
                        max_y=theSphere.y+theSphere.r
                if max_y - min_y > max_height:
                    max_height = max_y - min_y


        return max_height

    def join_isolated_spheres(self,physical_neighbors_only=True):
        for theSphere in self.sphereList:
            if len(theSphere.permanentlyConnectedSpheres(physical_neighbors_only=physical_neighbors_only))==0:
                non_permanent_neighbors=[]
                for theNeighbor in theSphere.neighbors:
                    if not (theNeighbor.interface_type=="permanent"):
                        non_permanent_neighbors.append(theNeighbor.theSphere)
                if len(non_permanent_neighbors)>0:
                    theSphere.establish_permanent_link(
                        non_permanent_neighbors[random.randint(0,len(non_permanent_neighbors)-1)],
                        do_backlink=True)



    def cutByTriangulationPoints(self, triangulation_points, edge_fuzziness=0):
        # First, for each sphere, identify the neareast of the triangulation points

        nearest_point=[]

        self.edge_fuzziness=edge_fuzziness

        print("cutByTriangulationPoints, max r=",self.r_max,"edge fuzziness = ",self.edge_fuzziness)

        for theSphere in self.sphereList:
            min_dist=0
            min_index = -1
            started=False
            for triangulation_index in range(len(triangulation_points)):
                # Minimal distance to triangulation points, with possibility to randomness to generate fuzzier edges
                current_d=theSphere.d(triangulation_points[triangulation_index])+edge_fuzziness*random.random()*self.r_max
                if (not started) or (current_d<min_dist):
                    min_index=triangulation_index
                    min_dist=current_d
                    started=True
            nearest_point.append(min_index)

        for theIndex in range(len(self.sphereList)):
            theSphere = self.sphereList[theIndex]
            for theNeighbor in theSphere.neighbors:
                if (theNeighbor.interface_type == "permanent"):
                    theOtherIndex = self.sphereList.index(theNeighbor.theSphere)
                    if not (nearest_point[theIndex]==nearest_point[theOtherIndex]):
                        theSphere.cut_permanent_link(theNeighbor.theSphere)



    def cutByTriangulation(self, n_points=5,edge_fuzziness=0):
        thePoints=[]
        for ind in range(n_points):
            thePoints.append(PointLeesEdwards(random.random()*self.size_x,random.random()*self.size_y,
                                              size_x=self.size_x,size_y=self.size_y))

        self.cutByTriangulationPoints(thePoints,edge_fuzziness=edge_fuzziness)

        self.doCutByTriangulation = True



    def cutRandomLine(self):
        if self.avoid_horizontal_angle_degree<=0:
            super(EnsembleCompactParticles,self).cutRandomLine()
            return

        point = [random.randint(0, self.size_x), random.randint(0, self.size_y)]
        angle = random.random() * 2 * math.pi
        while not self.angle_OK(angle):
            print("Rejecting angle",angle/math.pi*180)
            angle = random.random() * 2 * math.pi
        self.cutLine(point, angle)

        self.doCutByTriangulation = False

    # Functions relatiting to identifying coherent particles

    def findParticle(self,theSphere):

        for theParticle in self.particles:
            if theParticle.count(theSphere):
                return theParticle
        return False


    # Checks whether a given pair of spheres is connected permanently.
    # Four return values are possible: "direct", "indirect", "no_connection", or False if there was some error
    def permanentConnectionBetweenSpheres(self,theSphere1, theSphere2,physical_neighbors_only=True):
        if not self.sphereList.count(theSphere1):
            print("permanentConnectionBetweenSpheres: Sphere not found")
            return False
        if not self.sphereList.count(theSphere2):
            print("permanentConnectionBetweenSpheres: Sphere not found")
            return False

        neighbors1 = theSphere1.permanentlyConnectedSpheres(physical_neighbors_only)

        if(neighbors1.count(theSphere2)):
            return "direct"

        neighbors2 = theSphere2.permanentlyConnectedSpheres(physical_neighbors_only)

        if (neighbors2.count(theSphere1)):
            return "direct"

        self.identify_particles(physical_neighbors_only)

        particle1=self.findParticle( theSphere1)

        if not particle1:
            print("permanentConnectionBetweenSpheres: No particle found for given sphere")
            return False

        particle2 = self.findParticle( theSphere2)

        if not particle2:
            print("permanentConnectionBetweenSpheres: No particle found for given sphere")
            return False

        if(particle1==particle2):
            return "indirect"

        return "no_connection"


    def n_permanent_connections(self,physical_neighbors_only=True):
        n=0
        for theSphere in self.sphereList:
            n=n+len(theSphere.permanentlyConnectedSpheres(physical_neighbors_only))
        return (n/2)


    def remove_non_essential_links(self, max_fraction_to_remove,physical_neighbors_only=True, max_trials=1000 ):
        self.identify_particles(physical_neighbors_only)

        failed_trials=0
        succesful_trials=0

        n_links = self.n_permanent_connections(physical_neighbors_only)

        print("Removing connections (non-essential): Target removal fraction ",max_fraction_to_remove," total initial links ",n_links)

        while failed_trials<max_trials and succesful_trials<max_fraction_to_remove*n_links:
            failed_trials=failed_trials+1
            sphereIndex=random.randint(0,len(self.sphereList)-1)
            selectedSphere = self.sphereList[sphereIndex]
            neighbors = selectedSphere.permanentlyConnectedSpheres(physical_neighbors_only)
            if len(neighbors)>0:
                neighborIndex = random.randint(0,len(neighbors)-1)
                theNeighbor = neighbors[neighborIndex]
                # Try to cut the connection
                selectedSphere.cut_permanent_link(theNeighbor,do_backlink=True)
                self.identify_particles(physical_neighbors_only)
                connectivity=self.permanentConnectionBetweenSpheres(selectedSphere, theNeighbor,physical_neighbors_only)
                if connectivity=="indirect":
                    succesful_trials=succesful_trials+1
                    failed_trials=0
                else:
                    selectedSphere.establish_permanent_link(theNeighbor,do_backlink=True)

        self.removed_fraction=succesful_trials/n_links

        print("Removing connections (non-essential): Actual removal fraction = ",self.removed_fraction)

    def identify_particles(self,physical_neighbors_only=True):
        self.particles=[]
        for theSphere in self.sphereList:
            if not self.findParticle(theSphere):
                self.addParticleFromSphere(theSphere,physical_neighbors_only)

    # The idea here is that we loop through all the spheres of the particle by keeping an overall non-listed array up to date
    def addParticleFromSphere(self,theSphere,physical_neighbors_only=True):
        # Start the particles
        newParticle = [theSphere]
        # Add to the particles list
        self.particles.append(newParticle)

        # Find the neighbors of the first sphere
        neighbors=theSphere.permanentlyConnectedSpheres(physical_neighbors_only)

        # initiate the not-yet-listed array
        non_listed=[]

        # First round of neighbors: if not in the particle, list uniquely in the non-listed array (so check before adding
        # the spheres that they are not already listed, this is important as several paths can lead to the same sphere
        for theNeighbor in neighbors:
            if not newParticle.count(theNeighbor):
                if not non_listed.count(theNeighbor):
                    non_listed.append(theNeighbor)



        # While we still have non-listed spheres in the non-listed array, go ahead
        while len(non_listed)>0:
            # First, add the currently non-listed spheres to the particle
            for sphereToAdd in non_listed:
                newParticle.append(sphereToAdd)

            # start a new screen for the neighbors specifically of the just-added spheres (for older spheres, all the
            # neighbors should already be included)
            neighbors = []

            for theSphere in non_listed:
                # get the neighbors of the sphere
                localNeighbors = theSphere.permanentlyConnectedSpheres()
                for l in localNeighbors:
                    # check whether the neighbors are listed in the particles
                    if not newParticle.count(l):
                        # if not already listed, add to the listed
                        if not neighbors.count(l):
                            neighbors.append(l)
            # the new non-particle neighbors become the new-non listed spheres
            non_listed = neighbors



def EnsembleCompactParticlesFromModelParameters(size_x=500,size_y=500,N=100,packing_fraction=1,mu=1,
                                                Young_modulus_spheres=10000,density=50,bimodal_factor=1.4,
                                                cut_lines=5,do_permanent_links=True,theTk=False,do_pre_equilibration=True,
                                                relative_viscosity=0.01,central_repulsion_coefficient=0,anticipated_amplitude=0.1,
                                                relative_transversal_link_strength=1,avoid_horizontal_angle_degree=0,
                                                avoid_height_spanning_particles=False,doCutByTriangulation=True,doDrawing=True,
                                                do_debug=False):

    

    # First, some logics: with permanent links but insufficient tools to cut them, height spanning particles cannot be avoided

    if avoid_height_spanning_particles and ((doCutByTriangulation and cut_lines<=1) or ((not doCutByTriangulation)
                                    and cut_Lines<=0)):
        avoid_height_spanning_particles=False
        print("Cannot avoid height spanning particles for bulk ensembles")

    theCanvas=False

    if doDrawing and not theTk:
        theTk = Tk()

    if doDrawing:

        theCanvas = Canvas(theTk, width=size_x, height=size_y)

        theCanvas.pack()







    model = particle_shear_model_parameters(size_x=size_x, size_y=size_y, N=N,
                                            packing_fraction=packing_fraction,
                                            Young_modulus_spheres=Young_modulus_spheres,density=density,
                                            bimodal_factor=1)

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




    theEnsemble = EnsembleCompactParticles(size_x, size_y, N, packing_fraction,
                                           theCanvas, doDrawing=doDrawing, k=model.k,
                                           nu= relative_viscosity*model.k * model.time_constant, m=model.m,
                                           bimodal_factor=bimodal_factor,
                                           k_t=model.k*relative_transversal_link_strength,
                                           nu_t= relative_viscosity*model.k * model.time_constant*relative_transversal_link_strength,
                                           mu=mu,
                                           dt=final_dt, dt_max= dt_max, theTkSimulation=theTk,
                                           avoid_horizontal_angle_degree=avoid_horizontal_angle_degree)


    print("Turning on enhanced central repulsion, coefficient = ",central_repulsion_coefficient)
    theEnsemble.set_central_repulsion_coefficient(central_repulsion_coefficient)

    print("Avoiding full height spanning particles:",avoid_height_spanning_particles)
    theEnsemble.avoid_height_spanning_particles=avoid_height_spanning_particles # Record this parameter for file saving


    theEnsemble.model=model

    if do_pre_equilibration:

        theEnsemble.dt=final_dt

        mdt=0.25*model.time_constant/bimodal_factor
        if relative_viscosity <= 0.1:
            mdt = 0.2 * model.time_constant/bimodal_factor

        theEnsemble.dt_max=mdt

        N_step=300

        if(do_debug):
            N_step=30

        theEnsemble.free_pre_equilibration(N=N_step)

        if anticipated_amplitude<=0.01 or relative_transversal_link_strength<0.1:
            theEnsemble.free_pre_equilibration(N=N_step)

        theEnsemble.dt = final_dt
        theEnsemble.dt_max = dt_max

        N_step=200

        if (do_debug):
            N_step = 20

        theEnsemble.free_pre_equilibration(N=N_step)
        if anticipated_amplitude <= 0.01:
            theEnsemble.free_pre_equilibration(N=N_step)
        if anticipated_amplitude <= 0.001:
            theEnsemble.free_pre_equilibration(N=N_step)

    if do_permanent_links:
        theEnsemble.makeAllLinksPermanent()

        theEnsemble.cutTopBottomEdge()

        if (doCutByTriangulation):
            print("Preparing particles by triangulation")
            theEnsemble.cutByTriangulation(cut_lines)
        else:
            print("Preparing particles by straight line cut")
            for i in range(cut_lines):
                theEnsemble.cutRandomLine()

        max_height=0

        if theEnsemble.avoid_height_spanning_particles:
            max_height=theEnsemble.maximal_particle_height()


        while theEnsemble.avoid_height_spanning_particles and max_height > theEnsemble.size_y*0.9:
            theEnsemble.makeAllLinksPermanent()

            theEnsemble.cutTopBottomEdge()

            if (doCutByTriangulation):
                print("Preparing particles by triangulation")
                theEnsemble.cutByTriangulation(cut_lines)
            else:
                print("Preparing particles by straight line cut")
                for i in range(cut_lines):
                    theEnsemble.cutRandomLine()

            if theEnsemble.avoid_height_spanning_particles:
                max_height = theEnsemble.maximal_particle_height()

        theEnsemble.join_isolated_spheres()

        theEnsemble.dt_max = min(theEnsemble.dt*2,theEnsemble.dt_max)
        theEnsemble.dt = theEnsemble.dt

        if relative_transversal_link_strength>5:
            theEnsemble.dt_max=theEnsemble.dt_max/2


        theEnsemble.free_pre_equilibration()



    return theEnsemble










