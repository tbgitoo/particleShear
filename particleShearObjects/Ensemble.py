from tkinter import *
import random
import math
from .Sphere import Sphere
from .SphereFriction import SphereFriction
from particleShearBase import Force_register
from particleShearBase import Graphical_output_configuration
from particleShearBase import CanvasPointsBasicElasticity


def r_estimate(size_x,size_y,packing_fraction,N,bimodal_upper=1.2,bimodal_lower=0.8):
    """Average radius

    TWe find the average radius from the `packing_fraction`, the available area
    `size_x` times `size_y` and the desired number of spheres. Indeed, collectively the `N` spheres should
    occupy a theoretical area of `size_x` times `size_y` divided by `N`. In a real situation, they will of
     course occupy
    a smaller area due to compression. However, as the `packing_fraction`, also referred to as notional phase volume
     (Evans, I.D. and A. Lips, Concentration-Dependence of the Linear Elastic Behavior of Model Microgel Dispersions.
     Journal of the Chemical Society-Faraday Transactions, 1990. 86(20): p. 3413-3417.) is defined relative to the fully
     expanded state, this does not matter. If the spheres had a homogeneous size, the relevant radius would be \n
     sqrt(size_x * size_y * packing_fraction / N / math.pi) \n

    Now, to avoid crystallization, a bimodal distribution of sphere radii needs to be used
    Otsuki, M. and H. Hayakawa, Discontinuous
    change of shear modulus for frictional
    jammed granular materials. Phys Rev E, 2017. 95(6-1): p. 062902. Still, the area occupied by the spheres should
    match size_x * size_y * packing_fraction. In analogy to Otsuki et al.,
    We chose our bimodal distribution at radii +/- 20 percent of the nominal radius, as the sum of the areas of a
    circle of 1.2 times r + the area of a circle of 0.8 times r is slightly bigger than twice the area of a circle of
    radius r, we correct for this. The correction is however minor, its just 4 percent.
    """
    return math.sqrt(size_x * size_y * packing_fraction / N / math.pi / (bimodal_upper * bimodal_upper + \
                                                                         bimodal_lower * bimodal_lower) * 2)


def adjust_m(m,r_actual,r_mean):
    """Adjust the mass for the actual radius as compared to the average theoretical radius"""
    return m*r_actual*r_actual/r_mean/r_mean

