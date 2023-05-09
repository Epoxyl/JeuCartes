import random

from Game.Deck import Deck, get_card_string
from Game.Player import Player

class Plateau:
  description = ""
  classement = []

  deck = None
  defausse = Deck()

  players = []

  def __init__(self, nb_players, description):
    self.deck = Deck(52)
    self.deck.shuffle_cards()

    self.players.append(Player("Alexandre"))
    self.players.append(Player("Antoine"))
    self.players.append(Player("Julien"))
    self.players.append(Player("Yohann"))

    self.description = description

    self.ditribute_to_players(7)

  def ditribute_to_players(self, number_cards):
    print("Ditributing to players...")
    for i in range(number_cards):
      for player in self.players:
        card = self.deck.draw_card()
        player.add_card(card)

  def show(self, current_player, starting=False):
    """

    :param Player current_player:
    :return:
    """
    if not starting:
      print("Défausse : {} ({})".format(get_card_string(self.defausse.cards[-1]), self.defausse.cards[-1]))

    current_player.show_hand()
