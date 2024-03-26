from .solutionUtils import fonction_objectif, giveNumberOfConflict, giveNumberOfPions
import random

def is_possible_move(matrix, i, j, new_i, new_j):
  """
  Détermine si un mouvement est possible ou non.
  """
  if matrix[i][j] == 1 and matrix[new_i][new_j] == 0:
    return True
  return False


def relation_de_voisinage(matrix, taille, i, j, new_i, new_j):
  """
  Permet de déplacer un pion, d'obtenir un voisin et de l'évaluer
  """

  # application des changements
  matrix[i][j] = 0
  matrix[new_i][new_j] = 1
  score = fonction_objectif(matrix, taille)

  # retour à la solution de base pour explorer les autres voisins
  matrix[i][j] = 1
  matrix[new_i][new_j] = 0

  return score


def relation_de_voisinage_avec_ajout(matrix, taille, i, j, new_i, new_j):
  """
  Permet de déplacer un pion, d'obtenir un voisin et de l'évaluer
  Ajoute un pion si plus de conflit
  A REVOIR
  """

  # application des changements
  matrix[i][j] = 0
  matrix[new_i][new_j] = 1

  if giveNumberOfConflict(matrix,
                           taille) == 0 and giveNumberOfPions(matrix) < 2 * taille:
    #ajout d'un pion
    while True:
      a = random.randint(0, taille - 1)
      b = random.randint(0, taille - 1)
      if matrix[a][b] == 0:
        matrix[a][b] = 1
        break

  return fonction_objectif(matrix, taille)


def generation_voisins(N):
  """
  Renvoie un tableau de vecteurs des mouvements possibles pour générer TOUS les voisins
  N, la taille de la matrice
  """
  tab = []

  vect = ()

  for a in range(N):
    i = a
    for b in range(N):
      j = b

      for c in range(N):
        new_i = c
        for d in range(N):
          new_j = d

          vect = (i, j, new_i, new_j)
          if i == new_i and j == new_j:
            continue
          else:
            tab.append(vect)

  return tab, len(tab)