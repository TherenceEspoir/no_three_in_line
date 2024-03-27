import csv


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

        while csvfile.readline() :
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

            print("FIN")
            scores_first.append(tab_scores)
            evals_first.append(tab_nbEval)
            convergence_first.append(tab_nbSolCou)


