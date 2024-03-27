import numpy as np
import copy, random
random.seed(42)

#Fichier de fonctions utilitaires

def transpose(matrice):
    """
    Retourne la transposée de la matrice
    """
    return np.transpose(matrice)

def decale_gauche(t):
    taille = len(t) 
    return [[0]*(taille-i-1) + ligne + [0]*(i) for i, ligne in enumerate(t)]


def decale_droite(t):
    """
    Pour chaque ligne dans le tableau, décaler vers la droite par rapport à son index
    et ajouter des zéros à la fin pour conserver la taille originale de la ligne
    """
    taille = len(t)  
    return [[0]*i + ligne + [0]*(taille-i-1) for i, ligne in enumerate(t)]
   
    
def somme_elements_depasse_deux(ligne):
    """
    Retourne True si la somme des éléments de la ligne dépasse 2, False sinon
    """
    return np.sum(ligne) > 2



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


def print_matrix(matrix):
  for a in range(len(matrix)):
    for b in range(len(matrix)):
      print(matrix[a][b], end=" ")
    print("\n")


