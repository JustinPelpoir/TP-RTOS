from dataclasses import dataclass
from functools import reduce
from math import lcm


@dataclass
class Tache:
    nom: str
    C: int
    D: int
    T: int
    priorite: int
    restant: int = 0    # travail restant de l'instance en cours
    echeance: int = 0   # échéance absolue de l'instance en cours


def simuler(taches, duree):
    taches = sorted(taches, key=lambda x: x.priorite, reverse=True)  # HPF
    trace, echecs = [], []

    for t in range(duree + 1):
        for tache in taches:
            # 1. échéance ratée ?
            if t == tache.echeance and tache.restant > 0:
                echecs.append((tache.nom, t))
            # 2. activation d'une nouvelle instance
            if t % tache.T == 0:
                tache.restant = tache.C
                tache.echeance = t + tache.D

        if t == duree:
            break

        # 3. choix : la plus prioritaire qui a du travail
        elue = next((x for x in taches if x.restant > 0), None)

        # 4. exécution d'une unité de temps
        if elue:
            elue.restant -= 1
            trace.append(elue.nom)
        else:
            trace.append("-")

    return trace, echecs


if __name__ == "__main__":
    taches = [
        Tache("T1", C=2, D=7, T=7, priorite=20),
        Tache("T2", C=3, D=11, T=11, priorite=15),
        Tache("T3", C=5, D=13, T=13, priorite=10),
    ]

    H = reduce(lcm, (x.T for x in taches))
    trace, echecs = simuler(taches, H)

    print("Hyperpériode :", H)
    print("Début de la trace :", " ".join(trace[:20]))
    if echecs:
        print(f"NON faisable : {len(echecs)} échéance(s) ratée(s), première : {echecs[0]}")
    else:
        print("Faisable")