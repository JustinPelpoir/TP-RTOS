import math


# Fonction pour obtenir la priorité d'un job
def obtenir_priorite(job):
  return job["prio"]


def simuler(tasks, policy="HPF", preemptive=True):
  H = math.lcm(*(t["T"] for t in tasks))  # Hyperpériode (ppcm des périodes)
  ready = []
  curr = None
  misses = []

  for t in range(H):
    
    # Arrivée des tâches
    for task in tasks:
      if t % task["T"] == 0:
        # Calcul de la priorité selon la politique choisie
        if policy == "HPF":
          prio = task["P"] # Priorité la plus haute = priorité haute
        elif policy == "RM":
          prio = -task["T"]  # Période la plus courte = priorité haute
        else:  # DM
          prio = -task["D"]  # Échéance la plus courte = priorité haute

        ready.append({
            "task": task,
            "rem": task["C"],
            "deadline": t + task["D"],
            "prio": prio,
        })

    # Vérification des échéances manquées
    for job in list(ready):
      if t >= job["deadline"]:
        misses.append((t, job["task"]["name"]))
        ready.remove(job)
        if curr == job:
          curr = None

    
    # Sélection du job le plus prioritaire et exécution
    if ready:
      ready.sort(key=obtenir_priorite, reverse=True)

      if preemptive or curr not in ready:
        curr = ready[0]

      curr["rem"] -= 1
      if curr["rem"] == 0:
        ready.remove(curr)
        curr = None

  return len(misses) == 0, misses


def main():
  # Liste des tâches : (Nom, Durée C, Échéance D, Période T, Priorité P)
  tasks = [
      {"name": "Thread 1", "C": 2, "D": 7, "T": 7, "P": 20},
      {"name": "Thread 2", "C": 3, "D": 11, "T": 11, "P": 15},
      {"name": "Thread 3", "C": 5, "D": 13, "T": 13, "P": 10},
  ]

  for policy in ["HPF", "RM", "DM"]:
    for preemptive in [True, False]:
      ok, misses = simuler(tasks, policy, preemptive)
      mode = "Préemptif" if preemptive else "Non-Préemptif"
      print(f"{policy} ({mode}) -> {'FAISABLE' if ok else 'ÉCHEC'}")
      if not ok:
        print(f"  Échéance manquée à t={misses[0][0]}s par {misses[0][1]}")

if __name__ == "__main__":
  main()