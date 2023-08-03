import json
from typing import List
import numpy as np

import gymnasium as gym
from gymnasium import spaces
from gymnasium.error import DependencyNotInstalled

from Game.Deck import get_card_string
from Game.Player import Player
from Game.Utils.Exceptions import InvalidCardException

from collections import defaultdict

from Game.__main__ import Results


class PresidentEnv(gym.Env):
  """
  Blackjack is a card game where the goal is to beat the dealer by obtaining cards
  that sum to closer to 21 (without going over 21) than the dealers cards.

  ## Description
  The game starts with the dealer having one face up and one face down card,
  while the player has two face up cards. All cards are drawn from an infinite deck
  (i.e. with replacement).

  The card values are:
  - Face cards (Jack, Queen, King) have a point value of 10.
  - Aces can either count as 11 (called a 'usable ace') or 1.
  - Numerical cards (2-9) have a value equal to their number.

  The player has the sum of cards held. The player can request
  additional cards (hit) until they decide to stop (stick) or exceed 21 (bust,
  immediate loss).

  After the player sticks, the dealer reveals their facedown card, and draws cards
  until their sum is 17 or greater. If the dealer goes bust, the player wins.

  If neither the player nor the dealer busts, the outcome (win, lose, draw) is
  decided by whose sum is closer to 21.

  This environment corresponds to the version of the blackjack problem
  described in Example 5.1 in Reinforcement Learning: An Introduction
  by Sutton and Barto [<a href="#blackjack_ref">1</a>].

  ## Action Space
  The action shape is `(1,)` in the range `{0, 1}` indicating
  whether to stick or hit.

  - 0: Stick
  - 1: Hit

  ## Observation Space
  The observation consists of a 3-tuple containing: the player's current sum,
  the value of the dealer's one showing card (1-10 where 1 is ace),
  and whether the player holds a usable ace (0 or 1).

  The observation is returned as `(int(), int(), int())`.

  ## Starting State
  The starting state is initialised in the following range.

  | Observation               | Min  | Max  |
  |---------------------------|------|------|
  | Player current sum        |  4   |  12  |
  | Dealer showing card value |  2   |  11  |
  | Usable Ace                |  0   |  1   |

  ## Rewards
  - win game: +1
  - lose game: -1
  - draw game: 0
  - win game with natural blackjack:
  +1.5 (if <a href="#nat">natural</a> is True)
  +1 (if <a href="#nat">natural</a> is False)

  ## Episode End
  The episode ends if the following happens:

  - Termination:
  1. The player hits and the sum of hand exceeds 21.
  2. The player sticks.

  An ace will always be counted as usable (11) unless it busts the player.

  ## Information

  No additional information is returned.

  ## Arguments

  ```python
  import gymnasium as gym
  gym.make('Blackjack-v1', natural=False, sab=False)
  ```

  <a id="nat"></a>`natural=False`: Whether to give an additional reward for
  starting with a natural blackjack, i.e. starting with an ace and ten (sum is 21).

  <a id="sab"></a>`sab=False`: Whether to follow the exact rules outlined in the book by
  Sutton and Barto. If `sab` is `True`, the keyword argument `natural` will be ignored.
  If the player achieves a natural blackjack and the dealer does not, the player
  will win (i.e. get a reward of +1). The reverse rule does not apply.
  If both the player and the dealer get a natural, it will be a draw (i.e. reward 0).

  ## References
  <a id="blackjack_ref"></a>[1] R. Sutton and A. Barto, “Reinforcement Learning:
  An Introduction” 2020. [Online]. Available: [http://www.incompleteideas.net/book/RLbook2020.pdf](http://www.incompleteideas.net/book/RLbook2020.pdf)

  ## Version History
  * v1: Fix the natural handling in Blackjack
  * v0: Initial version release
  """

  def __init__(self, nb_cards_hand=7, nb_cards=52, add_Agent=True):
    # Possibilités d'actions
    self.action_space = spaces.Discrete(nb_cards_hand)
    # Informations sur le jeu (carte actuelle, main actuelle, cartes jouées)
    self.observation_space = spaces.Tuple(
      (spaces.Discrete(nb_cards), spaces.Discrete(nb_cards_hand), spaces.Discrete(nb_cards))
    )


