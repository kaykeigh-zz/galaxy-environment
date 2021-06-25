# Building an environmental catalog for galaxies

**Author**: Kayleigh Meneghini | **Email**: kayleighmeneghini@gmail.com

## How to use

This package is available on PyPi.

For more details, please check this [tutorial](https://github.com/kaykeigh/galaxy-environment/blob/master/tutorial/Tutorial.ipynb)

```
# installation
pip install galaxy-environment

# import 
from galaxy_environment import environment
```

## Introduction 
How much the environment affects galaxies is still part of the unknown, as some results are discrepant depending on the sample selection, according to Lai
et al. (2016), such as the chosen magnitude or velocity dispersion limit for sample.

Furthermore, the very definition of environment makes this type of study not trivial, after all *how to define the environment*? 
We can consider the local environment, such as the associated with a central galaxy and its satellites, or on larger scales such as those associated
to groups and clusters. 

According to Muldrew et al. (2012), there are two wide methods used to define the galactic environment, these are: **Nearest Neighbors and Fixed Apertures**.

In this package I have implemented the calculation of environmental estimators by these two methods, using the Python routines developed by Wright (2006) for calculating distances in cosmology.

## Method 1: Nearest Neighbors
The principle of Nearest Neighbors is that galaxies with closest neighbors are in denser environments and, therefore, have higher density fields. 
This method defines the galactic environment using a variable scale, depending on the number of neighbors of each galaxy.
For each galaxy in the sample, values for k are chosen, this being the number of neighbors and calculate the distance to each of them around an interval of z.

## Method 2: Fixed Apertures
This method, unlike the previous one, defines a scale for the environment around a fixed area or volume for each galaxy. 
So, the more galaxies within that area or volume, the denser the environment. 


## References
* Etherington J., Thomas D., Measuring galaxy environments in large-scale photometric
surveys, Monthly Notices of the Royal Astronomical Society, 2015, vol. 451, p. 660

* Lai et al. (2016), CAN WE DETECT THE COLOR–DENSITY RELATION WITH
PHOTOMETRIC REDSHIFTS?, The Astrophysical Journal, 2016, vol. 825, p. 40

* Muldrew et al. (2012), Measures of galaxy environment – I. What is ‘environment’?,
Monthly Notices of the Royal Astronomical Society, 2012, vol. 419, p. 2670

* Wright E., A Cosmology Calculator for the World Wide Web, Publications of the Astro-
nomical Society of the Pacific, 2006, vol. 118, p. 1711–1715
