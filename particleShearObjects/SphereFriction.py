from tkinter import *
import random
import math
from .Sphere import Sphere
from particleShearBase import Force_register
from particleShearBase import CircleFrictionElasticity

class SphereFriction(CircleFrictionElasticity):
    """Objects of type `particleShear.CircleFrictionElasticity`, using standard rather than periodic Lees-Edwards
    boundary conditions"""
    def __init__(self, color, x, y, diameter, m=1,my_index=1, theCanvas=FALSE, doDrawing=FALSE,force_register=Force_register()):
        """Constructor as `particleShear.CircleFrictionElasticity.__init__` in `particleShear.CircleFrictionElasticity`
        but with and indexing element (my_index) and
        with the parameter use_lees_edwards set to False"""
        super(SphereFriction, self).__init__(color, x, y, diameter, m,  theCanvas, doDrawing, force_register,
                                             use_lees_edwards=False)


        self.myindex = my_index  # To give a unique index







