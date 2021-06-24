from . import distances

import math
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd


def createDataFrame(df, estimator = ['knn', 'fixed'], kn=[1, 7, 10, 50], radius=[0.25,1,2,5,8,10]):
    
 if estimator == 'knn': 
    df_environment = pd.DataFrame()
    df_environment = (df_environment
               .assign(id = np.repeat(0,len(df)), 
                      ra = np.repeat(0,len(df)),
                      dec = np.repeat(0,len(df)),
                      z = np.repeat(0,len(df))))
    
    for k in range(0, len(kn)):
         df_environment["sigma_k" + str(kn[k])] = np.repeat(0,len(df))
            
    df_environment = (df_environment
               .assign(
                      n_neighbours = np.repeat(0,len(df)), 
                      neighbours_ids = np.repeat(0,len(df))))

 elif estimator == 'fixed':
        df_environment = pd.DataFrame()
        df_environment = (df_environment
                .assign(id = np.repeat(0,len(df)), 
                        ra = np.repeat(0,len(df)),
                        dec = np.repeat(0,len(df)),
                        z = np.repeat(0,len(df))))
        
        for k in range(0, len(radius)):
            df_environment["sigma_r" + str(radius[k])] = np.repeat(0,len(df))
                
        df_environment = (df_environment
                .assign(
                        n_neighbours = np.repeat(0,len(df)), 
                        neighbours_ids = np.repeat(0,len(df))))

    
 return df_environment

def knn(ra, dec, zs, delta_z, ids, kn=[1, 7, 10, 50]):
    
    df_environment = createDataFrame(ra, estimator = 'knn', kn = kn )
    distd = distances.cosmological_distances(zs)
    dens_knn=np.tile(0.0,len(kn))

    if len(ra) > 10000:
        print('Hmm, I just checked here and it seems your sample is larger than 10k rows... \n')
        print('Go grab some coffee, it may take a few minutes!')
    else:
        print('It will be ready in less than a minute... You are lucky!')

    for i in range(0, len(ra)):
    #definindo intervalo de redshift
        z = zs[i]
        z1 = z-2*delta_z
        z2 = z+2*delta_z
        ra1 = ra[i]
        dec1 = dec[i]
        dist = distd[i]

        # pegando o subgrupo de galáxias nesse intervalo
        ra2 = ra[np.logical_and(zs > z1, zs <= z2)]
        dec2 = dec[np.logical_and(zs > z1, zs <= z2)]

        df_environment['n_neighbours'].iloc[i] = len(ra2)
        df_environment['ra'].iloc[i] = ra1
        df_environment['dec'].iloc[i] = dec1
        df_environment['z'].iloc[i] = z

        d = distances.great_circle_distance(ra1, dec1, ra2, dec2)*dist
        
        # distance to k-neighbours
        indice = np.argsort(d)

        #density
        for k in range(0, len(kn)):
            try: 
                dens_knn[k] = kn[k]/(math.pi*d[indice[kn[k]]]**2)

            except:
                dens_knn[k]=0

            df_environment["sigma_k" + str(kn[k])].iloc[i] = dens_knn[k]

    return df_environment

def fixedApertures(ra, dec, zs, delta_z, ids, radius=[0.25,1,2,5,8,10]):
    
    df_environment = createDataFrame(ra, estimator = 'fixed', radius = radius)
    distd = distances.cosmological_distances(zs)
    dens_radius=np.tile(0.0,len(radius))

    if len(ra) > 10000:
        print('Hmm, I just checked here and it seems your sample is larger than 10k rows... \n')
        print('Go grab some coffee, it may take a few minutes!')
    else:
        print('It will be ready in less than a minute... You are lucky!')

    for i in range(0, len(ra)):
    #definindo intervalo de redshift
        z = zs[i]
        z1 = z-2*delta_z
        z2 = z+2*delta_z
        ra1 = ra[i]
        dec1 = dec[i]
        dist = distd[i]

        # pegando o subgrupo de galáxias nesse intervalo
        ra2 = ra[np.logical_and(zs > z1, zs <= z2)]
        dec2 = dec[np.logical_and(zs > z1, zs <= z2)]

        df_environment['n_neighbours'].iloc[i] = len(ra2)
        df_environment['ra'].iloc[i] = ra1
        df_environment['dec'].iloc[i] = dec1
        df_environment['z'].iloc[i] = z

        d = distances.great_circle_distance(ra1, dec1, ra2, dec2)*dist
        
        # distance to k-neighbours
        indice = np.argsort(d)

        #density 
        for k in range(0, len(radius)):
            dens_radius[k] = len(d[d < radius[k]])/(math.pi*radius[k]**2)

            df_environment["sigma_r" + str(radius[k])].iloc[i] = dens_radius[k]

    return df_environment