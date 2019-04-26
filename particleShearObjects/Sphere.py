
from particleShearBase import Force_register

from particleShearBase import CircleBasicElasticity

# Basic friction-less sphere with drawing functions
class Sphere(CircleBasicElasticity):
    """Objects of type `particleShear.CircleBasicElasticity`, using standard rather than periodic Lees-Edwards
        boundary conditions"""
    def __init__(self, color, x, y, diameter, m=1,my_index=1,theCanvas=False, doDrawing=False,force_register=Force_register()):
        """Constructor as `particleShearBase.CircleBasicElasticity.__init__` but with use_lees_edwards set to False
        and indexing element (my_index)."""

        super(Sphere,self).__init__(color,x,y,diameter,m=m, theCanvas=theCanvas, doDrawing=doDrawing,force_register=force_register,
                                    use_lees_edwards=False)

        self.myindex=my_index # To give a unique index






