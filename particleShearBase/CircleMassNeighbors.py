from tkinter import *
import random
import math

from .Force_register import Force_register

from .neighbor_relation import neighbor_relation

from .Graphical_output_configuration import Graphical_output_configuration

from .CircleMass import CircleMass

# Basic friction-less sphere with drawing functions
class CircleMassNeighbors(CircleMass):
    """Provide a circle with a neighbor list

       Add capacity to handle the relation to neighboring spheres to the `particleShear.CircleMass` parent class """
    def __init__(self, color, x, y, diameter, m=1, theCanvas=False, doDrawing=False,force_register=Force_register(),
                 use_lees_edwards=False):



        self.neighbors = []
        """The list of neighbors, of class `particleShear.neighbor_relation` (or subclass)"""

        super(CircleMassNeighbors,self).__init__(color,x,y,diameter,m=m, theCanvas=theCanvas, doDrawing=doDrawing,
                                                 force_register=force_register,use_lees_edwards=use_lees_edwards)







    def set_graphical_output_configuration(self, graphical_output_configuration):
        """Set new `particleShear.Graphical_output_configuration`

        This method is defined in class `particleShear.CircleMassNeighbors`"""
        self.deleteNeighborDrawing()
        super(CircleMassNeighbors,self).set_graphical_output_configuration(graphical_output_configuration)
        self.initiateNeighborDrawing()



    def deleteNeighborDrawing(self):
        """Deletes the drawing objects for the neighbor interfaces

        There seems to be no good way to move a line, so deleting and drawing
        is done at every simulation step for the neighbor lines.\n
        This method is defined in class `particleShear.CircleMassNeighbors`"""
        for theNeighbor in self.neighbors:
            if theNeighbor.graphical_line_index!=-1:
                if self.theCanvas:
                    self.theCanvas.delete(theNeighbor.graphical_line_index)
                theNeighbor.graphical_line_index=-1

    def contactLineColor(self,interface_type):
        """Find current contact line color

        Color codes for the interface state; by default, red is locked, green is slipping.
        These settings can be changed in the `particleShear.CircleMassNeighbors.graphical_output_configuration` instance
        variable\n
        This method is defined in class `particleShear.CircleMassNeighbors`"""
        col=self.graphical_output_configuration.color_interface_slip
        if(interface_type == "stick"):
            col=self.graphical_output_configuration.color_interface_locked
        return col


    def initiateNeighborDrawing(self):
        """Generate the graphical representation of the neighboring lines

        This method is defined in class `particleShear.CircleMassNeighbors`"""



        if self.graphical_output_configuration.draw_active_interface:
            for theNeighbor in self.neighbors:
                if not theNeighbor.interface_type=="permanent" or self.graphical_output_configuration.draw_permanent_interfaces:
                    if theNeighbor.graphical_line_index == -1:
                        dist = self.d(theNeighbor.theSphere)
                        # From geometrical considerations: intersection circles with shared height segment
                        # self.r^2-x^2=theNeighbor.theSphere.r^2-(dist-x)^2
                        # self.r^2-x^2+dist^2-2*x*dist+x^2=theNeighbor.theSphere.r^2
                        # self.r^2+dist^2-2*x*dist=theNeighbor.theSphere.r^2
                        # dist^2-2*x*dist=theNeighbor.theSphere.r^2-self.r^2
                        # -dist^2+2*x*dist=self.r^2-theNeighbor.theSphere.r^2
                        # -dist+2*x=(self.r^2-theNeighbor.theSphere.r^2)/dist
                        # x=1/2*(dist+(self.r^2-theNeighbor.theSphere.r^2)/dist)

                        if (dist <= self.r + theNeighbor.theSphere.r) and dist > 0:
                            l = (dist + (
                                        self.r * self.r - theNeighbor.theSphere.r * theNeighbor.theSphere.r) / dist) / 2

                            if self.r * self.r - l * l >= 0:
                                h = math.sqrt(self.r * self.r - l * l)
                                norm_vector = self.n(theNeighbor.theSphere)
                                pos = self.coordinates()
                                touch_point_x = pos[0] + norm_vector[0] * l
                                touch_point_y = pos[1] + norm_vector[1] * l
                                endpoint_1_x = touch_point_x - norm_vector[1] * h
                                endpoint_1_y = touch_point_y + norm_vector[0] * h
                                endpoint_2_x = touch_point_x + norm_vector[1] * h
                                endpoint_2_y = touch_point_y - norm_vector[0] * h
                                color = self.contactLineColor(theNeighbor.interface_type)
                                if self.theCanvas:
                                    theNeighbor.graphical_line_index = self.theCanvas.create_line(
                                        endpoint_1_x,
                                        endpoint_1_y,
                                        endpoint_2_x,
                                        endpoint_2_y,
                                        width=3, fill=color
                                    )

    def moveDrawing(self, dt):
        """Move the drawings associated with this object

        This method is defined in class `particleShear.CircleMassNeighbors`"""
        super(CircleMassNeighbors,self).moveDrawing(dt)
        self.deleteNeighborDrawing()
        self.initiateNeighborDrawing()

    def deleteDrawing(self):
        """Delete the drawings associated with this object

        This method is defined in class `particleShear.CircleMassNeighbors`"""
        self.deleteNeighborDrawing()
        super(CircleMassNeighbors,self).deleteDrawing()



    def test_neighbor_relation(self, theSphere):
        """Test whether a given sphere is a neighbor

        Tests whether or not the sphere is a geometrical neighbor. Depending on the result, update the list of
        `particleShear.CircleMassNeighbors.neighbors`. If necessary, draw or delete the associated shapes.\n
        This method is defined in class `particleShear.CircleMassNeighbors`"""
        if abs(self.y-theSphere.y) > self.r+theSphere.r and abs(self.y-theSphere.y)< self.size_y-self.r-theSphere.r:
            is_neighbor=False
        else:
            d = self.d(theSphere)
            pos = theSphere.coordinates()
            r = pos[2]
            is_neighbor = (d < r + self.r)


        # Regardless of the distance, first check whether we find the sphere in the neighbors list
        found = FALSE
        foundNeighborIndex=-1
        for theNeighborIndex in range(len(self.neighbors)):
            theNeighbor = self.neighbors[theNeighborIndex]
            if (theSphere == theNeighbor.theSphere):
                foundNeighborIndex = theNeighborIndex
                found = TRUE

        if not is_neighbor: #If the sphere is not a neighbor (anymore)
            if found: #It was previously a neighbor, but no more, so delete it from the neighbors list
                if self.doDrawing:
                    self.deleteNeighborDrawing()
                del self.neighbors[foundNeighborIndex]
                if self.doDrawing:
                    self.initiateNeighborDrawing()
        if is_neighbor:
            if not found: # Not found previously, so add a new entry
                info = neighbor_relation(0,"stick",theSphere)
                if self.doDrawing:
                    self.deleteNeighborDrawing()
                self.neighbors.append(info)
                if self.doDrawing:
                    self.initiateNeighborDrawing()



    def findNeighborIndex(self, theSphere):
        """Return whether theSphere is among the currently listed `particleShear.CircleMassNeighbors.neighbors`"""

        foundNeighborIndex = -1
        for theNeighborIndex in range(len(self.neighbors)):
            theNeighbor = self.neighbors[theNeighborIndex]
            if (theSphere == theNeighbor.theSphere):
                foundNeighborIndex = theNeighborIndex

        return foundNeighborIndex