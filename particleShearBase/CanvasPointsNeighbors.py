from tkinter import *
import random
import math
from .Force_register import Force_register
from .Graphical_output_configuration import Graphical_output_configuration
from .CanvasPointsMass import CanvasPointsMass


class CanvasPointsNeighbors(CanvasPointsMass):
    """Canvas for placing `particleShear.CircleMassNeighbors` objects (referred to as spheres).
           This class maintains a list of objects of type
           `particleShear.CircleMassNeighbors` or derived and adds basic functions to handle this collection"""

    def __init__(self, size_x, size_y, theCanvas=False, doDrawing=False, m=1):

        super(CanvasPointsNeighbors,self).__init__(size_x=size_x,size_y=size_y,theCanvas=theCanvas,doDrawing=doDrawing,m=m)




    def particle_info(self):
        return "CanvasPointsNeighbors: particles with mass and detection of geometric neighbors"

    def test_neighbor_relation(self):
        """Instruct every sphere to test establish its geometric (and possibly permanent) neighbors.

        This function calls `particleShear.CircleMassNeighbors.test_neighbor_relation` on each member of the
        `particleShear.CanvasPoints.sphereList`.\n
         This method is defined in class `particleShear.CanvasPointsNeighbors`"""
        for sphereIndex in range(len(self.sphereList)):
            for sphereIndex2 in range(len(self.sphereList)):

                if sphereIndex != sphereIndex2:
                    self.sphereList[sphereIndex].test_neighbor_relation(
                        self.sphereList[sphereIndex2]
                    )








