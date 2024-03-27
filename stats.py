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
import matplotlib.pyplot as plt

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
if __name__ == "__main__":
    scores_file = 'results/results_1.csv'
    all_stat = read_data_by_strat(scores_file)

    # Calculer les moyennes des scores, des nombres d'évaluations et des nombres de solutions courantes
    mean_scores_by_strategy = {}
    mean_evals_by_strategy = {}
    mean_solutions_by_strategy = {}
    for strategy, data in all_stat.items():
        mean_scores_by_strategy[strategy] = {}
        mean_evals_by_strategy[strategy] = {}
        mean_solutions_by_strategy[strategy] = {}
        for N in [4, 5, 9]:
            scores_for_N = [entry[1] for entry in data if entry[0] == N]
            evals_for_N = [entry[2] for entry in data if entry[0] == N]
            solutions_for_N = [entry[3] for entry in data if entry[0] == N]
            mean_score_for_N = np.mean(scores_for_N)
            mean_eval_for_N = np.mean(evals_for_N)
            mean_solution_for_N = np.mean(solutions_for_N)
            mean_scores_by_strategy[strategy][N] = mean_score_for_N
            mean_evals_by_strategy[strategy][N] = mean_eval_for_N
            mean_solutions_by_strategy[strategy][N] = mean_solution_for_N

    # Tracer les courbes pour les scores moyens
    plt.figure(figsize=(16, 6))
    plt.subplot(1, 3, 1)
    for strategy, mean_scores_for_strategy in mean_scores_by_strategy.items():
        plt.plot(list(mean_scores_for_strategy.keys()), list(mean_scores_for_strategy.values()), marker='o', label=strategy)
    plt.xlabel('Taille de la matrice')
    plt.ylabel('Score moyen')
    plt.title('Score moyen en fonction de la taille de la matrice')
    plt.legend()
    plt.grid(True)

    # Tracer les courbes pour les nombres d'évaluations moyens
    plt.subplot(1, 3, 2)
    for strategy, mean_evals_for_strategy in mean_evals_by_strategy.items():
        plt.plot(list(mean_evals_for_strategy.keys()), list(mean_evals_for_strategy.values()), marker='o', label=strategy)
    plt.xlabel('Taille de la matrice')
    plt.ylabel('Nombre d\'évaluations moyen')
    plt.title('Nombre d\'évaluations moyen en fonction de la taille de la matrice')
    plt.legend()
    plt.grid(True)

    # Tracer les courbes pour les nombres de solutions courantes moyens
    plt.subplot(1, 3, 3)
    for strategy, mean_solutions_for_strategy in mean_solutions_by_strategy.items():
        plt.plot(list(mean_solutions_for_strategy.keys()), list(mean_solutions_for_strategy.values()), marker='o', label=strategy)
    plt.xlabel('Taille de la matrice')
    plt.ylabel('Nombre de solutions courantes moyen')
    plt.title('Nombre de solutions courantes moyen en fonction de la taille de la matrice')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
