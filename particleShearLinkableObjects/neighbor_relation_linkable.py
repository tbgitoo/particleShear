from particleShearBase import neighbor_relation


# Object holding the information to the neighboring spheres
class neighbor_relation_linkable(neighbor_relation):
    def __init__(self,friction_position,interface_type,theSphere,graphical_line_index=-1,linking_line_index=-1):
        super(neighbor_relation_linkable,self).__init__(friction_position,interface_type,theSphere,
                                                        graphical_line_index=graphical_line_index)
        self.linking_line_index = linking_line_index  # -1 is for no linking line yet
        self.equilibrium_distance=0


