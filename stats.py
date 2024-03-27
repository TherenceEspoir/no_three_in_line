"""
import csv

def csvcount(filename):
    with open(filename, 'r') as f:
        i = 0
        for ligne in f:
            i += 1
    return i


if __name__ == "__main__":

    nombre_run = 0
    with open(f"config", "r") as file:
        for line in file :
            data = line.split("=")
            if data[0] == "NOMBRE_RUN" :
                nombre_run = int(data[1])


    scores_first = []
    evals_first = []
    convergence_first = []    

    with open(f"results/results_1.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        next(spamreader, None)  # skip the headers
        nb_lines = csvcount("results/results_1.csv") -1
        nb_line = 0

        while nb_line != nb_lines :
            for _ in range(0, nombre_run) :
                tab_scores = []
                tab_nbEval = []
                tab_nbSolCou = []

                data = csvfile.readline().rstrip('\n').split(',')
                strat = data[0]
                _, current_score, current_nbEval, current_nbSolutionCourante = list(map(float, data[1::]))

                tab_scores.append(current_score)
                tab_nbEval.append(current_nbEval)
                tab_nbSolCou.append(current_nbSolutionCourante)

                nb_line += 1

            print("FIN")
            scores_first.append(tab_scores)
            evals_first.append(tab_nbEval)
            convergence_first.append(tab_nbSolCou)

    print(scores_first)
    print(evals_first)
    print(convergence_first)        

"""



# Pour mes "nombre_run" itérations sur ma matrice de taille N avec first
  # ave_first = []
  # worst_first = []
  # best_first = []
  # for tab in scores_first :
  #   ave_first.append(sum(tab)/len(tab))
  #   worst_first.append(max(tab))
  #   best_first.append(min(tab))
  # aveEval_first = []
  # for tab in evals_first :
  #   aveEval_first.append(sum(tab)/len(tab))
  # ave_convergence = []
  # for tab in convergence_first :
  #   ave_convergence.append(sum(tab)/len(tab))


  # plt.plot(taille_matrices, ave_first, 'b-o', label="first improvement")
  # plt.xlabel("N, taille de la matrice")
  # plt.xticks(range(min(taille_matrices), max(taille_matrices)+1, 1))
  # plt.ylabel("score moyen")
  # plt.title("Graphique des scores moyens obtenus pour 10 exécutions de chaque algo sur une instance de taille donnée")
  # plt.legend()
  # plt.show()


  # plt.plot(taille_matrices, aveEval_first, 'b-o', label="first improvement")
  # plt.xlabel("N, taille de la matrice")
  # plt.xticks(range(min(taille_matrices), max(taille_matrices)+1, 1))
  # plt.ylabel("nb d'évaluations moyen")
  # plt.title("Graphique du nombre d'évaluations moyen pour 10 exécutions de chaque algo sur une instance de taille donnée")
  # plt.legend()
  # plt.show()


import csv

import numpy as np

def read_data_by_strat(file_path):
    strategy_data = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            strategy = row['strategy']
            N = int(row['N'])
            score = float(row['score'])
            nbEval = int(row['nbEval'])
            nbSolutionCourante = int(row['nbSolutionCourante'])
            if strategy not in strategy_data:
                strategy_data[strategy] = []
            strategy_data[strategy].append((N, score, nbEval, nbSolutionCourante))
    return strategy_data

scores_file = 'results/results_1.csv'
all_stat = read_data_by_strat(scores_file)

#boucle for sur all_stat pour récupérer la moyenne des scores, moyenne des nbEval et moyenne des nbSolutionCourante par taille de matrice pour chaque stratégie
#puis afficher les graphiques
import matplotlib.pyplot as plt


tab_Result = []
for strategy, data in all_stat.items():
    Ns = set([d[0] for d in data])
    moyennes = {}
    for N in Ns:
        score  = [d[1] for d in data if d[0] == N]
        nbEvals = [d[2] for d in data if d[0] == N]
        nbSolutionsCourantes = [d[3] for d in data if d[0] == N]
        tab_Result.append([strategy,N, score,nbEvals,nbSolutionsCourantes])

print(tab_Result)


for i in range(0, len(tab_Result)):
    
    strategy = tab_Result[i][0]
    taille = tab_Result[i][1]
    mean_score = np.mean(tab_Result[i][2])
    mean_nbEval = np.mean(tab_Result[i][3])
    mean_nbSolCour = np.mean(tab_Result[i][4])

    #graphique du score moyen en fonction de la taille de la matrice pour chaque stratégie
    plt.plot(taille, mean_score, label=strategy)
    plt.xlabel("Taille de la matrice")
    plt.ylabel("Score moyen")
    plt.title("Score moyen en fonction de la taille de la matrice")
    plt.legend()
    plt.show()

    #graphique du nombre d'évaluations moyen en fonction de la taille de la matrice pour chaque stratégie
    plt.plot(taille, mean_nbEval, label=strategy)
    plt.xlabel("Taille de la matrice")
    plt.ylabel("Nombre d'évaluations moyen")
    plt.title("Nombre d'évaluations moyen en fonction de la taille de la matrice")
    plt.legend()
    plt.show()

    #graphique du nombre de solutions courantes moyen en fonction de la taille de la matrice pour chaque stratégie
    plt.plot(taille, mean_nbSolCour, label=strategy)
    plt.xlabel("Taille de la matrice")
    plt.ylabel("Nombre de solutions courantes moyen")
    plt.title("Nombre de solutions courantes moyen en fonction de la taille de la matrice")
    plt.legend()
    plt.show()




#graphique du score moyen en fonction de la taille de la matrice pour chaque stratégie


#on veut 5 grapiques avec autant de courbes que de stratégies


