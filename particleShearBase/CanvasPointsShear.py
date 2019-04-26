from .CanvasPointsNeighbors import CanvasPointsNeighbors

class CanvasPointsShear(CanvasPointsNeighbors):
    """Canvas for placing `particleShear.CircleMassNeighbors` objects (referred to as spheres).
               This class maintains a list of objects of type
               `particleShear.CircleMassNeighbors` or derived and adds specific functionality linked to shear under
               Lees-Edwards boundary conditions"""

    def __init__(self, size_x, size_y, theCanvas=False, doDrawing=False,m=1):



        super(CanvasPointsShear,self).__init__(size_x=size_x,size_y=size_y,theCanvas=theCanvas,doDrawing=doDrawing,m=m)


        self.t=0
        """Record time while applying shear"""

        self.applyingShear = False
        """Are we currently applying a shear protocol? 
        
        Advance time only if True"""
        self.shear_rate = 0
        """Current shear rate (relative, so 1/s)"""
        self.shear = 0
        """Current applied shear (relative, so dimension-less)"""
        self.use_lees_edwards=True
        """Flag to indicate whether or not we use Lees-Edwards boundary conditions"""





    def canMove(self, theSphere):
        """Indicate whether a given sphere (object of type `particleShear.Point`
        or subclass thereof) to move on the current canvas


        This is for appyling boundary conditions where the movement is imposed externally on the top and lower edge.
        In this case all spheres can move except for in specified shear experiments where
        `particleShear.CanvasPointsShear.applyingShear` is set True\n
           This method is defined in class `particleShear.CanvasPointsShear`"""
        if not self.applyingShear:
            return True
        pos = theSphere.coordinates()
        # Spheres touching the upper and lower boundaries are attached to these boundaries and therefore immobilized
        return pos[1] > pos[2] and pos[1] < self.size_y - pos[2]


    def particle_info(self):
        return "CanvasPointsShear: Points with mass, neighbor detection and shear"



    def do_linear_acceleration(self, dt):
        """Instruct mobile spheres (objects of type `particleShear.Point` or subclasses thereof) to change their speed depending
        on the forces acting on them.

        The objects need to to derive from `particleShear.CircleMass` or
        otherwise possess a do_linear_acceleration method. In addition to its parent method
        (`particleShear.CanvasPoints.do_linear_acceleration` of class `particleShear.CanvasPoints`),
        this method imposes the local speed given by the
        current `particleShear.CanvasPointsShear.shear_rate` at the top and lower boundary to the immobile spheres



        This method is defined in class `particleShear.CanvasPointsShear`"""
        super(CanvasPointsShear,self).do_linear_acceleration(dt)
        for theSphere in self.sphereList:
            if not self.canMove(theSphere):

                pos = theSphere.coordinates()
                theSphere.yspeed = 0
                if pos[1] > self.size_y / 2:
                    theSphere.xspeed = self.shear_rate * self.size_y / 2
                else:
                    theSphere.xspeed = -self.shear_rate * self.size_y / 2

    def transmit_lees_edwards_parameters(self, theSphere):
        """Transmit the parameters pertaining to the Lees-Edwards boundary conditions to the spheres.

        If `particleShear.CanvasPointsShear.use_lees_edwards` is set to True, transmit the instance variables regarding
        canvas size (`particleShear.CanvasPoints.size_x`,`particleShear.CanvasPoints.size_y`), and shear regime
        (`particleShear.CanvasPointsShear.shear`,`particleShear.CanvasPointsShear.shear_rate`,
        `particleShear.CanvasPointsShear.use_lees_edwards`) to the given target sphere.
         Else, only set the `particleShear.PointLeesEdwards.use_lees_edwards` field in the
          target sphere to False\n
         This method is defined in class `particleShear.CanvasPointsShear`"""
        if self.use_lees_edwards:
            theSphere.size_x = self.size_x
            theSphere.size_y = self.size_y
            theSphere.shear_rate = self.shear_rate
            theSphere.shear = self.shear
            theSphere.use_lees_edwards = self.use_lees_edwards
        else:
            if hasattr(theSphere, "use_lees_edwards"):
                theSphere.use_lees_edwards = False
        return theSphere






