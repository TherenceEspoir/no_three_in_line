import matplotlib.pyplot as plt
import csv
import numpy as np

def csvcount(filename):
    with open(filename, 'r') as f:
        i = 0
        for ligne in f:
            i += 1
    return i


if __name__ == "__main__":

    taille_matrices = [4, 5, 9] # à récupérer autrement

    nombre_run = 0
    with open(f"config", "r") as file:
        for line in file :
            data = line.split("=")
            if data[0] == "NOMBRE_RUN" :
                nombre_run = int(data[1])


    scores_first = []
    evals_first = []
    convergence_first = []

    scores_best = []
    evals_best = []
    convergence_best = [] 

    with open(f"results/results_1.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        next(spamreader, None)  # skip the headers
        nb_lines = csvcount("results/results_1.csv") -1
        nb_line = 0

        while nb_line != nb_lines :
            tab_scores = []
            tab_nbEval = []
            tab_nbSolCou = []
            
            for _ in range(0, nombre_run) :

                data = csvfile.readline().rstrip('\n').split(',')
                strat = data[0]
                _, current_score, current_nbEval, current_nbSolutionCourante = list(map(float, data[1::]))

                tab_scores.append(current_score)
                tab_nbEval.append(current_nbEval)
                tab_nbSolCou.append(current_nbSolutionCourante)
                nb_line += 1

            match strat :
                case "first" :
                    scores_first.append(tab_scores)
                    evals_first.append(tab_nbEval)
                    convergence_first.append(tab_nbSolCou)

                case "best" :
                    scores_best.append(tab_scores)
                    evals_best.append(tab_nbEval)
                    convergence_best.append(tab_nbSolCou)
                    
    
    ave_score_first = []
    worst_score_first = []
    best_score_first = []
    for tab in scores_first :
        ave_score_first.append(sum(tab) / len(tab))
        worst_score_first.append(max(tab))
        best_score_first.append(min(tab))

    ave_score_best = []
    worst_score_best = []
    best_score_best = []
    for i in range(len(taille_matrices)) :
        ave_score_best.append(np.mean(scores_best[i]))
        worst_score_best.append(max(tab))
        best_score_best.append(min(tab))

    
    # graphique du score moyen en fonction de la taille de la matrice pour chaque stratégie
    plt.plot(taille_matrices, ave_score_first, 'b-o', label="first improvement")
    plt.plot(taille_matrices, ave_score_best, 'r-o', label="best improvement")
    plt.xlabel("Taille de la matrice")
    plt.ylabel("Score moyen")
    plt.title("Score moyen en fonction de la taille de la matrice")
    plt.legend()
    plt.show()


    # graphique du pire score en fonction de la taille de la matrice pour chaque stratégie
    plt.plot(taille_matrices, worst_score_first, 'b-o', label="first improvement")
    plt.plot(taille_matrices, worst_score_best, 'r-o', label="best improvement")
    plt.xlabel("Taille de la matrice")
    plt.ylabel("Score moyen")
    plt.title("Score moyen en fonction de la taille de la matrice")
    plt.legend()
    plt.show()


    # graphique du pire score en fonction de la taille de la matrice pour chaque stratégie
    plt.plot(taille_matrices, best_score_first, 'b-o', label="first improvement")
    plt.plot(taille_matrices, best_score_best, 'r-o', label="best improvement")
    plt.xlabel("Taille de la matrice")
    plt.ylabel("Score moyen")
    plt.title("Score moyen en fonction de la taille de la matrice")
    plt.legend()
    plt.show()
