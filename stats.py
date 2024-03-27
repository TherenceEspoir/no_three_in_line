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

    with open(f"results/results_first.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        next(spamreader, None)  # skip the headers
        nb_lines = csvcount("results/results_first.csv") -1
        nb_line = 0

        while nb_line != nb_lines :
            for _ in range(0, nombre_run) :
                tab_scores = []
                tab_nbEval = []
                tab_nbSolCou = []

                data = csvfile.readline().rstrip('\n').split(',')
                print(data)
                _, _, current_score, current_nbEval, current_nbSolutionCourante = list(map(float, data))

                tab_scores.append(current_score)
                tab_nbEval.append(current_nbEval)
                tab_nbSolCou.append(current_nbSolutionCourante)

                nb_line += 1

            print("FIN")
            scores_first.append(tab_scores)
            evals_first.append(tab_nbEval)
            convergence_first.append(tab_nbSolCou)





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