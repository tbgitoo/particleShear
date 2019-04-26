
# Basic friction-less sphere with drawing functions
class Graphical_output_configuration:
    """Provide configuration options for graphical output

    `particleShear.Graphical_output_configuration` objects are used to configure graphical representation of
     the spheres (class `particleShear.Circle` and derived).\n
     Sub-package particleShearBase
     """


    def __init__(self, draw_spheres_as="spheres",color_spheres_volume="grey",color_spheres_boundary="green",
                 draw_rotation_line=False, color_rotation_line="black",
                 draw_active_interface=True,color_interface_locked="red",color_interface_slip="green",
                 draw_permanent_connections=True,color_permanent_connections="blue",
                 draw_permanent_interfaces=False,
                 draw_volume_forces=False,color_volume_forces="darkorchid",
                 draw_boundary_forces=False,color_boundary_forces="darkorchid",
                 force_scale=1000,
                 draw_speeds=False,color_speeds="black"):
        """Initialization"""

        self.draw_spheres_as = draw_spheres_as
        """ Display of the spheres. Can be "spheres", "dots" or "none", 
        setting used by the spheres (Class `particleShear.Circle` and derived)"""
        self.color_spheres_volume = color_spheres_volume # Can be any valid python color, used by the spheres
        """  Drawing color of the spheres. 
        Can be any valid python color, used by the spheres (Class `particleShear.Circle` and derived)"""
        self.color_spheres_boundary = color_spheres_boundary # Can be any valid python color, used by the spheres
        """  Drawing color of the spheres on boundary. Not currently implemented. 
                Can be any valid python color, to be used by the spheres (Class `particleShear.Circle` and derived)"""
        self.draw_rotation_line = draw_rotation_line
        """ Boolean, indicates whehter the spheres to display rotation status (`particleShear.SphereFriction` and derived) """
        self.color_rotation_line = color_rotation_line # Can be any valid python color, used by the spheres
        """ Python color, indicates color for the rotation line (`particleShear.SphereFriction` and derived) """
        self.draw_active_interface = draw_active_interface
        """ Boolean, indicates whether currently active `particleShear.neighbor_relation`s should be shown 
        graphically. Used by the spheres 
        (`particleShear.CircleMassNeighbors` and derived)"""
        self.color_interface_locked = color_interface_locked
        """ Can be any valid python color, used by the spheres (`particleShear.CircleMassNeighbors` and derived). This 
        indicates the color for representation of the locked `particleShear.neighbor_relation`s"""
        self.color_interface_slip = color_interface_slip
        """ Can be any valid python color, used by the spheres (`particleShear.CircleMassNeighbors` and derived). This 
                indicates the color for representation of the locked `particleShear.neighbor_relation`s"""
        self.draw_permanent_connections = draw_permanent_connections
        """Boolean,  indicates to the spherees (`particleShear.SphereLinkable` and derived) whether permanent connections 
        should be drawn"""
        self.draw_permanent_interfaces=draw_permanent_interfaces
        """Boolean,  indicates to the spherees (`particleShear.SphereLinkable` and derived) whether the interfaces active 
        for the permanent connections should be drawn"""

        self.color_permanent_connections = color_permanent_connections
        """Valid Python color for the permanent connections, drawn from center to center
         """
        self.draw_volume_forces = draw_volume_forces
        """Boolean, used by `particleShear.StressTensorEvaluation` to show final forces on the
                non-constrained, totally interior spheres"""

        self.color_volume_forces = color_volume_forces
        """Any valid python color, used by `particleShear.StressTensorEvaluation`
         to show final forces on the non-constrained, interior spheres"""
        self.draw_boundary_forces = draw_boundary_forces
        """ Boolean, used by `particleShear.StressTensorEvaluation` to show final forces applied
            on the non-constrained spheres partially in contact with the constrained
            boundary spheres"""
        self.color_boundary_forces = color_boundary_forces
        """ Python color, used by `particleShear.StressTensorEvaluation` to show final forces applied
            on the non-constrained spheres partially in contact with the constrained
            boundary spheres"""
        self.force_scale = force_scale
        """ To graphically scale the forces to have reasonable length """
        self.draw_speeds = draw_speeds
        """Boolean, indicates whether spheres should draw their speed as vectors"""
        self.color_speeds = color_speeds
        """Python color, used by the spheres for the color of the speed vector"""

