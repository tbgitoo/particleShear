from tkinter import *
import random
import math

from particleShearBase import CanvasPointsFrictionElasticityLeesEdwards

def dotProduct2(a,b):
    """Helper function for the scalar product of vectors of length 2"""
    return a[0]*b[0]+a[1]*b[1]

class CanvasPointsLinkable (CanvasPointsFrictionElasticityLeesEdwards):
    """Canvas for placing `particleShear.SphereLinkable` objects (referred to as spheres).
          This class maintains a list of objects of type
          `particleShear.SphereLinkable` and adds elementary functions related to crosslinking"""

    def __init__(self, size_x, size_y, theCanvas=FALSE, doDrawing=False,
                 k=1, nu=0.01,m=1,k_t=1,nu_t=0.01,mu=0.1):

        """Initialize self

                                - **parameters**\n
                                    `size_x` Width of area to be used in pixels = micrometers for the simulation\n
                                    `size_y` Height of area to be used in pixels = micrometers for the simulation\n
                                    `theCanvas` possibility to transmit a `tkinter` `Canvas` object for graphical output\n
                                    `doDrawing` Flag to indicate whether graphical output should be produced or not\n
                                    `k` Central spring constant in (mg/s^2)/m of depth;
                                    so F=-k*x*L with L the depth of the stack (the simulation is 2D) and x the compression\n
                                    `nu` Central viscosity force constant in (mg/s)/m of depth. This is to have F=nu*v*L, L again the depth\n
                                    `m` is the mass per unit of depth in mg/m of depth\n
                                    `k_t` Tangential spring constant in (mg/s^2)/m of depth;
                                    relevant for locked or permanent interfaces but not for slipping interfaces\n
                                    `nu_t` Central viscosity force constant in (mg/s)/m of depth.
                                     Relevant for frictionally locked and permanent interfaces but not slipping ones\n
                                    `mu` Friction coefficient, describes the maximum interface force for non-permanent interfaces by
                                    F_tangential_max = F_central*mu"""

        super(CanvasPointsLinkable, self).__init__(
            size_x, size_y, theCanvas=theCanvas, doDrawing=doDrawing,
                 k=k, nu=nu,m=m,k_t=k_t,nu_t=nu_t,mu=mu)


    def particle_info(self):
        """Provide short description of particle type of inclusion into output file

                Method defined in `particleShear.CanvasPointsLinkable` """
        return "CanvasPointsLinkable: Frictional spheres with possible permanent links, Lees Edwards boundary"


    def makeAllLinksPermanent(self):
        """Link all currently touching spheres with permanent links

                        Method defined in `particleShear.CanvasPointsLinkable` """
        for theSphere in self.sphereList:
            for theNeighbor in theSphere.neighbors:
                theSphere.establish_permanent_link(theNeighbor.theSphere)

    def cutLine(self,point,angle):
        """Remove permanent links across a straight line

        - **parameters**\n
            `point` Vector of 2 elements for x and y coordinates of a point on the cut line\n
            `angle` Angle of the cut line, in radians; 0=vertical \n
            Method defined in `particleShear.CanvasPointsLinkable` """
        norm_vector = [math.cos(angle), math.sin(angle)]
        base = dotProduct2(norm_vector,point)

        for theSphere in self.sphereList:
            for theNeighbor in theSphere.neighbors:
                if (theNeighbor.interface_type == "permanent"):
                    myScalar_product = dotProduct2(norm_vector, [theSphere.x, theSphere.y]) - base
                    dist = theSphere.d(theNeighbor.theSphere)
                    n_vector = theSphere.n(theNeighbor.theSphere)
                    neighbor_scalar_product = dotProduct2(norm_vector, [theSphere.x + n_vector[0] * dist,
                                                                      theSphere.y + n_vector[1] * dist]) - base
                    # Crossline means opposite side or cut through one or two of the points
                    if (myScalar_product * neighbor_scalar_product) <= 0:
                        theSphere.cut_permanent_link(theNeighbor.theSphere)

    def cutRandomLine(self):
        """Remove permanent links across a random cut line

            Method defined in `particleShear.CanvasPointsLinkable` """
        point=[random.randint(0,self.size_x), random.randint(0,self.size_y)]
        angle=random.random()* 2 * math.pi
        self.cutLine(point,angle)

    def cutTopBottomEdge(self):
        """Remove permanent links across a top and bottom boundary lines

            Method defined in `particleShear.CanvasPointsLinkable` """
        self.cutLine([0,0],math.pi/2)
        self.cutLine([0, self.size_y], math.pi / 2)







