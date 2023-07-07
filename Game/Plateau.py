import random

from Game.Deck import Deck, get_card_string
from Game.IA.PresidentEnvironment import PresidentAgent, GreedPlayer
from Game.Player import Player

from gymnasium import Env


class Plateau(Env):
  description = ""
  classement = []

  deck = None
  defausse = Deck()
  played_cards = Deck()

  players = []

  def __init__(self, players, description="", add_agent=False, environment=None):
    """
    :param players: name list of the players
    :param description: description to show
    :param add_Agent: if True, add an agent as a player named Bob
    """


    for name, type in players.items():
      if type == "Human":
        self.players.append(Player(name))
      elif type == "Greedy":
        self.players.append(GreedPlayer(name))
      elif type == "Learning":
        self.players.append(PresidentAgent(name, environment))

    self.description = description

  def ditribute_to_players(self, number_cards):
    print("Ditributing to players...")
    for i in range(number_cards):
      for player in self.players:
        card = self.deck.draw_card()
        player.add_card(card)

  def empty_played_cards(self):
    self.defausse.cards += self.played_cards.cards
    self.played_cards.cards = []

  def empty_player_cards(self):
    for player in self.players:
      player.empty_hand()

  def players_have_cards(self):
    """
    Returns if at least one player still have cards
    :return:
    """
    still_playing = False
    for player in self.players:
      if len(player.hand.cards):
        still_playing = True

    return still_playing

  def show(self, current_player, starting=False):
    """

    :param Player current_player:
    :return:
    """
    if not starting:
      print("Défausse : {} ({})".format(get_card_string(self.played_cards.cards[-1]), self.played_cards.cards[-1]))

    current_player.show_hand()

  def update_agents(self):
    for player in self.players:
      if player.__class__ == PresidentAgent:
        player.update()

