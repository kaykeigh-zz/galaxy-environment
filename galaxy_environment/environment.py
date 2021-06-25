from . import distances

import math
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd


def createDataFrame(df, estimator = ['knn', 'fixed'], kn=[1, 7, 10, 50], radius=[0.25,1,2,5,8,10]):
    '''
    Creates a pandas dataframe for the environmental estimators.
    
    Parameters:
    -----------
    
    df: Pandas dataframe containing the sample of galaxies;
    
    estimator: str
    'knn' for the nearest neighbors method
    'fixed' for fixed apertures method.
    
    kn: list
    List containing k values for calculating distances to k-neighbors.
    
    radius: list
    List containing the projected radius values in Mpc.
    
    '''
    
    if estimator == 'knn': 
        df_environment = pd.DataFrame()
        df_environment = (df_environment
                   .assign(ID = np.repeat(0,len(df)), 
                          ra = np.repeat(0,len(df)),
                          dec = np.repeat(0,len(df)),
                          z = np.repeat(0,len(df))))
    
        for k in range(0, len(kn)):
             df_environment["sigma_k" + str(kn[k])] = np.repeat(0,len(df))

        df_environment = (df_environment
                    .assign(n_neighborhood = np.repeat(0,len(df))))

    elif estimator == 'fixed':
        df_environment = pd.DataFrame()
        df_environment = (df_environment
                .assign(ID = np.repeat(0,len(df)), 
                        ra = np.repeat(0,len(df)),
                        dec = np.repeat(0,len(df)),
                        z = np.repeat(0,len(df))))
        
        for k in range(0, len(radius)):
            df_environment["sigma_r" + str(radius[k])] = np.repeat(0,len(df))
                
        df_environment = (df_environment
                .assign(n_neighborhood = np.repeat(0,len(df))))

    
    return df_environment

def knn(df, id_column = 'ID', ra_column='RA', dec_column='DEC' , degrees = True, z_column ='z', delta_z=None, kn=[1, 7, 10, 50]):
    ''' 
    For each galaxy in the sample, we choose values for k, 
    which is the number of neighbors around a range of z. 
    The distance to each k neighbor is calculated and 
    the surface density of galaxies in that radius is estimated. 
   
   
    Parameters:
    -----------
    df = Pandas dataframe
    Each line represents a galaxy with its respective coordinates (RA and Dec) and redshift (z);
    
    ra_column = str
    Column name in the dataframe containing the right ascension coordinate in degrees;
    
    dec_column = str
    Column name in the dataframe containing the declination coordinate in degrees;
    
    degrees = Boolean
    True by default. 
    If your coordinates are in radians, pass the value False for the parameter;
    
    z_column = str
    Column name in the dataframe containing the redshift;
    
    delta_z = float
    None by default, it will be taken two standard deviations of z column.  
    If you prefer, you can pass a float for this parameter;
    
    kn = list
    List containing k values for calculating distances to k-neighbors.
    
    
     
    ''' 
 
    if degrees == True: 
        ra = df[ra_column].values * (math.pi/180)
        dec = df[dec_column].values * (math.pi/180)
    else: 
        ra = df[ra_column].values
        dec = df[dec_column].values 
        
    ids = df[id_column].values
    zs = df[z_column].values
    
    if delta_z is None:
        delta_z = np.std(zs).round(3)
    
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

        
        df_environment['ID'].iloc[i] = ids[i]
        df_environment['n_neighborhood'].iloc[i] = len(ra2)
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

def fixedApertures(df, id_column = 'ID',  ra_column='RA', dec_column='DEC' , degrees = True, z_column ='z', delta_z=None, 
                   radius =[0.25,1,2,5,8,10]):
    ''' 
    This method defines a scale for the environment, 
    We calculate the density by counting the number of galaxies 
    within a fixed radius in Mpc around a range of z.
   
   
    Parameters:
    -----------
    df = Pandas dataframe
    Each line represents a galaxy with its respective coordinates (RA and Dec) and redshift (z);
    
    ra_column = str
    Column name in the dataframe containing the right ascension coordinate in degrees;
    
    dec_column = str
    Column name in the dataframe containing the declination coordinate in degrees;
    
    degrees = Boolean
    True by default. 
    If your coordinates are in radians, pass the value False for the parameter;
    
    z_column = str
    Column name in the dataframe containing the redshift;
    
    delta_z = float
    None by default, it will be taken two standard deviations of z column. 
    If you prefer, you can pass a float for this parameter;
    
    radius = list
    List containing the projected radius values in Mpc.
    
    '''
    
    if degrees: 
        ra = df[ra_column].values * (math.pi/180)
        dec = df[dec_column].values * (math.pi/180)
    else: 
        ra = df[ra_column].values
        dec = df[dec_column].values 
        
    ids = df[id_column].values
    zs = df[z_column].values
    
    if delta_z is None:
        delta_z = np.std(zs).round(3)
    
    df_environment = createDataFrame(ra, estimator = 'fixed', radius = radius)
    distd = distances.cosmological_distances(zs)
    dens_radius=np.tile(0.0,len(radius))

    if len(ra) > 10000:
        print('Hmm, I just checked here and it seems your sample is larger than 10k rows... \n')
        print('Go grab some coffee! It may take a while...')
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

        df_environment['ID'].iloc[i] = ids[i]
        df_environment['n_neighborhood'].iloc[i] = len(ra2)
        df_environment['ra'].iloc[i] = ra1
        df_environment['dec'].iloc[i] = dec1
        df_environment['z'].iloc[i] = z

        d = distances.great_circle_distance(ra1, dec1, ra2, dec2)*dist
        

        #density 
        for k in range(0, len(radius)):
            dens_radius[k] = len(d[d < radius[k]])/(math.pi*radius[k]**2)

            df_environment["sigma_r" + str(radius[k])].iloc[i] = dens_radius[k]

    return df_environment