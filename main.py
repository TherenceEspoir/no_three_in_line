from lib.utils import *

"""
test = [
    [1, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
]


print(nombre_de_conflit(test))

"""

from sre_constants import JUMP
import numpy as np
from itertools import permutations
import copy, random


# VERSION 1
def giveARandomCandidateSolution_1(N):
  """
  This function gives a random solution (n the size of the grid).

  A solution has between N and 2N pions so that each line has between 1 and 2 pions.
  """
  lines = []
  model = [0] * N
  for i in range(0, N):
    lg = copy.copy(model)
    lg[i] = 1
    lines.append(lg)
    for j in range(i + 1, N):
      lg_2 = copy.copy(lg)
      lg_2[j] = 1
      lines.append(lg_2)

  matrix = []
  for _ in range(N):
    r = random.randint(0, len(lines) - 1)
    matrix.append(lines[r])

  return matrix


# VERSION 2
def giveARandomCandidateSolution_2(N):
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



def print_matrix(matrix):
  for a in range(len(matrix)):
    for b in range(len(matrix)):
      print(matrix[a][b], end=" ")
    print("\n")


def giveNumberOfPions(matrix):
  """
    Cette fonction donne le nombre de pions (valeurs de 1) dans une matrice.
    """
  return np.sum(np.array(matrix) == 1)


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





def fonction_objectif(matrice, taille):
  """
  This function calculates the objective function for the given matrices.
  """
  nb_conflit = nombre_de_conflit(matrice, taille)

  # return round(score / giveNumberOfPions(matrice), 3)
  return 1 - ((giveNumberOfPions(matrice) - nb_conflit) / (2 * taille))


def echange_one_pion(matrix, taille):
  """
  Selon notre relation de voisinage, dite "échange de pion", on veut pouvoir déplacer un pion à un emplacement libre.
  """
  # voisin = copy.deepcopy(matrix)

  # 1. on choisit un pion aléatoire
  while True:
    i = random.randint(0, taille - 1)  #ligne
    j = random.randint(0, taille - 1)  #colonne
    if (matrix[i][j] == 1):
      break

  # 2. on le déplace sur une case libre
  while True:
    new_i = random.randint(0, taille - 1)
    new_j = random.randint(0, taille - 1)
    if (matrix[new_i][new_j] == 0):
      # voisin[new_i][new_j] = 1
      # voisin[i][j] = 0
      # si le nv voisin n'a pas encore été regardé, je break
      break

  # 3. on retourne la matrice
  # return voisin
  return i, j, new_i, new_j


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

  if nombre_de_conflit(matrix,
                           taille) == 0 and giveNumberOfPions(matrix) < 2 * N:
    #ajout d'un pion
    while True:
      a = random.randint(0, N - 1)
      b = random.randint(0, N - 1)
      if matrix[a][b] == 0:
        matrix[a][b] = 1
        break

  return fonction_objectif(matrix, taille)


# stratégies de sélection
def best_improvment(matrix, cout, possible_voisins, taille_voisinage):
  """
  Sélectionne le voisin avec le meilleur score. 
  La fenêtre de voisinage représente ici le coût prêt à être dépensé
  """

  taille = len(matrix)
  nb_eval = 0  # nb d'appel à la fct score
  best_indices = None
  best_score = -1

  while best_indices != -1 and nb_eval < cout:
    best_score = fonction_objectif(matrix, taille)
    nb_eval += 1
    best_indices = -1

    for voisin in range(taille_voisinage):
      if (nb_eval >= cout):
        break

      i, j, new_i, new_j = possible_voisins[voisin]
      if is_possible_move(matrix, i, j, new_i, new_j):

        # evaluation
        score = relation_de_voisinage(matrix, taille, i, j, new_i, new_j)
        nb_eval += 1
        if best_score > score:
          best_score = score
          best_indices = (i, j, new_i, new_j)

    if best_indices != -1:  # j'ai trouvé un meilleur voisin
      (i, j, new_i, new_j) = best_indices
      matrix[i][j] = 0
      matrix[new_i][new_j] = 1
      print_matrix(matrix)
      print(best_score)
      print("=== ET ===")
    elif nb_eval < cout:
      print("Plus de meilleur voisin trouvé (optimum local) !")
      print("nb eval : ", str(nb_eval))
      print("taille voisinage : ", str(taille_voisinage))
    else:
      print("Nombre MAX d'évaluations atteint")

  return matrix, best_score


