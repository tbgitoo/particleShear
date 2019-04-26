from tkinter import *
import random
import math
from particleShearBase import CircleFrictionElasticity
from particleShearBase import Force_register

class SphereFrictionLeesEdwards(CircleFrictionElasticity):
     """Objects of type `particleShear.CircleFrictionElasticity` , using the periodic Lees-Edwards boundary conditions"""
     def __init__(self, color, x, y, diameter, m=1,my_index=1, theCanvas=FALSE, doDrawing=FALSE,
                 force_register=Force_register(),
                 size_x=500,size_y=500):
        """Constructor as `particleShear.CircleFrictionElasticity.__init__` in `particleShear.CircleFrictionElasticity`
        but with and indexing element (my_index) and with the parameter use_lees_edwards set to True"""
        super(SphereFrictionLeesEdwards,self).__init__(color, x, y, diameter, m, theCanvas, doDrawing,force_register,
                                                       use_lees_edwards=True)


        self.use_lees_edwards=True
        self.myindex = my_index  # To give a unique index
        self.size_x=size_x
        self.size_y=size_y












