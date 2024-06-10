
from lib.solutionUtils import *
from lib.voisinUtils import *
from lib.conflictUtils import *

import matplotlib.pyplot as plt
from sre_constants import JUMP
import numpy as np
from itertools import permutations
import copy, random, csv



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

      # evaluation
      score, action = relation_de_voisinage(matrix, taille, i, j, new_i, new_j)
      # score, action = relation_de_voisinage_v2(matrix, taille, i, j, new_i, new_j)
      if score != 10 : nb_eval += 1
      if best_score > score:
        best_score = score
        best_indices = (i, j, new_i, new_j)
        best_action = action

    if best_indices != -1:  # j'ai trouvé un meilleur voisin
      (i, j, new_i, new_j) = best_indices
      apply_changement(matrix, i, j, new_i, new_j, best_action)
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

      # evaluation
      # neighbor_score, action = relation_de_voisinage(matrix, taille, i, j, new_i,
      #                                        new_j)
      neighbor_score, action = relation_de_voisinage_v2(matrix, taille, i, j, new_i,
                                              new_j)
      if neighbor_score != 10 : nb_eval += 1

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
      apply_changement(matrix, i, j, new_i, new_j, action)
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





def k_improvement(matrix, voisinage, taille_voisinage, k, cout):
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
    while len(k_voisins_ameliorants) < k and taille_artificielle > 0 and nb_eval < cout:

      rd = random.randint(0, taille_artificielle-1)
      i, j, new_i, new_j = voisinage[rd]
      indices = (i, j, new_i, new_j)
      

      # evaluation
      # neighbor_score, action = relation_de_voisinage(matrix, taille, i, j, new_i,
      #                                        new_j)
      neighbor_score, action = relation_de_voisinage_v2(matrix, taille, i, j, new_i,
                                              new_j)
      if neighbor_score != 10 : nb_eval += 1
      if neighbor_score < best_score:
        k_voisins_ameliorants.append([indices, neighbor_score, action])

      # Dans tous les cas, MAJ des voisins possibles
      part_1 = voisinage[0:rd]
      part_2 = voisinage[rd + 1::]
      voisinage = part_1 + part_2 + [indices]
      taille_artificielle -= 1

    nb_voisins_ameliorants = len(k_voisins_ameliorants)
    if nb_voisins_ameliorants != 0:
      print(f"{nb_voisins_ameliorants} voisins améliorants trouvés")
      # print(f"Taille du voisinage : {taille_voisinage}")
      best_new_score = best_score

      for voisin in range(nb_voisins_ameliorants):
        (i, j, new_i, new_j), score, action = k_voisins_ameliorants[voisin]

        # evaluation
        if best_new_score > score:
          best_new_score = score
          best_indices = (i, j, new_i, new_j)
          best_action = action

      # j'ai trouvé mon meilleur voisin parmi les K améliorants
      i, j, new_i, new_j = best_indices
      apply_changement(matrix, i, j, new_i, new_j, best_action)
      nbSolutionCourante += 1
      best_score = best_new_score
      # print_matrix(matrix)
      # print(best_score)
      # print("=== ET ===")

      # RAZ des voisins
      taille_artificielle = taille_voisinage

    # else:  # et que taille artificielle == 0
    #   print("Plus de voisin améliorant trouvé !")
    elif taille_artificielle == 0:
      print("Plus de voisin améliorant trouvé !")
    elif nb_eval >= cout:
      print("Nombre MAX d'évaluations atteint : ", str(nb_eval))

  return matrix, best_score, nb_eval, nbSolutionCourante 


#méthode de pertubation
def pertubation(matrix,number_of_pertubation):
  taille = len(matrix)

  for _ in range(number_of_pertubation):

    i = random.randint(0, taille - 1)
    j = random.randint(0, taille - 1)

    new_i = random.randint(0, taille - 1)
    new_j = random.randint(0, taille - 1)

    #while not is_possible_move(matrix, i, j, new_i, new_j):
    while(matrix[i][j] == matrix[new_i][new_j] ):
      i = random.randint(0, taille - 1)
      j = random.randint(0, taille - 1)
      new_i = random.randint(0, taille - 1)
      new_j = random.randint(0, taille - 1)
    matrix[i][j] , matrix[new_i][new_j] = matrix[new_i][new_j], matrix[i][j]
  return matrix


