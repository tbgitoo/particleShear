from tkinter import *
import math
from .Force_register import Force_register
from .Graphical_output_configuration import Graphical_output_configuration


class CanvasPoints():
    """Canvas for placing objects of type `particleShear.Point` (or subclasses thereof).

    This class maintains a list of objects of type
    `particleShear.Point` or derived and provides basic functions to handle this collection. These objects are generically
    referred to as spheres and are stored in `particleShear.CanvasPoints.sphereList`.\n
    Class defined in subpackage particleShearBase"""
    def __init__(self, size_x, size_y, theCanvas=False, doDrawing=False):
        """Initialize self

        - **parameters**\n
            `size_x` Width of area to be used in pixels = micrometers for the simulation\n
            `size_y` Height of area to be used in pixels = micrometers for the simulation\n
            `theCanvas` possibility to transmit a `tkinter` `Canvas` object for graphical output\n
            `doDrawing` Flag to indicate whether graphical output should be produced or not"""
        self.theCanvas = theCanvas
        """tkinter canvas for drawing the simulation objects"""
        self.size_x = size_x
        """Width of area to be used in pixels = micrometers for the simulation
        
        Generally, but not strictly necessarily, this is also the width of `particleShear.CanvasPoints.theCanvas`"""
        self.size_y = size_y
        """Height of area to be used in pixels = micrometers for the simulation 
        
        Generally, but not strictly necessarily, this is also the height of `particleShear.CanvasPoints.theCanvas`"""
        self.doDrawing = doDrawing
        """Flag to indicate whether graphical output should be produced or not (boolean)"""
        self.sphereList = []
        """list of objects of type `particleShear.Point` or derived. These objects are referred to as spheres"""
        self.graphical_output_configuration=Graphical_output_configuration() # Default graphical output configuration
        """`particleShear.Graphical_output_configuration` to set options how the spheres and their neighboring relations
        are displayed"""
        self.set_graphical_output_configuration(self.graphical_output_configuration) # To propagate it also to the spheres



    def set_graphical_output_configuration(self, graphical_output_configuration):
        """Set new `particleShear.Graphical_output_configuration`

        This method is defined in class `particleShear.CanvasPoints`"""
        self.graphical_output_configuration=graphical_output_configuration
        for theSphere in self.sphereList:
            theSphere.set_graphical_output_configuration(self.graphical_output_configuration)


    def initiateGraphics(self):
        """Initiate drawing of the constituent sphere objects by invokation of
         `particleShear.Circle.initiate_drawing`.

          For this, the objects need to derive from
         `particleShear.Circle` or otherwise provide a initiate_drawing method. \n
          This method is defined in class `particleShear.CanvasPoints`"""
        if(self.doDrawing):
            for theSphere in self.sphereList:
                theSphere.doDrawing=True
                theSphere.initiate_drawing()


    # For recording incoming force reported by the spheres


    def correct_linear_drift(self):
        """Subtract average linear speed from all constituent sphere objects (of type `particleShear.Point`
        or subclasses thereof)

          This method is defined in class `particleShear.CanvasPoints`"""
        l=0
        vx=0
        vy=0
        for theSphere in self.sphereList:
            vx=vx+theSphere.xspeed
            vy=vy+theSphere.yspeed
            l=l+1
        if l>0:
            vx=vx/l
            vy=vy/l
            for theSphere in self.sphereList:
                theSphere.xspeed=theSphere.xspeed-vx
                theSphere.yspeed = theSphere.yspeed - vy


    def particle_info(self):
        """Return information on the type of particle ensemble used. This information
        can for instance be used to properly document output in files"""
        return "CanvasPoints: Geometrical operations only"

    # To be overriden by subclasses with special boundary conditions

    def canMove(self,theSphere):
        """Return boolean to indicate whether a given sphere (object of type `particleShear.Point`
        or subclass thereof) to move on the current canvas\n
        To be overriden by subclasses of `particleShear.CanvasPoints` with special boundary conditions


        This method is defined in class `particleShear.CanvasPoints`"""
        return True



    def do_linear_acceleration(self, dt):
        """Instruct mobile spheres (objects of type `particleShear.Point` or subclasses thereof) to change their speed depending
        on the forces acting on them. The objects need to to derive from `particleShear.CircleMass` or
        otherwise possess a do_linear_acceleration method


        This method is defined in class `particleShear.CanvasPoints`"""
        for theSphere in self.sphereList:
            if self.canMove(theSphere):
                theSphere.do_linear_acceleration(dt)



    def cool(self, f=0.8):
        """Cool the sphere objects (of type `particleShear.Point` or subclass thereof) by a factor of f;
        for f=0 the objects stop, for f=1 this has no
        effect. For this function to work, the objects need to derive from `particleShear.PointLeesEdwards` or
        otherwise present a cool method

        This method is defined in class `particleShear.CanvasPoints`"""
        for theSphere in self.sphereList:
            theSphere.cool(f)

    def move(self, dt=1):
        """Move the spheres (of type `particleShear.Point` or derived)  during a time period dt (in s)

        This method is defined in class `particleShear.CanvasPoints`"""
        for theSphere in self.sphereList:
            theSphere.move(dt)

    def boundary_conditions(self):
        """Invoke `particleShear.Point.boundary_conditions` routine
        on each of the spheres (of type `particleShear.Point` or subclass)

        This method is defined in class `particleShear.CanvasPoints`"""
        for theSphere in self.sphereList:
            theSphere.boundary_conditions(self.size_x, self.size_y)


    def movableSphereList(self):
        """Return the list of mobile spheres (list of objects of type
        `particleShear.Point` or subclasses thereof); for these mobile objects,
        `particleShear.CanvasPoints.canMove` returns True

        This method is defined in class `particleShear.CanvasPoints`"""
        movable_spheres = []
        for theSphere in self.sphereList:
            if (self.canMove(theSphere)):
                movable_spheres.append(theSphere)
        return movable_spheres



    def regular_sphere_distribution(self,rand_fraction=0.5):
        """Distributes the spheres (objects derived from `particleShear.Point` class or subclasses) in a regular
        rectangular grid on the area defined by `particleShear.CanvasPoints.size_x` * `particleShear.CanvasPoints.size_y`

        - **parameters**\n
            `rand_fraction` allows local random fluctuations of the sphere positions around the grid positions\n
            This method is defined in class `particleShear.CanvasPoints`"""
        N_spheres = len(self.sphereList)

        N_rows = int(round(math.sqrt(N_spheres * self.size_y / self.size_x)))


        total_length_to_distribute = N_rows * (self.size_x)

        length_per_sphere = total_length_to_distribute / N_spheres

        y_spacing = self.size_y / (N_rows + 1)

        total_length_to_distribute = total_length_to_distribute + length_per_sphere

        ni = 0

        for theSphere in self.sphereList:
            current_length_pos = length_per_sphere * ni
            row_index = int(math.floor(current_length_pos / total_length_to_distribute * N_rows))
            col_index = \
                (current_length_pos - row_index * total_length_to_distribute / N_rows) / length_per_sphere
            theSphere.y = row_index * length_per_sphere+(random.random()-0.5)*rand_fraction*length_per_sphere
            theSphere.x = col_index * y_spacing+(random.random()-0.5)*rand_fraction*y_spacing

            ni = ni + 1




