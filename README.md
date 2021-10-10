# Building an environmental catalog for galaxies

**Author**: Kayleigh Meneghini | **Email**: kayleighmeneghini@gmail.com

## How to use

This package is available on [PyPi](https://pypi.org/project/galaxy-environment/).

For more details, please check this [tutorial](https://github.com/kaykeigh/galaxy-environment/blob/master/tutorial/Tutorial.ipynb), using [S-PLUS](https://arxiv.org/pdf/1907.01567.pdf) data.


```
# Installing 
pip install galaxy-environment
```

```
# import 
from galaxy_environment import environment
```

### Any doubts about this package, please write to kayleighmeneghini@gmail.com
-------------------------------------------------------------------------------------------------------------------

## Introduction 
The environment has a decisive role in how galaxies evolve. We observed a strong correlation between galaxy properties such as color, morphology and their environment. However, the definition of environment makes this type of study non-trivial, after all, we can consider the local environment, as the association of a central galaxy and its satellites, or on larger scales, groups and clusters of galaxies.

There are two wide methods used to define the galactic environment, these are: **Nearest Neighbors and Fixed Apertures**.

In this package I have implemented the calculation of environmental estimators by these two methods, using the Python routines developed by Wright (2006) for calculating distances in cosmology.

## Method 1: Nearest Neighbors
The principle of Nearest Neighbors is that galaxies with closest neighbors are in denser environments and, therefore, have higher density fields. 
This method defines the galactic environment using a variable scale, depending on the number of neighbors of each galaxy.
For each galaxy in the sample, values for k are chosen, this being the number of neighbors and calculate the distance to each of them around an interval of z.

## Method 2: Fixed Apertures
This method, unlike the previous one, defines a scale for the environment around a fixed area or volume for each galaxy. 
So, the more galaxies within that area or volume, the denser the environment. 

## Method 3: Bayesian density estimator
An alternative method proposed by [Ivezic et. al (2005)](https://iopscience.iop.org/article/10.1086/427392/pdf), considering distances to *all* K neighbors instead of only the distance to the K-th nearest neighbor
