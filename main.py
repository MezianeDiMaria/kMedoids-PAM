from random import randint
from kMedoids import kMedoidsPAM

myMatrix = [[randint(1,5) for j in range (6)] for i in range(15)]

medoidsNumber = 6

ImpAttNbr = 5

# Important : the sum of medoidsNumber and ImpAttNbr must be less than usageMatrixe length value.
# Otherwise the algorithm will enter an infinite loop

oTT = 3

clustering = kMedoidsPAM(usageMatrice=myMatrix,k=medoidsNumber,nbrImprovementAttempts= ImpAttNbr,
                         outliersThresholdTraitement=oTT)
print(clustering)