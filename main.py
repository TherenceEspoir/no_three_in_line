
from lib.solutionUtils import *
from lib.voisinUtils import *
from lib.conflictUtils import *

import matplotlib.pyplot as plt
from sre_constants import JUMP
import numpy as np
from itertools import permutations
import copy, random



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
      # print_matrix(matrix)
      # print(best_score)
      # print("=== ET ===")
    elif nb_eval < cout:
      print("Plus de meilleur voisin trouvé (optimum local) !")
      # print("nb eval : ", str(nb_eval))
      # print("taille voisinage : ", str(taille_voisinage))
    else:
      print("Nombre MAX d'évaluations atteint")

  return matrix, best_score





def first_improvement(matrix, cout, voisinage, taille_voisinage):
  "Si le voisin est améliorant on le prend directement"
  taille = np.array(matrix).shape[0]
  best_score = fonction_objectif(matrix, taille)
  nb_eval = 1  # nb d'appel à la fct score

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

      # print_matrix(matrix)
      # print(best_score)
      # print("=== ET ===")

      # RAZ des voisins
      taille_artificielle = taille_voisinage

    elif taille_artificielle == 0:
      print("Plus de voisin améliorant trouvé !")
      # print("nb eval : ", str(nb_eval))
      # print("taille voisinage : ", str(taille_voisinage))
    elif nb_eval >= cout:
      # print("taille arti : ", str(taille_artificielle))
      print("Nombre MAX d'évaluations atteint : ", str(nb_eval))

  return matrix, best_score, nb_eval





def k_improvement(matrix, voisinage, taille_voisinage, k):
  """
  Cherche k voisins améliorants parmi les voisins possibles
  Puis prend le meilleur parmi ces k voisins
  """
  taille = np.array(matrix).shape[0]
  best_score = fonction_objectif(matrix, taille)

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
      best_score = best_new_score
      # print_matrix(matrix)
      # print(best_score)
      # print("=== ET ===")

      # RAZ des voisins
      taille_artificielle = taille_voisinage

    else:  # et que taille artificielle == 0
      print("Plus de voisin améliorant trouvé !")

  return matrix, best_score


if __name__ == "__main__":
    
  nombre_run = 10

  scores_first = []
  evals_first = []

  taille_matrices = [4, 5, 6, 10, 12, 13, 14] #20, 25, 30

  
  for N in taille_matrices :
    current_matrix = giveARandomCandidateSolution(N)
    with open(f"data/instance_{N}.txt", "w") as file:
      for row in current_matrix:
          file.write(" ".join(map(str, row)) + "\n")
  

  # tester les différentes instances
  for N in taille_matrices :

    possible_voisins, taille_voisinage = generation_voisins(N)
    tab_scores = []
    tab_nbEval = []


    # avec un first improvement
    for iteration in range(nombre_run) :
      # lecture de l'instance initiale
      with open(f"data/instance_{N}.txt", "r") as file:
          current_matrix = [[int(x) for x in line.split()] for line in file]

      print(f"Itération {iteration+1} ({N})")

      _, current_score, current_nbEval = first_improvement(current_matrix, 200000,
                                                      possible_voisins,
                                                      taille_voisinage)
      tab_scores.append(current_score)
      tab_nbEval.append(current_nbEval)

    scores_first.append(tab_scores)
    evals_first.append(tab_nbEval)




    # lecture de l'instance initiale - 2
    # with open(f"data/instance_{i}.txt", "r") as file:
    #     current_matrix = [[int(x) for x in line.split()] for line in file]

    # # avec un best improvment
    # current_matrix, current_score = best_improvement(current_matrix, 200000,
    # possible_voisins,
    # taille_voisinage)



    # lecture de l'instance initiale - 3
    # with open(f"data/instance_{i}.txt", "r") as file:
    #     current_matrix = [[int(x) for x in line.split()] for line in file]

    # # avec un K improvment
    # K = [2, 5, 10]
    # for k in K :
    #   current_matrix, current_score = k_improvement(current_matrix,
    #                                             possible_voisins,
    #                                             taille_voisinage, k)
    

    print_matrix(current_matrix)
    print(current_score)
    print("Nombre de conflits : ", str(giveNumberOfConflict(current_matrix, N)))
    print("Nombre de pions : ", str(giveNumberOfPions(current_matrix)))



  # Pour mes "nombre_run" itérations sur ma matrice de taille N avec first
  ave_first = []
  worst_first = []
  best_first = []
  for tab in scores_first :
    ave_first.append(sum(tab)/len(tab))
    worst_first.append(max(tab))
    best_first.append(min(tab))
  aveEval_first = []
  for tab in evals_first :
    aveEval_first.append(sum(tab)/len(tab))


  plt.plot(taille_matrices, ave_first, 'b-o', label="first improvement")
  plt.xlabel("N, taille de la matrice")
  plt.xticks(range(min(taille_matrices), max(taille_matrices)+1, 1))
  plt.ylabel("score moyen")
  plt.title("Graphique des scores moyens obtenus pour 10 exécutions de chaque algo sur une instance de taille donnée")
  plt.legend()
  plt.show()


  plt.plot(taille_matrices, aveEval_first, 'b-o', label="first improvement")
  plt.xlabel("N, taille de la matrice")
  plt.xticks(range(min(taille_matrices), max(taille_matrices)+1, 1))
  plt.ylabel("nb d'évaluations moyen")
  plt.title("Graphique du nombre d'évaluations moyen pour 10 exécutions de chaque algo sur une instance de taille donnée")
  plt.legend()
  plt.show()                    