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
  if is_possible_move(matrix, i, j, new_i, new_j) : 
    matrix[i][j] = 0
    matrix[new_i][new_j] = 1
    score = fonction_objectif(matrix, taille)

    # retour à la solution de base pour explorer les autres voisins
    matrix[i][j] = 1
    matrix[new_i][new_j] = 0

    return score, 0
  
  else :
    return 10, -1


def relation_de_voisinage_v2(matrix, taille, i, j, new_i, new_j):
  """
  Permet de déplacer, ajouter ou supprimer un pion, d'obtenir un voisin et de l'évaluer
  Choix de l'action réalisée fait de manière aléatoire
  """

  # choix de l'action
  # action = 0 : déplacement
  # action = 1 : ajout
  # action = 2 : suppression
  action = random.randint(0, 2)
  modif = True

  # application des changements    
  if action == 1 and giveNumberOfPions(matrix) < 2*taille and matrix[new_i][new_j] == 0:
    matrix[new_i][new_j] = 1
    score = fonction_objectif(matrix, taille)
  elif action == 2 and giveNumberOfPions(matrix) > 0 and matrix[i][j] == 1:
    matrix[i][j] = 0
    score = fonction_objectif(matrix, taille)
  elif is_possible_move(matrix, i, j, new_i, new_j) :
    matrix[i][j] = 0
    matrix[new_i][new_j] = 1
    score = fonction_objectif(matrix, taille)
  else : 
    score = 10
    modif = False


  # retour à la solution de base pour explorer les autres voisins
  if action == 1 and modif :
    matrix[new_i][new_j] = 0
  elif action == 2 and modif :
    matrix[i][j] = 1
  elif modif :
    matrix[i][j] = 1
    matrix[new_i][new_j] = 0
  # sinon il n'y a eu aucune modif

  return score, action


def apply_changement(matrix, i, j, new_i, new_j, action) :
  if action == 1 :
    matrix[new_i][new_j] = 1
  elif action == 2 :
    matrix[i][j] = 0
  else :
    matrix[i][j] = 0
    matrix[new_i][new_j] = 1

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