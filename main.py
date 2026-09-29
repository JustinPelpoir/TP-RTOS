import csv
import sys
from dataclasses import dataclass
from functools import reduce
from math import lcm


@dataclass
class Tache:
    nom: str
    C: int
    D: int
    T: int
    priorite: int = 0
    restant: int = 0    # travail restant de l'instance en cours
    echeance: int = 0   # échéance absolue de l'instance en cours


# Question 3 : une politique = une clé de tri (la plus prioritaire en premier)
POLITIQUES = {
    "HPF": lambda x: -x.priorite,
    "RM": lambda x: x.T,
    "DM": lambda x: x.D,
}


# Question 2 : les tâches viennent d'un fichier, leur nombre est quelconque
def charger(fichier):
    with open(fichier, newline="", encoding="utf-8") as f:
        return [
            Tache(ligne["nom"], int(ligne["C"]), int(ligne["D"]), int(ligne["T"]),
                  int(ligne.get("priorite") or 0))
            for ligne in csv.DictReader(f)
        ]


def simuler(taches, duree, politique):
    taches = sorted(taches, key=POLITIQUES[politique])
    for x in taches:
        x.restant, x.echeance = 0, 0
    trace, echecs = [], []

    for t in range(duree + 1):
        for tache in taches:
            if t == tache.echeance and tache.restant > 0:
                echecs.append((tache.nom, t))
            if t % tache.T == 0:
                tache.restant = tache.C
                tache.echeance = t + tache.D

        if t == duree:
            break

        elue = next((x for x in taches if x.restant > 0), None)
        if elue:
            elue.restant -= 1
            trace.append(elue.nom)
        else:
            trace.append("-")

    return trace, echecs


if __name__ == "__main__":
    fichier = sys.argv[1] if len(sys.argv) > 1 else "taches.csv"
    taches = charger(fichier)

    H = reduce(lcm, (x.T for x in taches))
    U = sum(x.C / x.T for x in taches)
    print(f"{len(taches)} tâches | U = {U:.3f} | hyperpériode = {H}\n")

    for politique in POLITIQUES:
        trace, echecs = simuler(taches, H, politique)
        ordre = " > ".join(x.nom for x in sorted(taches, key=POLITIQUES[politique]))
        verdict = f"NON faisable (1er échec : {echecs[0]})" if echecs else "faisable"
        print(f"{politique:3} | {ordre} | {verdict}")