class PresidentAgent(Player):
  """
  Imported from OpenAI's Gym
  """
  environment = None

  def __init__(self, name, environment, learning_rate: float = 0.1, initial_epsilon: float = 0.5,
               epsilon_decay: float = 0.001, final_epsilon: float = 0.1,
               discount_factor: float = 0.95):
    """Initialize a Reinforcement Learning agent with an empty dictionary
    of state-action values (q_values), a learning rate and an epsilon.

    Args:
        learning_rate: The learning rate
        initial_epsilon: The initial epsilon value
        epsilon_decay: The decay for epsilon
        final_epsilon: The final epsilon value
        discount_factor: The discount factor for computing the Q-value
    """
    super().__init__(name)
    self.environment = environment
    self.q_values = defaultdict(lambda: np.zeros(self.environment.action_space.n))

    self.lr = learning_rate
    self.discount_factor = discount_factor

    self.epsilon = initial_epsilon
    self.epsilon_decay = epsilon_decay
    self.final_epsilon = final_epsilon

    self.current_reward = 0
    self.last_action = 0
    self.current_obs = None

    self.training_error = []

  def get_action(self, obs: tuple[int, List[int]]) -> int:
    """
    Returns the best action with probability (1 - epsilon)
    otherwise a random action with probability epsilon to ensure exploration.
    """

    if np.random.random() < self.epsilon:
      card_value = self.environment.action_space.sample()

    # with probability (1 - epsilon) act greedily (exploit)
    else:
      obs_tuple = (obs[0], tuple(obs[1]))
      card_value = int(np.argmax(self.q_values[obs_tuple]))

    self.current_obs = obs

    return card_value

  def step(self, played_cards):
    last_card = played_cards.cards[-1] if len(played_cards.cards) else 0
    # Player and self.played_cards is the observation in this context
    obs = (last_card, self.hand.cards)
    card = self.get_action(obs)
    self.last_action = card
    print("card value chosen : {}".format(card))

    try:
      if card not in self.hand.cards:
        raise InvalidCardException("Not in the hand !", 1)

      card_value = card % 13

      """
      if card is None:
        raise InvalidCardException("Card not valid : None.", 3)
      """

      # If card value < the last one, error for the agent
      if card_value < last_card % 13:
        raise InvalidCardException(
          "Carte {} plus basse que {}. Veuillez en choisir une autre.".format(get_card_string(card),
                                                                              get_card_string(last_card)), 2)

      # Little reward to be able to play a card
      self.current_reward += 1
      return card

    except InvalidCardException as e:
      # Essaye de jouer une carte qu'il ne peut pas => stop de l'épisode
      print("###################{} a fait une erreur : {}".format(self.name, e.__str__()))
      self.current_reward -= 10.0 if e.code == 2 else 15.0
      Results.savelog(e.code, self.current_reward)
      self.update(obs, card, self.current_reward, True, next_obs=None)
      raise e

  def update(
          self,
          obs: tuple[int, List[int]],
          action: int,
          reward: float,
          terminated: bool,
          next_obs: tuple[int, List[int]],
  ):
    """Updates the Q-value of an action."""
    future_q_value = (not terminated) * np.max(self.q_values[str(next_obs)])
    temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[str(obs)][action]
    )

    self.q_values[str(obs)][action] = (
            self.q_values[str(obs)][action] + self.lr * temporal_difference
    )
    self.training_error.append(temporal_difference)

    if terminated:
      self.current_reward = 0

  def decay_epsilon(self):
    self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)

  def check_convergence(self, threshold: float = 0.1, num_episodes: int = 100):
    last_n_errors = self.training_error[-num_episodes:]
    avg_error = sum(last_n_errors) / num_episodes

    if avg_error < threshold:
      print("Convergence reached.")
    else:
      print("Convergence not reached.")

    print(f"Average training error over the last {num_episodes} episodes: {avg_error}")

  def export(self, file_path: str):
    data = {
      "q_values": dict(self.q_values),
      "training_error": self.training_error,
      # "other_data": ...  # Ajoutez ici d'autres données importantes que vous souhaitez enregistrer
    }

    with open(file_path, "w") as f:
      json.dump(data, f)

class GreedPlayer(Player):
  pass
