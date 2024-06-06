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
    scores_file = 'results/results_full.csv'
    all_stat = read_data_by_strat(scores_file)

    # Calculer les moyennes des scores, des nombres d'évaluations et des nombres de solutions courantes
    mean_scores_by_strategy = {}
    best_scores_by_strategy = {}
    worst_scores_by_strategy = {}
    mean_evals_by_strategy = {}
    mean_solutions_by_strategy = {}
    for strategy, data in all_stat.items():
        mean_scores_by_strategy[strategy] = {}
        best_scores_by_strategy[strategy] = {}
        worst_scores_by_strategy[strategy] = {}
        mean_evals_by_strategy[strategy] = {}
        mean_solutions_by_strategy[strategy] = {}
        for N in [4, 5, 6, 10, 12, 13, 14, 20]:
            scores_for_N = [entry[1] for entry in data if entry[0] == N]
            evals_for_N = [entry[2] for entry in data if entry[0] == N]
            solutions_for_N = [entry[3] for entry in data if entry[0] == N]
            mean_score_for_N = np.mean(scores_for_N)
            best_score_for_N = np.min(scores_for_N)
            worst_score_for_N = np.max(scores_for_N)
            mean_eval_for_N = np.mean(evals_for_N)
            mean_solution_for_N = np.mean(solutions_for_N)
            mean_scores_by_strategy[strategy][N] = mean_score_for_N
            best_scores_by_strategy[strategy][N] = best_score_for_N
            worst_scores_by_strategy[strategy][N] = worst_score_for_N
            mean_evals_by_strategy[strategy][N] = mean_eval_for_N
            mean_solutions_by_strategy[strategy][N] = mean_solution_for_N


    plt.figure(figsize=(25, 16))

    # Tracer les courbes pour les scores moyens
    plt.subplot(2, 5, 1)
    for strategy, mean_scores_for_strategy in mean_scores_by_strategy.items():
        plt.plot(list(mean_scores_for_strategy.keys()), list(mean_scores_for_strategy.values()), marker='o', label=strategy)
    plt.xlabel('N, Taille de la matrice')
    plt.ylabel('Score moyen')
    plt.title('Score moyen en fonction de N')
    plt.legend()
    plt.grid(True)

    # Tracer les courbes pour les meilleurs scores
    plt.subplot(2, 5, 7)
    for strategy, best_scores_by_strategy in best_scores_by_strategy.items():
        plt.plot(list(best_scores_by_strategy.keys()), list(best_scores_by_strategy.values()), marker='o', label=strategy)
    plt.xlabel('N, Taille de la matrice')
    plt.ylabel('Meilleurs scores')
    plt.title('Meilleurs scores en fonction de N')
    plt.legend()
    plt.grid(True)

    # Tracer les courbes pour les pires scores
    plt.subplot(2, 5, 3)
    for strategy, worst_scores_by_strategy in worst_scores_by_strategy.items():
        plt.plot(list(worst_scores_by_strategy.keys()), list(worst_scores_by_strategy.values()), marker='o', label=strategy)
    plt.xlabel('N, Taille de la matrice')
    plt.ylabel('Pires scores')
    plt.title('Pires scores en fonction de N')
    plt.legend()
    plt.grid(True)

    # Tracer les courbes pour les nombres d'évaluations moyens
    plt.subplot(2, 5, 9)
    for strategy, mean_evals_for_strategy in mean_evals_by_strategy.items():
        plt.plot(list(mean_evals_for_strategy.keys()), list(mean_evals_for_strategy.values()), marker='o', label=strategy)
    plt.xlabel('N, Taille de la matrice')
    plt.ylabel('Nombre d\'évaluations moyen')
    plt.title('Nombre d\'évaluations moyen en fonction de N')
    plt.legend()
    plt.grid(True)

    # Tracer les courbes pour les nombres de solutions courantes moyens
    plt.subplot(2, 5, 5)
    for strategy, mean_solutions_for_strategy in mean_solutions_by_strategy.items():
        plt.plot(list(mean_solutions_for_strategy.keys()), list(mean_solutions_for_strategy.values()), marker='o', label=strategy)
    plt.xlabel('N, Taille de la matrice')
    plt.ylabel('Nombre de solutions courantes moyen')
    plt.title('Nombre de pas moyen en fonction de N')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
