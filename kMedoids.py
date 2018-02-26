from Cluster import Cluster
from random import randint
from operator import itemgetter
from copy import deepcopy

# usageMatrice ==> [[..],[..],..] each sublist constitute the vector values of a point

# k ==> number of clusters

# nbrImprovementAttempts ==> number of attempts to improve a clustering,
# this parameter influence the reply time of the funtion

def kMedoidsPAM(usageMatrice, k, nbrImprovementAttempts, outliersThresholdTraitement=0):
    clusters=[]
    indicesSelectedClusters=[]

    # choose randomly the medoids and create clusters
    for x in range(k):
        rand = randint(0, len(usageMatrice)-1)
        while rand in indicesSelectedClusters : rand = randint(0,len(usageMatrice)-1)
        clusters.append( Cluster(x, (rand,usageMatrice[rand])) )
        indicesSelectedClusters.append(rand)

    # associate each point of the matrix to the closest cluster
    for x in range(len(usageMatrice)):
        closestCluster = min(
            [ (cluster,cluster.calculDistance ((x,usageMatrice[x])) ) for cluster in clusters] ,key = itemgetter(1))[0]
        i = clusters.index([cluster for cluster in clusters if cluster.numCluster == closestCluster.numCluster][0])
        clusters[i].addMember((x,usageMatrice[x]))

    # initialize a boolean variable that determinate if there is there is modification or no.
    # So if there is no possibility to modify clusters, the algorithm will end
    modif = True

    while modif:

        # determinate the unoptimized cluster to redefine his medoid
        inoptimizedClusterIndex = clusters.index(
            max( [(cluster,cluster.distancesSum) for cluster in clusters], key = itemgetter(1))[0])
        numInoptimizedCluster = clusters[inoptimizedClusterIndex].numCluster

        # create a copy of the list of actual clusters
        newClusters = deepcopy(clusters)

        newIndicesSelectedClusters = indicesSelectedClusters[:]

        # redefine the medoid of the unoptimized cluster
        newIndicesSelectedClusters.remove(clusters[inoptimizedClusterIndex].centroide[0])
        newClusters.remove(newClusters[inoptimizedClusterIndex])
        rand = randint(0, len(usageMatrice)-1)

        while rand in indicesSelectedClusters: rand = randint(0, len(usageMatrice)-1)
        newIndicesSelectedClusters.append(rand)
        newClusters.append(Cluster(numInoptimizedCluster, (rand,usageMatrice[rand])))

        # distribute points to the appropriate new test clusters
        for x in range(k) : newClusters[x].clearCluster()
        for x in range(len(usageMatrice)):
            closestCluster = min(
                [(cluster, cluster.calculDistance((x, usageMatrice[x]))) for cluster in newClusters],key=itemgetter(1))[0]
            i = newClusters.index([cluster for cluster in newClusters if cluster.numCluster == closestCluster.numCluster][0])
            newClusters[i].addMember((x, usageMatrice[x]))

        # if there is an improvement : the list of test clusters become the list of clusters
        if sum([cluster.distancesSum for cluster in newClusters]) < sum([cluster.distancesSum for cluster in clusters]):
            clusters = newClusters[:]
            indicesSelectedClusters = newIndicesSelectedClusters[:]
        # in else we'll change randomly the medoid of the unoptimized cluster until we get an improvement
        else:
            cpt=0
            testedCentroides=[rand]
            improvement = False

            # changing medoid until we get an improvement or until we exceed the number of the improvement attempts
            while(cpt<nbrImprovementAttempts and not improvement):

                # remove the unoptimized cluster from the list of test clusters
                newClusters.remove([cluster for cluster in newClusters if cluster.centroide[0]==rand][0])
                newIndicesSelectedClusters.remove(rand)

                # Choose a new medoid for the unoptimized cluster
                while rand in indicesSelectedClusters or rand in testedCentroides: rand = randint(0, len(usageMatrice)-1)
                testedCentroides.append(rand)
                newIndicesSelectedClusters.append(rand)
                newClusters.append(Cluster(numInoptimizedCluster,(rand, usageMatrice[rand])))

                # redistribuate points
                for x in range(k): newClusters[x].clearCluster()
                for x in range(len(usageMatrice)):
                    closestCluster = min(
                        [(cluster, cluster.calculDistance((x, usageMatrice[x]))) for cluster in newClusters], key=itemgetter(1))[0]
                    i = newClusters.index(
                        [cluster for cluster in newClusters if cluster.numCluster == closestCluster.numCluster][0])
                    newClusters[i].addMember((x, usageMatrice[x]))

                # if is there an improvement update our clusters
                if sum([cluster.distancesSum for cluster in newClusters]) < sum(
                        [cluster.distancesSum for cluster in clusters]):
                    clusters = newClusters[:]
                    indicesSelectedClusters = newIndicesSelectedClusters[:]
                    improvement = True


                cpt +=1

            # we stop algorithm if the number of improvement attempts are consumed
            if not improvement :
                modif = False


    # outliers traitement
    if outliersThresholdTraitement>0:
        nbrClustersToDelete=[]
        for cluster in clusters:
            if len(cluster.members) <= outliersThresholdTraitement:
                nbrClustersToDelete.append(cluster.numCluster)
                while len(cluster.members)>0:

                    # introduice outlier point into an other clost cluster
                    min([(otherCluster,otherCluster.calculDistance(cluster.members[0]))
                                       for otherCluster in clusters if otherCluster.numCluster not in nbrClustersToDelete]
                                      , key=itemgetter(1))[0].members.append(cluster.members[0])
                    cluster.members.remove(cluster.members[0])

    # build the clustering result as a list
    clustering = []
    for cluster in clusters:
        for (id, value) in cluster.members:
            clustering.insert(id, int(cluster.numCluster))

    return clustering