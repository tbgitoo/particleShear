from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='particleShear',
      version='1.0',
      description='Simulation of frictional and possibly crosslinked particles in shear',
      url='https://github.com/tbgitoo/particleShear',
      author='Thomas Braschler',
      author_email='thomas.braschler@unige.ch',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['particleShear','particleShearBase','particleShearObjects',
                'particleShearLinkableObjects',
                'particleShearSimulation',
                'particleShearRunSimulation',
                'particleShearTest'],
      install_requires=['Pillow'],
      zip_safe=False,
      test_suite='particleShearTest',
      project_urls={
          "Bug Tracker": "https://github.com/tbgitoo/particleShear/issues"
      },
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Operating System :: OS Independent",
      ]
      )