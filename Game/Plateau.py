import random

from Game.Deck import Deck, get_card_string
from Game.Player import Player

from gymnasium import Env

class Plateau(Env):
  description = ""
  classement = []

  deck = None
  defausse = Deck()

  players = []

  def __init__(self, players, description, add_Agent):
    """
    :param players: name list of the players
    :param description: description to show
    :param add_Agent: if True, add an agent as a player named Bob
    """
    self.deck = Deck(52)
    self.deck.shuffle_cards()

    for player_name in players:
      self.players.append(Player(player_name))

    if add_Agent:
      self.players.append(Player("Bob", is_agent=True))

    self.description = description

  def ditribute_to_players(self, number_cards):
    print("Ditributing to players...")
    for i in range(number_cards):
      for player in self.players:
        card = self.deck.draw_card()
        player.add_card(card)

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
      print("Défausse : {} ({})".format(get_card_string(self.defausse.cards[-1]), self.defausse.cards[-1]))

    current_player.show_hand()
