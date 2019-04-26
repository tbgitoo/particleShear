from tkinter import *
import random
import math
from .SphereLinkable import SphereLinkable
from .CanvasPointsLinkable import CanvasPointsLinkable
from particleShearObjects import r_estimate
from particleShearObjects import adjust_m
from particleShearBase import Force_register

class EnsembleLinkable(CanvasPointsLinkable):

    def __init__(self, size_x, size_y, N, packing_fraction=0.8, theCanvas=FALSE, doDrawing=FALSE,
                 k=1, nu=0.01,m=1,
                 bimodal_factor=1.4,
                 k_t=1,nu_t=0.01,mu=0.1):


        super(EnsembleLinkable, self).__init__( size_x, size_y, theCanvas, False,
                                                          k, nu, m,k_t=k_t,nu_t=nu_t,mu=mu)

        self.bimodal_upper = math.sqrt(bimodal_factor)
        self.bimodal_lower = math.sqrt(1 / bimodal_factor)

        self.N = N
        self.packing_fraction = packing_fraction

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
                                                     i, theCanvas, False,self, self.size_x, self.size_y))
        self.setShearInSpheres()
        self.setShearRateInSpheres()

        self.set_graphical_output_configuration(
            self.graphical_output_configuration)  # To propagate it also to the spheres

        self.initiateGraphics()






    def particle_info(self):
        return "Frictional spheres under Lees-Edwards boundary conditions with possible permanent links between neighbors\n" \
               "\tbimodal size distribution, equal probability, \n\tr1="+\
               str(self.r_max*0.8/1.2)+"r2="+str(self.r_max)+"\n\tidentical mass="+str(self.sphereList[0].m)+"mg"

    def random_radius_bimodal(self,r):
        return r*(self.bimodal_lower+(self.bimodal_upper-self.bimodal_lower)*random.randint(0, 1))

