from .Ensemble import r_estimate
import math

class particle_shear_model_parameters():
    """Model class to facilitate calculation of particle and simulation parameters from physical properties of the
        constituent spheres

        Class defined in subpackage particleShearObjects"""
    def __init__(self,size_x=500,size_y=500,N=100,packing_fraction=1,Young_modulus_spheres=10000,density=50,
                 bimodal_factor=1):
        """Initialize model

        Parameters\n
        `size_x` Width of area to be used in pixels = micrometers for the simulation\n
        `size_y` Height of area to be used in pixels = micrometers for the simulation\n
        `N` The number of spheres to place\n
        `packing_fraction` The packing fraction indicating the density; this is defined as the area occupied by the
         non-compressed spheres as compared to the actual available area (size_x times size_y)\n
         `Young_modulus_spheres` The Young modulus of the constituent spheres in Pa\n
         `density of the spheres in kg/m^3\n`
         `bimodal_factor` is ratio of radii of the smaller and larger spheres in the bimodal distribution
          """

        self.bimodal_factor=bimodal_factor
        """Bimodal factor indicating the ratio between the larger and the smaller spheres (bimodal size distribution)"""
        self.size_x=size_x
        """Width of the simulation area in micrometers (=Pixels) """
        self.size_y=size_y
        """Height of the simulation area in micrometers (=Pixels) """
        self.size_x_m=size_x/1e6 # Pixel units are micrometers
        """Width of the simulation area in meters """
        self.size_y_m=size_y/1e6 # Pixel units are micrometers
        """Height of the simulation area in meters """
        self.N=N
        """Number of spheres"""
        self.packing_fraction=packing_fraction
        """Packing fraction: relative area occupied by the uncompressed spheres as compared to the available area"""
        self.r=r_estimate(self.size_x,self.size_y,self.packing_fraction,self.N,
                          bimodal_upper=math.sqrt(bimodal_factor),bimodal_lower=1/math.sqrt(bimodal_factor))
        """Average radius in micrometers.
        
        The radius is defined such that the larger radius would be sqrt(bimodal_factor)*radius and the smaller
        1/sqrt(bimodal_factor)*radius. The expected packing fraction is conserved by adjusting for the increase in 
        average cross section area resulting from the use of a bimodal distribution"""
        self.r_m=self.r/1e6 # Pixel units are micrometers
        """Average radius in meters"""
        self.m=math.pi*self.r_m*self.r_m*density*1e6 #This is per m of depth for the cylinders; the mass is converted to mg/m
        """Average mass per particle, in mg/m (cylindrical particles shown in cross section, mass per m of cylinder depth)"""

        self.Young_modulus_spheres = Young_modulus_spheres
        """Young modulus of the constituent spheres; this is of the material of which the spheres are made, in general, 
        the ensemble would be softer"""
        self.density=density
        """Density of the particles, in kg/m^3"""

        self.k=math.pi/8*Young_modulus_spheres*1e6
        """Spring constant, in mg/s^2/m; this relates the force per unit length to the indentation depth.
        
        The formula used is pi/8*Young_modulus spheres; this is eq. 5.34 from Popov, V.L, 
        Contact Mechanics and Friction: Physical Principles and Applications, Berlin, Germany, 
        2017, 2nd edition (DOI 10.1007/978-3-662-53081-8), with an effective modulus given by 
         E*=E/2 from eq. 5.26 also in Popov's contact mechanics book. We neglect here the effect of the 
          Poisson coefficient (i.e. we assume Poisson coefficient=0), this introduces at worst 25% error"""


        self.time_constant=math.sqrt(self.m/self.k)/math.sqrt(max(bimodal_factor,1/bimodal_factor))
        """Characteristic time constant sqrt(m/k)
        
        
        Here, the expressions of k and m in per m of depth cancels out
        Also, regarding a possible bimodal distribution (bimodal_factor>1), we err on the side of caution
        If a bimodal distribution is provided, then, the smaller radius will be r/sqrt(bimodal_factor), and so the mass
        will be m/bimodal_factor. That makes the time constant smaller, by sqrt(bimodal_factor). To be sure against
        indication of bimodal factor < 1, use the maximum of (bimodal_factor, 1/bimodal_factor)
        """
