import math

# Configuration de l'exemple de tâches : (Nom, Durée C, Échéance relative D, Période T)
tasks = [
    {"name": "Thread 1", "C": 2, "D": 7, "T": 7},
    {"name": "Thread 2", "C": 3, "D": 11, "T": 11},
    {"name": "Thread 3", "C": 5, "D": 13, "T": 13},
]

def obtnir_echeance_absolue(job):
  return job["absolute_deadline"]


def simuler_edf(tasks, max_time=None):
  # si max_time pas spécifié, on simule sur l'hyperpériode H
  if max_time is None:
    max_time = math.lcm(*(t["T"] for t in tasks))

  ready = []
  curr = None
  misses = []
  timeline = []  # Trace d exécution
  job_ids = {t["name"]: 0 for t in tasks}

  print(f"=== DEBUT SIMULATION EDF (Horizon: {max_time}s) ===")

  for t in range(max_time):
    
	# Arrivée de nouvelles instances (Jobs)
    for task in tasks:
      if t % task["T"] == 0:
        job_ids[task["name"]] += 1
        job_name = f"{task['name']} (Job {job_ids[task['name']]})"
        # Échéance absolue = Temps d'arrivée + Échéance relative (D_i)
        abs_deadline = t + task["D"]

        ready.append({
            "name": job_name,
            "task": task,
            "rem": task["C"],
            "absolute_deadline": abs_deadline,
        })
        print(
            f"[t={t:2d}s] ARRIVÉE : {job_name} | Échéance absolue :"
            f" t={abs_deadline}s"
        )

    # Vérification des dépassements d'échéance
    for job in list(ready):
      if t >= job["absolute_deadline"] and job["rem"] > 0:
        misses.append((t, job["name"]))
        print(f"!!! [t={t:2d}s] ÉCHÉANCE MANQUÉE par {job['name']} !!!")
        ready.remove(job)
        if curr == job:
          curr = None

    # sélection du job à échéance la plus proche
    if ready:
      # tri dynamique par échéance (plus petite valeur = plus prioritaire)
      ready.sort(key=obtnir_echeance_absolue)
      curr = ready[0]

      timeline.append(curr["name"])
      curr["rem"] -= 1

      print(
          f"       EXÉCUTION : {curr['name']} (reste {curr['rem']}s | échéance"
          f" t={curr['absolute_deadline']}s)"
      )

      
      if curr["rem"] == 0:
        print(f"       FIN : {curr['name']} a terminé son exécution.")
        ready.remove(curr)
        curr = None
    else:
      timeline.append("IDLE")
      print(f"       PROCESSEUR INACTIF (IDLE)")

  faisable = len(misses) == 0
  return faisable, timeline, misses


def main():
	U = sum(t["C"] / t["T"] for t in tasks)
	print(f"Charge processeur U = {U:.3f} (94.3%)\n")


	faisable, trace, manques = simuler_edf(tasks, max_time=20)

	print("\n=== BILAN ===")
	print(f"Système faisable sous EDF : {'OUI' if faisable else 'NON'}")

main()