import csv
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

from Game import game_directory


class Results:
  """
  Printing/saving logs for learning results
  """
  save = False
  path = "{}/Logs/results.txt".format(game_directory)

  def __init__(self):
    self.clean()
    self.savelog("error_code", "rewards")

  @staticmethod
  def savelog(error_code, rewards):
    with open(Results.path, "a", encoding="utf-8") as file_log:
      file_log.write("{};{}\n".format(error_code, rewards))

  @staticmethod
  def clean():
    with open(Results.path, "w", encoding="utf-8") as file_log:
      file_log.write("")

  @staticmethod
  def show_results():
    data = pd.read_csv(Results.path, header=0, sep=';')
    error_codes = data["error_code"].tolist()
    rewards = data["rewards"].tolist()

    different_error_codes = data["error_code"].unique().tolist()
    number_errors = {}
    for code in different_error_codes:
      number_errors[code] = []

    for line in range(len(data)):
      for code in different_error_codes:
        if error_codes[line] == code:
          number_errors[code].append(1 + number_errors[code][line-1] if line else 0)
        else:
          number_errors[code].append(number_errors[code][line-1] if line else 0)

    x = range(len(data))
    # Création du graphe
    plt.figure()

    for code in different_error_codes:
      plt.plot(x, number_errors[code], marker='o', label=f"Error Code {code}")
      plt.legend()

    plt.xlabel("Indice dans le tableau results")
    plt.ylabel("Nombre d'erreurs")
    plt.title("Nombre d'erreurs par code d'erreur")

    plt.show()