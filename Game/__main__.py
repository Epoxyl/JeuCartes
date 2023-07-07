import gymnasium as gym

from Game.Utils.Exceptions import InvalidCardException
from Game.Utils.colors import bcolors

env = gym.make("President-v0")
from Game.President import President

players = {
  'Alexandre': 'Greedy',
  'Antoine': 'Greedy',
  'Julien': 'Greedy',
  'Bob': 'Learning'
}
agent_list = [0, 0, 0, 0]
MAX_SCORE = 100


def main():
  """
  Main program
  :return:
  """
  print(env)
  game = President(players, True, env)

  for i in range(5000):
    print(bcolors.OKGREEN + "Essai n°{}".format(i) + bcolors.ENDC)
    try:
      game.launch_game()
    except InvalidCardException as e:
      print(
        bcolors.WARNING + "l'épisode s'est stoppé à cause de l'erreur : {}.\nEnregistrement puis lancement d'une nouvelle partie...".format(
          e.__str__()) + bcolors.ENDC)
  # game.update_agents()
