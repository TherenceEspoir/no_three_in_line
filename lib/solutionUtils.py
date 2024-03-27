
import copy, random
import numpy as np


from .conflictUtils import giveNumberOfConflict


def giveARandomCandidateSolution(N):
    """
    This function gives a random solution (n the size of the grid).
    A line can have more than 2 pions.

    Returns a matrix as a list of lists with N to 2N pions randomly placed.
    """
    # Initialisation de la matrice comme une liste de listes remplies de 0
    matrix = [[0 for _ in range(N)] for _ in range(N)]
    nbPions = random.randint(N, 2 * N)

    for _ in range(nbPions):
        while True:
            i = random.randint(0, N - 1)
            j = random.randint(0, N - 1)
            if matrix[i][j] == 0:
                matrix[i][j] = 1
                break

    return matrix


def giveNumberOfPions(matrix):
  """
    Cette fonction donne le nombre de pions (valeurs de 1) dans une matrice.
    """
  return np.sum(np.array(matrix) == 1)



def fonction_objectif(matrice, taille):
  """
  This function calculates the objective function for the given matrices.
  """
  nb_conflit = giveNumberOfConflict(matrice, taille)

  return round(1 - ((giveNumberOfPions(matrice) - nb_conflit) / (2 * taille)), 4)