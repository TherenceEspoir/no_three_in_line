import numpy as np

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


def nombre_de_conflit(matrice,taille=0):
    """
    Retourne le nombre de conflits dans la matrice
    """
    score = 0
    #ligne
    for ligne in matrice:
        if somme_elements_depasse_deux(ligne):
            score += np.sum(ligne) - 2

    matrice_transposee = np.transpose(matrice)

    #colonne
    for ligne in matrice_transposee:
        if somme_elements_depasse_deux(ligne):
            score += np.sum(ligne) - 2

    #diagonale gauche à droite
    matrice_decale_a_gauche = decale_gauche(matrice)
    mtg= np.transpose(matrice_decale_a_gauche)
    for ligne in mtg:
        if somme_elements_depasse_deux(ligne):
            score += np.sum(ligne) - 2

    #diagonale droite à gauche
    matrice_decale_a_droite = decale_droite(matrice)
    mtd= np.transpose(matrice_decale_a_droite)
    for ligne in mtd:
        if somme_elements_depasse_deux(ligne):
            score += np.sum(ligne) - 2        
    return score
