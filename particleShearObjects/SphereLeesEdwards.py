from tkinter import *
import random
import math

from particleShearBase import neighbor_relation
from particleShearBase import CircleBasicElasticity

from particleShearBase import Force_register

# Recognition across period boundary conditions with shear displacement
class SphereLeesEdwards(CircleBasicElasticity):
    """Objects of type `particleShear.CircleBasicElasticity`, using periodic Lees-Edwards
            boundary conditions"""
    def __init__(self, color, x, y, diameter, m=1, myindex=1,theCanvas=FALSE, doDrawing=FALSE,
                 force_register=Force_register(),size_x=500,size_y=500):
        """Constructor as `particleShearBase.CircleBasicElasticity.__init__` but with use_lees_edwards set to True
               and indexing element (my_index)."""


        super(SphereLeesEdwards, self).__init__(color, x, y, diameter, m, theCanvas, doDrawing,force_register,
                                                use_lees_edwards=True)
        self.size_x=size_x
        self.size_y=size_y
        self.myindex = my_index