def first_improvment(matrix, cout, possible_voisins, taille_voisinage):
  "Si le voisin est améliorant on le prend directement"
  taille = np.array(matrix).shape[0]
  best_score = fonction_objectif(matrix, taille)
  nb_eval = 1  # nb d'appel à la fct score

  best_indices = None
  taille_artificielle = taille_voisinage
  voisinage = copy.deepcopy(possible_voisins)

  while best_indices != -1 and nb_eval < cout:
    best_indices = -1
    neighbor_score = 5000
    indices = (-1, -1, -1, -1)

    # tant que je n'ai pas de voisin minimisant mon score
    print("eval ", str(nb_eval), " sur ", str(cout))
    while best_score <= neighbor_score and nb_eval < cout and taille_artificielle > 0:
      rd = random.randint(0, taille_artificielle)
      i, j, new_i, new_j = voisinage[rd]
      indices = (i, j, new_i, new_j)
      if is_possible_move(matrix, i, j, new_i, new_j):

        # evaluation
        neighbor_score = relation_de_voisinage(matrix, taille, i, j, new_i,
                                               new_j)
        nb_eval += 1

      # Dans tous les cas, MAJ des voisins possibles
      part_1 = voisinage[0:rd]
      part_2 = voisinage[rd + 1::]
      voisinage = part_1 + part_2 + [indices]
      taille_artificielle -= 1

    # un voisin améliorant le score a été trouvé
    print("best score : ", str(best_score), " et neighboor Score ",
          str(neighbor_score))
    if neighbor_score < best_score:
      best_score = neighbor_score
      best_indices = indices
      (i, j, new_i, new_j) = best_indices
      matrix[i][j] = 0
      matrix[new_i][new_j] = 1

      print_matrix(matrix)
      print(best_score)
      print("=== ET ===")

      # RAZ des voisins
      taille_artificielle = taille_voisinage
      voisinage = copy.deepcopy(possible_voisins)

    elif taille_artificielle == 0:
      print("Plus de voisin améliorant trouvé !")
      print("nb eval : ", str(nb_eval))
      print("taille voisinage : ", str(taille_voisinage))
    elif nb_eval >= cout:
      print("taille arti : ", str(taille_artificielle))
      print("Nombre MAX d'évaluations atteint : ", str(nb_eval))

  return matrix, best_score


def k_improvment(matrix, possible_voisins, taille_voisinage, k):
  """
  Cherche k voisins améliorants parmi les voisins possibles
  Puis prend le meilleur parmi ces k voisins
  """
  taille = np.array(matrix).shape[0]
  best_score = fonction_objectif(matrix, taille)

  k_voisins_ameliorants = []  # best_indices
  indices = (-1, -1, -1, -1)
  taille_artificielle = taille_voisinage
  voisinage = copy.deepcopy(possible_voisins)

  while len(k_voisins_ameliorants) < k and taille_artificielle > 0:

    rd = random.randint(0, taille_artificielle)
    i, j, new_i, new_j = voisinage[rd]
    indices = (i, j, new_i, new_j)
    if is_possible_move(matrix, i, j, new_i, new_j):

      # evaluation
      neighbor_score = relation_de_voisinage(matrix, taille, i, j, new_i,
                                             new_j)
      if neighbor_score < best_score:
        k_voisins_ameliorants.append([indices, neighbor_score])

      # Dans tous les cas, MAJ des voisins possibles
      part_1 = voisinage[0:rd]
      part_2 = voisinage[rd + 1::]
      voisinage = part_1 + part_2 + [indices]
      taille_artificielle -= 1

  nb_voisins_ameliorants = len(k_voisins_ameliorants)
  if nb_voisins_ameliorants == k or (taille_artificielle == 0
                                     and nb_voisins_ameliorants != 0):
    print(f"{nb_voisins_ameliorants} voisins améliorants trouvés")
    print(f"Taille du voisinage : {taille_voisinage}")
    best_new_score = 5000
    best_indices = (-1, -1, -1, -1)

    for voisin in range(nb_voisins_ameliorants):
      (i, j, new_i, new_j), score = k_voisins_ameliorants[voisin]

      # evaluation
      if best_new_score > score:
        best_new_score = score
        best_indices = (i, j, new_i, new_j)

    # j'ai trouvé mon meilleur voisin parmi les K améliorants
    i, j, new_i, new_j = best_indices
    matrix[i][j] = 0
    matrix[new_i][new_j] = 1
    print_matrix(matrix)
    print(best_new_score)
    print("=== ET ===")

  elif nb_voisins_ameliorants == 0:
    print("Plus de voisin améliorant trouvé !")


if __name__ == "__main__":

  # initialisation d'une matrice aléatoire de taille N
  N = 14
  current_matrix = giveARandomCandidateSolution_2(N)
  # current_matrix = [[1, 0, 1, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 0, 1, 1]]
  possible_voisins, taille_voisinage = generation_voisins(N)
  current_score = fonction_objectif(current_matrix, N)

  print_matrix(current_matrix)
  print(current_score)

  # avec un first improvment
  # while current_score != 0:
  current_matrix, current_score = first_improvment(current_matrix, 200000,
                                                   possible_voisins,
                                                   taille_voisinage)

  #avec un best improvment
  # current_matrix, current_score = best_improvment(current_matrix, 200000,
  # possible_voisins,
  # taille_voisinage)

  print_matrix(current_matrix)
  print(current_score)
  print("Nombre de conflits : ", str(nombre_de_conflit(current_matrix, N)))
  print("Nombre de pions : ", str(giveNumberOfPions(current_matrix)))
