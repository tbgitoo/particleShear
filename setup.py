from setuptools import setup

setup(name='particleShear',
      version='1.0',
      description='Simulation of frictional and possibly crosslinked particles in shear',
      url='',
      author='Thomas Braschler',
      author_email='thomas.braschler@gmail.com',
      license='MIT',
      packages=['particleShear','particleShearBase','particleShearObjects',
                'particleShearLinkableObjects',
                'particleShearSimulation',
                'particleShearRunSimulation',
                'particleShearTest'],
      install_requires=['Pillow'],
      zip_safe=False,
      test_suite='particleShearTest')