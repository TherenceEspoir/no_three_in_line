from .utils import *

def giveNumberOfConflict(matrice,taille=0):
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