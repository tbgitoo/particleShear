from tkinter import *
import random
import math
from particleShearObjects import SphereFrictionLeesEdwards
from .neighbor_relation_linkable import neighbor_relation_linkable
from particleShearBase import Force_register
from particleShearBase import CircleBasicElasticity
from math import exp


def elastic_force_law_tensile(d, d0, k):
    return -k * (d0 - d)

def elastic_force_law_tensile_exponential(d, d0, k):
    return k*(1-exp(-(d-d0)/d0/TensileConfiguration.d_exponential))*d0*TensileConfiguration.d_exponential






class TensileConfiguration():
    """ Class to define alternative tensile force laws, not used by default"""

    d_exponential=0.2


class SphereLinkable(SphereFrictionLeesEdwards):
    call_back_elastic_force_law_tensile = elastic_force_law_tensile


    def __init__(self, color, x, y, diameter, m=1,my_index=1, theCanvas=FALSE, doDrawing=FALSE,
                 force_register=Force_register(),size_x=500,size_y=500):
        super(SphereLinkable,self).__init__(color, x, y, diameter, m,my_index, theCanvas, doDrawing,force_register,size_x,size_y)


    def cut_permanent_link(self,theSphere,do_backlink=True):
        foundNeighborIndex = self.findNeighborIndex(theSphere)

        if foundNeighborIndex >= 0:
            theNeighbor = self.neighbors[foundNeighborIndex]
            if theNeighbor.interface_type=="permanent":

                theNeighbor.equilibrium_distance = 0
                theNeighbor.friction_position = 0
                theNeighbor.interface_type = "slip"

                # Link back from the neighbor
                if do_backlink:
                    theNeighbor.theSphere.cut_permanent_link(self, do_backlink=False)
                if self.doDrawing:
                    self.initiateNeighborDrawing()

    def establish_permanent_link(self,theSphere,do_backlink=True):
        foundNeighborIndex = self.findNeighborIndex(theSphere)

        if foundNeighborIndex>=0:
            theNeighbor = self.neighbors[foundNeighborIndex]
            theNeighbor.equilibrium_distance=self.r+theNeighbor.theSphere.r
            theNeighbor.friction_position=0
            theNeighbor.interface_type="permanent"

            # Link back from the neighbor
            if do_backlink:
                theNeighbor.theSphere.establish_permanent_link(self,do_backlink=False)
            if self.doDrawing:

                self.initiateNeighborDrawing()

        else:
            info = neighbor_relation_linkable(0, "permanent", theSphere)
            info.equilibrium_distance=self.r+theSphere.r
            info.friction_position = 0



            if self.doDrawing:
                self.deleteNeighborDrawing()
            self.neighbors.append(info)

            if do_backlink:
                theSphere.establish_permanent_link(self,do_backlink=False)


            if self.doDrawing:
                self.initiateNeighborDrawing()

    def permanentlyConnectedSpheres(self,physical_neighbors_only=True):
        connected=[]
        for theNeighbor in self.neighbors:
            if theNeighbor.interface_type=="permanent" and not connected.count(theNeighbor.theSphere):
                if physical_neighbors_only: # Additional check for physical proximity
                    if abs(theNeighbor.theSphere.x-self.x)<self.size_x*0.5 and abs(theNeighbor.theSphere.y-self.y)<self.size_y*0.5:
                        connected.append(theNeighbor.theSphere)
        return connected








    def test_neighbor_relation(self, theSphere):
        d = self.d(theSphere)
        pos = theSphere.coordinates()
        r = pos[2]
        is_neighbor=(d < r + self.r)
        # Regardless of the distance, first check whether we find the sphere in the neighbors list
        found = FALSE
        foundNeighborIndex=-1
        for theNeighborIndex in range(len(self.neighbors)):
            theNeighbor = self.neighbors[theNeighborIndex]
            if (theSphere.myindex == theNeighbor.myindex):
                foundNeighborIndex = theNeighborIndex
                found = TRUE

        if not is_neighbor: #If the sphere is not a neighbor (anymore)
            if found: #It was previously a neighbor, but no more, so delete it from the neighbors list if possible
                if not self.neighbors[foundNeighborIndex].interface_type=="permanent":
                    if self.doDrawing:
                        self.deleteNeighborDrawing()
                    del self.neighbors[foundNeighborIndex]
                    if self.doDrawing:
                        self.initiateNeighborDrawing()

        if is_neighbor:
            if not found: # Not found previously, so add a new entry
                info = neighbor_relation_linkable(0,"stick",theSphere)
                if self.doDrawing:
                    self.deleteNeighborDrawing()
                self.neighbors.append(info)
                if self.doDrawing:
                    self.initiateNeighborDrawing()



    def deleteNeighborDrawing(self):
        super(SphereLinkable,self).deleteNeighborDrawing()
        for theNeighbor in self.neighbors:
            if theNeighbor.linking_line_index!=-1:
                if self.theCanvas:
                    self.theCanvas.delete(theNeighbor.linking_line_index)
                theNeighbor.linking_line_index=-1

    def initiateNeighborDrawing(self):
        super(SphereLinkable, self).initiateNeighborDrawing()
        for theNeighbor in self.neighbors:
            if theNeighbor.linking_line_index==-1:
                if theNeighbor.interface_type == "permanent":
                    # To correctly draw under periodic boundary conditions we need to use the joining vector and distance
                    # rather than raw coordinates
                    dist=self.d(theNeighbor.theSphere)
                    n_vector = self.n(theNeighbor.theSphere)
                    if self.theCanvas:
                        theNeighbor.linking_line_index = self.theCanvas.create_line(
                            self.x,
                            self.y,
                            self.x + n_vector[0] * dist,
                            self.y + n_vector[1] * dist,
                            width=3, fill="blue"
                        )

    # Here, permanent and transient interfaces behave the same. This is not necessarily true for subclasses
    def tangential_force_viscous_permanent(self,theSphere,nu):
        return self.tangential_force_viscous(theSphere,nu)



    def tangential_force(self, theSphere, nu,mu,k,k_t):
        d = self.d(theSphere)
        pos = theSphere.coordinates()
        r = pos[2]

        foundNeighborIndex=self.findNeighborIndex(theSphere)

        found = foundNeighborIndex >= 0

        isPermanent = False






        if found:

            # Check whether symmetric backlink exists

            backlink=self.neighbors[foundNeighborIndex].theSphere.findNeighborIndex(self)

            if(not backlink>=0):
                print("SphereLinkable: Asymmetric neighbor problem")



            if self.neighbors[foundNeighborIndex].interface_type == "permanent":
                isPermanent = True



        if d < r + self.r or isPermanent:


            if not found:
                print("tangential_force: Problem with neighbors, found touching sphere not in neighbors list")
                return




            if isPermanent:
                viscous_force=self.tangential_force_viscous_permanent(theSphere,nu)
                if abs(viscous_force - theSphere.tangential_force_viscous_permanent(self, nu)) > 1e-15:
                    print("viscous force mis-match", viscous_force - theSphere.tangential_force_viscous_permanent(self, nu))

            else:
                viscous_force=self.tangential_force_viscous(theSphere,nu)
                if abs(viscous_force - theSphere.tangential_force_viscous(self, nu)) > 1e-15:
                    print("viscous force mis-match", viscous_force - theSphere.tangential_force_viscous(self, nu))












            if isPermanent:
                elastic_force=self.tangential_force_elastic_permanent(theSphere,k_t)
            else:
                elastic_force=self.tangential_force_elastic(theSphere,k_t)






            total_adherence_force = viscous_force+elastic_force
            friction_force=self.get_elastic_force(theSphere, k)*mu






            sig=1
            if(total_adherence_force<0):
                sig=-1

            if(abs(total_adherence_force)<=abs(friction_force)):
                if not isPermanent:
                    self.neighbors[foundNeighborIndex].interface_type="stick"
                    theSphere.neighbors[backlink].interface_type = "stick"
            else:
                if not isPermanent:
                    self.neighbors[foundNeighborIndex].interface_type = "slip"
                    self.neighbors[foundNeighborIndex].friction_position=0
                    theSphere.neighbors[backlink].interface_type = "slip"
                    theSphere.neighbors[backlink].friction_position = 0
            if isPermanent:
                force=abs(total_adherence_force)
            else:
                force=min(abs(total_adherence_force),abs(friction_force))



            force=force*sig

            # The idea here is that the same friction point will be visited again when the neighboring sphere is examined,
            # so we assign only half the force here
            # The distribution is a bit complicated because of the conservation of angular momentum, so we use a dedicated function
            self.distribute_tangential_couple(theSphere, force/2)


    def tangential_force_elastic_permanent(self, theSphere, k_t):
        found = False
        foundNeighborIndex = -1
        for theNeighborIndex in range(len(self.neighbors)):
            theNeighbor = self.neighbors[theNeighborIndex]
            if (theSphere == theNeighbor.theSphere and theNeighbor.interface_type=="permanent"):
                foundNeighborIndex = theNeighborIndex
                found = TRUE
        if not found:
            print("Problem with neighbors, found permanent touching sphere not in neighbors list")
        else:

            return k_t * self.neighbors[foundNeighborIndex].friction_position

    def elastic_force(self, theSphere, k):



        foundNeighborIndex = self.findNeighborIndex(theSphere)

        if(foundNeighborIndex>=0):
            if(self.neighbors[foundNeighborIndex].interface_type != "permanent"):
                super(SphereLinkable,self).elastic_force(theSphere,k)
                return

        # So, we have a permanent neighbor here with a known equilibrium position

        d = self.d(theSphere)
        pos = theSphere.coordinates()
        r = pos[2]

        force = self.get_elastic_force_permanent(theSphere,k)

        n_vector = self.n(theSphere)

        self.xforce = self.xforce + force * n_vector[0]
        self.yforce = self.yforce + force * n_vector[1]


        self.force_register.record_individual_internal_force(self,theSphere,[force * n_vector[0], force * n_vector[1]])



    def get_elastic_force_permanent(self,theSphere,k=1):




        d = self.d(theSphere)

        foundNeighborIndex = self.findNeighborIndex(theSphere)

        if(foundNeighborIndex<0):
            print("Could not find supposedly permanent neighbor")
            return 0

        equilibrium_distance = self.neighbors[foundNeighborIndex].equilibrium_distance

        if d>=equilibrium_distance:

            return SphereLinkable.call_back_elastic_force_law_tensile(d, equilibrium_distance, k)




        return CircleBasicElasticity.call_back_elastic_force_law(d, equilibrium_distance, k, self.central_repulsion_coefficient)












    def contactLineColor(self,interface_type):
        col="green"
        if(interface_type == "stick" or interface_type == "permanent"):
            col="red"
        return col




