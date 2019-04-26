
class neighbor_relation():
    """Provide information on the relation to a neighboring spheres

    Defined in subpackage particleShearBase"""
    def __init__(self,friction_position,interface_type,theSphere,graphical_line_index=-1):
        self.myindex=0
        """Identification among the neighbors of a given sphere"""
        if hasattr(theSphere, "myindex"):
            self.myindex=theSphere.myindex
        self.friction_position=friction_position
        """Relative movement position of the interface
         
         See Eq. 7 in Otsuki, M. and H. Hayakawa, 
        Discontinuous change of shear modulus for frictional jammed granular materials. 
        Phys Rev E, 2017. 95(6-1): p. 062902. The friction position changes when relativement movement occurs for 
        locked spheres to account for elastic interaction in the locked state"""
        self.interface_type=interface_type
        """State of the interface, should be "stick", "slip", or permanent (in `particleShear.neighbor_relation_linkable`)  """
        self.theSphere = theSphere
        """Reference to the neighboring sphere"""
        self.graphical_line_index=graphical_line_index
        """Index on the Tkinter canvas of the line corresponding to the interface"""

