from prettytable import PrettyTable

from Game.Deck import get_card_string, Deck
from Game.Utils.Exceptions import InvalidCardException


class Player:
  name = ""

  # Deck hand of the player
  hand = None

  def __init__(self, name="User"):
    self.name = name
    self.hand = Deck()

  def __str__(self):
    return self.name

  def add_card(self, card):
    self.hand.add_card(card)
    return len(self.hand.cards)

  def remove_card_by_index(self, card_index):
    card = self.hand.draw_card(card_index)
    return len(self.hand.cards)

  def remove_card(self, card):
    """
    Remove a card from the hand of the player
    :param card: card value to remove
    :return: length of the hand
    """
    print(card)
    if not card in self.hand.cards:
      raise Exception("error : card not in hand !")

    self.hand.pick_card(card)
    return len(self.hand.cards)

  def empty_hand(self):
    self.hand.cards = []

  def hand_values(self):
    return self.hand.values()

  def show_hand(self):
    table = PrettyTable()
    table.field_names = [i + 1 for i in range(len(self.hand.cards))]

    table.add_row([get_card_string(card) for card in self.hand.cards])
    print(table)

  def choose_card(self):
    """
    Choose a card in the player's hand, by input.
    :return: the card played
    :raise: InvalidCardException if agent and not the right index (else it will wait for a new input)
    """
    print("Veuillez choisir la carte à jouer...")
    card_index = int(input()) - 1

    while card_index >= len(self.hand.cards) or card_index < 0:
      print("Erreur dans la saisie de votre carte. Veuillez choisir le numéro de la carte entre 1 et {}".format(
        len(self.hand.cards)))
      card_index = int(input()) - 1

    return self.hand.cards[card_index]
