This a classical implementation of the k-Medoids Algorithm PAM

This implementation is based on the manhattan distance, the function take in entrance matrix defined by a list of lists [[..],[..]...] . The sublists must have the same dimention.

The missing value are traited by the algorithme. It's recommanded to define a missing value like this :

import numpy as np
matrix[i][j] = np.nan

the function return a list which contains the cluster index ofn each points . So for example if we have a result like this :

[0,2,1,0,1]

the first point (it's the first sublist in the entred matrix) is associated to the cluster°0 (the first cluster)
In our example, we got five points and 3 cluster

This implementation can correct the outliers problem. So we can define a threshold and all clusters which a number of points equal or less than the threshold fixed 