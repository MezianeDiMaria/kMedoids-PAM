from random import randint
import numpy as np

class Cluster :
    """
    numCluster : the number of the cluster
    centroide : point that represent the center of the cluster ==> (index in the entered matrix,(vector of values))
    members : list of all points which are includes in the cluster , they are defined like the centroide
    distancesSum : the sum of distances between each point of the cluster and the centroide
    """
    def __init__(self,numCluster, centroide):
        self.numCluster = numCluster
        self.centroide = centroide
        self.members = []
        self.distancesSum = 0

    def addMember(self,member):
        self.members.append(member)
        self.distancesSum += self.calculDistance(member)

    def clearCluster(self):
        self.members.clear()
        self.distancesSum = 0

    # Manhattan distance
    def calculDistance(self,point):
        return sum([abs(self.centroide[1][x]-point[1][x]) for x in range(len(self.centroide[1]))
                    if self.centroide[1][x] != np.nan and point[1][x] != np.nan])




