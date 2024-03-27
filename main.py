
from lib.solutionUtils import *
from lib.voisinUtils import *
from lib.conflictUtils import *

import matplotlib.pyplot as plt
from sre_constants import JUMP
import numpy as np
from itertools import permutations
import copy, random
import csv


# stratégies de sélection
def best_improvement(matrix, cout, possible_voisins, taille_voisinage):
  """
  Sélectionne le voisin avec le meilleur score. 
  La fenêtre de voisinage représente ici le coût prêt à être dépensé
  """

  taille = len(matrix)
  nb_eval = 0  # nb d'appel à la fct score
  best_indices = None
  best_score = -1
  nbSolutionCourante = 1

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
      nbSolutionCourante += 1
    elif nb_eval < cout:
      print("Plus de meilleur voisin trouvé (optimum local) !")
      # print("nb eval : ", str(nb_eval))
      # print("taille voisinage : ", str(taille_voisinage))
    else:
      print("Nombre MAX d'évaluations atteint")

  return matrix, best_score, nb_eval, nbSolutionCourante





def first_improvement(matrix, cout, voisinage, taille_voisinage):
  "Si le voisin est améliorant on le prend directement"
  taille = np.array(matrix).shape[0]
  best_score = fonction_objectif(matrix, taille)
  nb_eval = 1  # nb d'appel à la fct score
  nbSolutionCourante = 1

  best_indices = None
  taille_artificielle = taille_voisinage

  while best_indices != -1 and nb_eval < cout:
    best_indices = -1
    neighbor_score = 5000
    indices = (-1, -1, -1, -1)

    # tant que je n'ai pas de voisin minimisant mon score
    # print("eval ", str(nb_eval), " sur ", str(cout))
    while best_score <= neighbor_score and nb_eval < cout and taille_artificielle > 0:
      rd = random.randint(0, taille_artificielle-1)
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
    # print("best score : ", str(best_score), " et neighboor Score ",
    #       str(neighbor_score))
    if neighbor_score < best_score:
      best_score = neighbor_score
      best_indices = indices
      (i, j, new_i, new_j) = best_indices
      matrix[i][j] = 0
      matrix[new_i][new_j] = 1
      nbSolutionCourante += 1

      # RAZ des voisins
      taille_artificielle = taille_voisinage

    elif taille_artificielle == 0:
      print("Plus de voisin améliorant trouvé !")
      # print("nb eval : ", str(nb_eval))
      # print("taille voisinage : ", str(taille_voisinage))
    elif nb_eval >= cout:
      # print("taille arti : ", str(taille_artificielle))
      print("Nombre MAX d'évaluations atteint : ", str(nb_eval))

  return matrix, best_score, nb_eval, nbSolutionCourante





def k_improvement(matrix, voisinage, taille_voisinage, k):
  """
  Cherche k voisins améliorants parmi les voisins possibles
  Puis prend le meilleur parmi ces k voisins
  """
  taille = np.array(matrix).shape[0]
  best_score = fonction_objectif(matrix, taille)
  nb_eval = 1  # nb d'appel à la fct score
  nbSolutionCourante = 1

  indices = (-1, -1, -1, -1)
  taille_artificielle = taille_voisinage
  best_indices = None

  while best_indices != (-1, -1, -1, -1):

    best_indices = (-1, -1, -1, -1)
    k_voisins_ameliorants = []

    # recherche des K améliorants
    while len(k_voisins_ameliorants) < k and taille_artificielle > 0:

      rd = random.randint(0, taille_artificielle-1)
      i, j, new_i, new_j = voisinage[rd]
      indices = (i, j, new_i, new_j)
      
      if is_possible_move(matrix, i, j, new_i, new_j):

        # evaluation
        neighbor_score = relation_de_voisinage(matrix, taille, i, j, new_i,
                                               new_j)
        nb_eval += 1
        if neighbor_score < best_score:
          k_voisins_ameliorants.append([indices, neighbor_score])

      # Dans tous les cas, MAJ des voisins possibles
      part_1 = voisinage[0:rd]
      part_2 = voisinage[rd + 1::]
      voisinage = part_1 + part_2 + [indices]
      taille_artificielle -= 1

    nb_voisins_ameliorants = len(k_voisins_ameliorants)
    if nb_voisins_ameliorants != 0:
      print(f"{nb_voisins_ameliorants} voisins améliorants trouvés")
      print(f"Taille du voisinage : {taille_voisinage}")
      best_new_score = best_score

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
      nbSolutionCourante += 1
      best_score = best_new_score
      # print_matrix(matrix)
      # print(best_score)
      # print("=== ET ===")

      # RAZ des voisins
      taille_artificielle = taille_voisinage

    else:  # et que taille artificielle == 0
      print("Plus de voisin améliorant trouvé !")

  return matrix, best_score, nb_eval, nbSolutionCourante


if __name__ == "__main__":

    nombre_executions = 10
    taille_matrices = [4, 5, 9]
    strategies = ["best", "first", "k2", "k5", "k10"]  # Liste des stratégies incluant kimprovement pour k = 1, 2 et 3


    with open("results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["strategy", "N", "score", "nbEval", "nbSolutionCourante"])
        
    
        for strategy in strategies:
            if strategy.startswith("k"):
                k = int(strategy[1:])  # Récupérer la valeur de k à partir du nom de la stratégie
            for N in taille_matrices:
                possible_voisins, taille_voisinage = generation_voisins(N)
                # Générer les instances et calculer les scores
                for _ in range(nombre_executions):
                    current_matrix = giveARandomCandidateSolution(N)
                    # Appliquer la stratégie
                    if strategy == "best":
                        _, current_score, current_nbEval, current_nbSolutionCourante = best_improvement(current_matrix, 200000,
                                                                  possible_voisins,
                                                                  taille_voisinage)
                    elif strategy == "first":
                        _, current_score, current_nbEval, current_nbSolutionCourante = first_improvement(current_matrix, 200000,
                                                                    possible_voisins,
                                                                    taille_voisinage)
                    elif strategy.startswith("k"):
                        _, current_score, current_nbEval, current_nbSolutionCourante = k_improvement(current_matrix, possible_voisins,
                                                                taille_voisinage, k)
                    else:
                        raise ValueError("Stratégie non valide")


                    writer.writerow([strategy, N, current_score, current_nbEval, current_nbSolutionCourante])
                    

