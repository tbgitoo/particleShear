from tkinter import *
import random
import math
from .SphereLinkable import SphereLinkable
from .neighbor_relation_linkable import neighbor_relation_linkable
from particleShearBase import Force_register



class SphereLinkableAdjustableInterfaceStrength(SphereLinkable):
    def __init__(self, color, x, y, diameter, m=1,my_index=1, theCanvas=FALSE, doDrawing=FALSE,
                 force_register=Force_register(),size_x=500,size_y=500,permanent_ratio_central=1,permanent_ratio_tangential=1,
                 keep_viscosity_coefficients_constant=True):

        # The idea is here that we specifically modify the permanent links to have mechanical properties that can be different
        # from the purely frictional ones

        self.permanent_ratio_central=permanent_ratio_central
        self.permanent_ratio_tangential=permanent_ratio_tangential

        self.keep_viscosity_coefficients_constant=keep_viscosity_coefficients_constant





        super(SphereLinkableAdjustableInterfaceStrength,self).__init__(
            color, x, y, diameter, m,my_index, theCanvas, doDrawing,force_register,size_x,size_y)



    def tangential_force_elastic_permanent(self, theSphere, k_t):
        #print("tangential_force_elastic_permanent", k_t,self.permanent_ratio_tangential)
        return super(SphereLinkableAdjustableInterfaceStrength,self).\
            tangential_force_elastic_permanent(theSphere, k_t)*self.permanent_ratio_tangential

    def tangential_force_viscous_permanent(self, theSphere, nu):
        if(self.keep_viscosity_coefficients_constant):
            return super(SphereLinkableAdjustableInterfaceStrength, self).tangential_force_viscous_permanent(theSphere, nu)
        #print("tangential_force_viscous_permanent",self.permanent_ratio_tangential)
        return super(SphereLinkableAdjustableInterfaceStrength, self). \
                   tangential_force_viscous_permanent(theSphere, nu) * self.permanent_ratio_tangential


    def get_elastic_force_permanent(self,theSphere,k=1):
        #print("get_elastic_force_permanent",k,self.permanent_ratio_central)
        return super(SphereLinkableAdjustableInterfaceStrength, self). \
                   get_elastic_force_permanent(theSphere, k)*self.permanent_ratio_central


    def get_central_viscous_force(self, theSphere, nu):



        foundNeighborIndex = self.findNeighborIndex(theSphere)

        if(self.keep_viscosity_coefficients_constant):
            return super(SphereLinkableAdjustableInterfaceStrength, self).get_central_viscous_force(theSphere, nu)



        if (foundNeighborIndex >= 0):
            if (self.neighbors[foundNeighborIndex].interface_type != "permanent"):
                return super(SphereLinkableAdjustableInterfaceStrength, self).get_central_viscous_force(theSphere, nu)
            else:
                return super(SphereLinkableAdjustableInterfaceStrength, self).get_central_viscous_force(theSphere, nu)*\
                    self.permanent_ratio_central

        return super(SphereLinkableAdjustableInterfaceStrength, self).get_central_viscous_force(theSphere, nu)



    def contactLineColor(self,interface_type):
        col="green"
        if(interface_type == "stick" ):
            col="red"
        if (interface_type == "permanent" ):
            col = "darkorange"
        return col




