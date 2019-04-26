from tkinter import *
import random
import math
from .SphereLeesEdwards import SphereLeesEdwards
from particleShearBase import CanvasPointsBasicElasticityLeesEdwards
from .Ensemble import r_estimate
from .Ensemble import adjust_m
from particleShearBase import Force_register

class EnsembleLeesEdwards(CanvasPointsBasicElasticityLeesEdwards):
    """Ensemble of particles of type  `particleShear.SphereLeesEdwards`, with Lees-Edwards boundary conditions

                    This class creates and maintains a list of objects of type
                    `particleShear.SphereLeesEdwards`. These objects are generically
                    referred to as spheres and are stored in `particleShear.CanvasPoints.sphereList`.\n
                    This class uses Lees-Edwards boundary conditions\n
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
                                `doDrawing` Flag to indicate whether graphical output should be produced or not\n
                                `k` Central spring constant in (mg/s^2)/m of depth;
                                so F=-k*x*L with L the depth of the stack (the simulation is 2D) and x the compression\n
                                `nu` Central viscosity force constant in (mg/s)/m of depth. This is to have F=nu*v*L, L again the depth\n
                                `m` is the average mass per unit of depth in mg/m of depth\n
                                `bimodal_factor` is ratio of radii of the smaller and larger spheres in the bimodal distribution
                                """

        super(EnsembleLeesEdwards,self).__init__(size_x, size_y,  theCanvas=theCanvas, doDrawing=False, k=k, nu=nu,m=m)

        self.bimodal_upper = math.sqrt(bimodal_factor)
        """Upper multiplication factor for the bimodal sphere size distribution"""
        self.bimodal_lower = math.sqrt(1 / bimodal_factor)
        """Lower multiplication factor for the bimodal sphere size distribution"""

        self.N = N
        """Number of spheres"""
        self.packing_fraction = packing_fraction
        """Packing fraction: relative area occupied by the uncompressed spheres as compared to the available area"""

        self.doDrawing=doDrawing
        """Boolean: Should we draw the ensemble during simulation"""

        self.sphereList = []
        """List of the spheres"""

        r=self.size_y/2 # default value
        if N>0:
            r = r_estimate(self.size_x, self.size_y, packing_fraction, N,
                           bimodal_upper=self.bimodal_upper,
                           bimodal_lower=self.bimodal_lower)

        self.r_max = 0
        """Largest sphere radius"""
        for i in range(N):
            r_sphere = self.random_radius_bimodal(r)
            if r_sphere > self.r_max:
                self.r_max = r_sphere
            self.sphereList.append(SphereLeesEdwards("grey",
                                                     random.randrange(0, size_x),
                                                     random.randrange(0, size_y), r_sphere * 2,
                                                     adjust_m(m, r_sphere, r),
                                                     i, theCanvas, False,self,self.size_x,self.size_y))

        self.setShearInSpheres()

        self.initiateGraphics()


    def particle_info(self):
        """Provide short description of particle type of inclusion into output file

        Method defined in `particleShear.EnsembleLeesEdwards` """
        return "Non-frictional spheres with Lees-Edwards boundary conditions, \n\tbimodal distribution, equal probability, \n\tr1="+\
               str(self.r_max*0.8/1.2)+"r2="+str(self.r_max)+"\n\tidentical mass="+str(self.sphereList[0].m)+"mg"


    def random_radius_bimodal(self,r):
        """Choose randomly one of the two bimodal radius values.

        Method defined in `particleShear.EnsembleLeesEdwards`"""
        return r*(self.bimodal_lower+(self.bimodal_upper-self.bimodal_lower)*random.randint(0, 1))