def ils(matrix, cout, possible_voisins, taille_voisinage, strategy, perturbation_strength=1):
    """
    Implémentation de l'Iterated Local Search (ILS).
    """
    perturbation_strength = int(len(matrix) / 2)
    # best_matrix = copy.deepcopy(matrix)
    # best_score = fonction_objectif(best_matrix, taille)
    nb_eval = 0
    nbpas=0

    if strategy == "best":
        best_matrix, best_score, evaluations, nbSolutionCourante = best_improvement(matrix, cout-nb_eval, possible_voisins, taille_voisinage)
    elif strategy == "first":
        best_matrix, best_score, evaluations, nbSolutionCourante = first_improvement(matrix, cout-nb_eval, possible_voisins, taille_voisinage)
    elif strategy.startswith("k"):
        k = int(strategy[1:])
        best_matrix, best_score, evaluations, nbSolutionCourante = k_improvement(matrix, possible_voisins, taille_voisinage, k, cout-nb_eval)
    else:
        raise ValueError("Stratégie non valide")
    nb_eval += evaluations
    nbpas+=1
    
    
    while nb_eval < cout:
        matrix = pertubation(best_matrix, perturbation_strength)
        if strategy == "best":
            maybeBest_matrix, maybeBest_score, evaluations, nbSolutionCourante = best_improvement(matrix, cout-nb_eval, possible_voisins, taille_voisinage)
        elif strategy == "first":
            maybeBest_matrix, maybeBest_score, evaluations, nbSolutionCourante = first_improvement(matrix, cout-nb_eval, possible_voisins, taille_voisinage)
        elif strategy.startswith("k"):
            k = int(strategy[1:])
            maybeBest_matrix, maybeBest_score, evaluations, nbSolutionCourante = k_improvement(matrix, possible_voisins, taille_voisinage, k, cout-nb_eval)
        else:
            raise ValueError("Stratégie non valide")

        nb_eval += evaluations
        nbpas+=1

        if maybeBest_score < best_score:
            best_matrix = copy.deepcopy(maybeBest_matrix)
            best_score = maybeBest_score

        

    return best_matrix, best_score, nb_eval, nbpas                   
      

if __name__ == "__main__":

  nombre_executions = 0
  with open(f"config", "r") as file:
    for line in file :
      data = line.split("=")
      if data[0] == "NOMBRE_RUN" :
        nombre_executions = int(data[1])
              
  # taille_matrices = [4, 5, 9]
  taille_matrices = [4, 5, 6, 10, 12, 13, 14, 20]

  # création des matrices initiales
  for N in taille_matrices :
    current_matrix = giveARandomCandidateSolution(N)
    with open(f"data/instance_{N}.txt", "w") as file:
      for row in current_matrix:
          file.write(" ".join(map(str, row)) + "\n")


  #strategies = ["best", "first", "k2", "k5", "k10","ils"]  # Liste des stratégies incluant kimprovement pour k = 1, 2 et 3
  strategies = ["ils"]

  with open("results/results_ilsk5_v2j.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["strategy", "N", "score", "nbEval", "nbSolutionCourante"])
    

    for strategy in strategies:
      if strategy.startswith("k"):
        k = int(strategy[1:])  # Récupérer la valeur de k à partir du nom de la stratégie
      
      for N in taille_matrices:
        possible_voisins, taille_voisinage = generation_voisins(N)
        
        # Calculer les scores
        for iteration in range(nombre_executions):

          # lecture de l'instance initiale
          with open(f"data/instance_{N}.txt", "r") as matrix:
            current_matrix = [[int(x) for x in line.split()] for line in matrix]

          print(f"Itération {iteration+1} ({N})")

          # Appliquer la stratégie

          if strategy == "ils":
                        current_matrix, current_score, current_nbEval,current_nbSolutionCourante = ils(
                            current_matrix, 200000, possible_voisins, taille_voisinage, strategy="k5", perturbation_strength=2
                        )
                    
          elif strategy == "best":
            current_matrix, current_score, current_nbEval, current_nbSolutionCourante = best_improvement(current_matrix, 200000,
                                                        possible_voisins,
                                                        taille_voisinage)
          elif strategy == "first":
            current_matrix, current_score, current_nbEval, current_nbSolutionCourante = first_improvement(current_matrix, 200000,
                                                          possible_voisins,
                                                          taille_voisinage)
          elif strategy.startswith("k"):
            current_matrix, current_score, current_nbEval, current_nbSolutionCourante = k_improvement(current_matrix, possible_voisins,
                                                      taille_voisinage, k)
          else:
            raise ValueError("Stratégie non valide")


          writer.writerow([strategy, N, current_score, current_nbEval, current_nbSolutionCourante])
          print_matrix(current_matrix)
          print(current_score)
          print("Nombre de conflits : ", str(giveNumberOfConflict(current_matrix, N)))
          print("Nombre de pions : ", str(giveNumberOfPions(current_matrix)))