class Ensemble(CanvasPointsBasicElasticity):
    """Ensemble of particles of type  `particleShear.SphereFriction`, with regular boundary conditions

        This class creates and maintains a list of objects of type
        `particleShear.SphereFriction`. These objects are generically
        referred to as spheres and are stored in `particleShear.CanvasPoints.sphereList`.\n
        The ensemble class does not implement proper Lees-Edwards boundaries, but emulates neighboring spheres by
        creating replicates of the spheres near the boundares displaced by one positive or negative multiple of the
        xy dimensions of the simulation area.\n
        Class defined in subpackage particleShearObjects"""

    def __init__(self, size_x, size_y, N, packing_fraction=0.8, theCanvas=False, doDrawing=False, k=1, nu=0.01,m=1,
                 bimodal_factor=1.4):
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
        """

        super(Ensemble,self).__init__(size_x=size_x,size_y=size_y,theCanvas=theCanvas,doDrawing=doDrawing,k=k, nu=nu,m=m)

        self.bimodal_upper = math.sqrt(bimodal_factor)
        """Upper multiplication factor for the bimodal sphere size distribution"""
        self.bimodal_lower = math.sqrt(1/bimodal_factor)
        """Lower multiplication factor for the bimodal sphere size distribution"""

        self.N = N
        """Number of spheres"""

        self.packing_fraction = packing_fraction
        """Packing fraction: relative area occupied by the uncompressed spheres as compared to the available area"""

        self.k = k
        """Central spring constant in (mg/s^2)/m of depth"""
        self.nu = nu
        """Central viscosity constant in (mg/s)/m of depth"""


        self.record_type = "internal"
        """Helper variable to distinguish between internal spheres and boundary replicates for the accounting of internal
        and external forces"""


        r=self.size_y/2 # If there are no spheres specified, keep some default value

        if N>0:
            r = r_estimate(self.size_x , self.size_y ,packing_fraction , N,
                           bimodal_upper=self.bimodal_upper,
                           bimodal_lower=self.bimodal_lower )

        self.r_max = 0
        """Largest sphere radius"""
        for i in range(N):
            r_sphere = self.random_radius_bimodal(r)
            if r_sphere > self.r_max:
                self.r_max = r_sphere
            self.sphereList.append(SphereFriction("grey",
                                                     random.randrange(0, size_x),
                                                     random.randrange(0, size_y), r_sphere * 2,
                                                     adjust_m(m, r_sphere, r),
                                                     i,theCanvas, False,self))
        self.spheres_boundary = []
        """List of the spheres on the boundary"""

        self.set_graphical_output_configuration(self.graphical_output_configuration) # To propagate it also to the spheres

        self.initiateGraphics()





    def random_radius_bimodal(self,r):
        """Choose randomly one of the two bimodal radius values.

        Method defined in `particleShear.Ensemble`"""
        return r*(self.bimodal_lower+(self.bimodal_upper-self.bimodal_lower)*random.randint(0, 1))


    # For recording incoming force reported by the spheres

    def record_individual_internal_force(self,target,source,force_vector):
        """Record internal force

        Internal forces are the forces that act between spheres within the interior of the simulation. That is,
        they are able to move, and are not replicates to emulate periodic or other boundaries. In this class, the
        distinction between internal and external forces is made by using the instance variable `particleShear.Ensemble.record_type`
        which switches between internal and external depending on whether forces originating from internal spheres
        or boundary replicates are considered.\n\n
        Method defined in `particleShear.Ensemble`"""

        if not self.canMove(target):
            return
        if self.record_type=="internal":
            super(Ensemble,self).record_individual_internal_force(target,source,force_vector)
        else: # running virtual boundary replicates, this is also external here
            self.record_external_force(target, force_vector)




    def particle_info(self):
        """Provide short description of particle type of inclusion into output file

        Method defined in `particleShear.Ensemble` """
        return "Non-frictional spheres, \n\tbimodal distribution, equal probability, \n\tr1="+\
               str(self.r_max*0.8/1.2)+"r2="+str(self.r_max)+"\n\tidentical mass="+str(self.sphereList[0].m)+"mg"

    def test_neighbor_relation(self):
        """Instruct every sphere to test establish its geometric (and possibly permanent) neighbors.

        This function calls `particleShear.CircleMassNeighbors.test_neighbor_relation` on each member of the
        `particleShear.CanvasPoints.sphereList`. It does so not only on the actuale sphere list, but also on the
        replicates used to emulate the boundary environment in this class.\n
        This method is defined in class `particleShear.Ensemble`"""
        super(Ensemble,self).test_neighbor_relation()
        for sphereIndex in range(len(self.sphereList)):
             for sphereIndexBoundary in range(len(self.spheres_boundary)):
                self.sphereList[sphereIndex].test_neighbor_relation(self.spheres_boundary[sphereIndexBoundary])


    def elastic_force(self):
        """Let all spheres calculate the central elastic force acting on them

        This includes forces acting from the replicated boundary spheres.

        This method is defined in class `particleShear.Ensemble`"""
        self.record_type = "interal"
        super(Ensemble,self).elastic_force()
        self.record_type = "external"
        for sphereIndex in range(len(self.sphereList)):
             for sphereIndexBoundary in range(len(self.spheres_boundary)):
                self.sphereList[sphereIndex].elastic_force(self.spheres_boundary[sphereIndexBoundary], self.k)


    def central_viscous_force(self):
        """Let all spheres calculate the central elastic force acting on from their known neighbors.

         This includes forces acting from the replicated boundary spheres. \n
         This method is defined in class `particleShear.CanvasPointsBasicElasticity`"""

        self.record_type = "interal"
        super(Ensemble, self).central_viscous_force()
        self.record_type = "external"
        for sphereIndex in range(len(self.sphereList)):
              for sphereIndexBoundary in range(len(self.spheres_boundary)):
                self.sphereList[sphereIndex].central_viscous_force(self.spheres_boundary[sphereIndexBoundary],
                                                                   self.nu)



    def periodic_boundary_extension(self):
        """Create periodic boundary extension.

         The function replicates spheres near the boundary to obtain virtual copies
         displaced by one positive or negative of the simulation area, in both x and y direction and also
         in corners by displacement in both x and y direction.


         This method is defined in class `particleShear.Ensemble`"""

        if self.doDrawing:

            for theSphere in self.spheres_boundary:
                theSphere.deleteDrawing()

        max_index=0
        for theSphere in self.sphereList:
            if max_index<theSphere.myindex:
                max_index=theSphere.myindex

        self.spheres_boundary = []
        index=max_index+1
        for theSphere in self.sphereList:
            pos = theSphere.coordinates()

            left_edge = pos[0] - pos[2] <= self.r_max
            right_edge = pos[0] + pos[2] >= self.size_x - self.r_max
            upper_edge = pos[1] - pos[2] <= self.r_max
            lower_edge = pos[1] + pos[2] >= self.size_y - self.r_max

            if left_edge:
                self.spheres_boundary.append(SphereFriction(
                    "green", pos[0] + self.size_x, pos[1], 2 * pos[2],
                    theSphere.m,index,self.theCanvas, self.doDrawing))
                index=index+1
                if upper_edge:
                    self.spheres_boundary.append(SphereFriction(
                        "green", pos[0] + self.size_x, pos[1] + self.size_y, 2 * pos[2],
                        theSphere.m,index, self.theCanvas, self.doDrawing))
                    index=index+1
                if lower_edge:
                    self.spheres_boundary.append(SphereFriction(
                        "green", pos[0] + self.size_x, pos[1] - self.size_y, 2 * pos[2],
                        theSphere.m,index, self.theCanvas, self.doDrawing))
                    index=index+1
            if right_edge:
                self.spheres_boundary.append(SphereFriction(
                    "green", pos[0] - self.size_x, pos[1], 2 * pos[2],
                    theSphere.m,index, self.theCanvas, self.doDrawing))
                index=index+1
                if upper_edge:
                    self.spheres_boundary.append(SphereFriction(
                        "green", pos[0] - self.size_x, pos[1] + self.size_y, 2 * pos[2],
                        theSphere.m,index,self.theCanvas, self.doDrawing))
                    index=index+1
                if lower_edge:
                    self.spheres_boundary.append(SphereFriction(
                        "green", pos[0] - self.size_x, pos[1] - self.size_y, 2 * pos[2],
                        theSphere.m, index,self.theCanvas, self.doDrawing))
                    index=index+1
            if upper_edge:
                self.spheres_boundary.append(SphereFriction(
                    "green", pos[0], pos[1] + self.size_y, 2 * pos[2],
                    theSphere.m,index, self.theCanvas, self.doDrawing))
                index=index+1
            if lower_edge:
                self.spheres_boundary.append(SphereFriction(
                    "green", pos[0], pos[1] - self.size_y, 2 * pos[2],
                    theSphere.m,index, self.theCanvas, self.doDrawing))
                index=index+1


    def mechanical_simulation_step_calculate_forces(self):
        """ Calculate the forces acting on the spheres

        This method is defined in class `particleShear.Ensemble`"""

        self.reset_force_register()
        self.periodic_boundary_extension()
        self.test_neighbor_relation()
        self.elastic_force_from_neighbors()
        self.central_viscous_force_from_neighbors()




