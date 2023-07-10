import random

cards_value = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "valet", "dame", "roi", "as"]


def get_card_string(card):
  return cards_value[card % 13] + "(" + str(card) + ")"


class Deck:
  cards = None

  def __init__(self, nb_cards=0):
    self.cards = []

    for i in range(1, nb_cards + 1):
      self.cards.append(i)

  def values(self):
    return [card % 13 for card in self.cards]

  def shuffle_cards(self):
    random.shuffle(self.cards)

  def draw_card(self, card_index=0):
    if card_index > len(self.cards):
      raise Exception("error : card_index too big ({})".format(card_index))

    card = self.cards.pop(card_index)
    return card

  def pick_card(self, card):
    card_index = self.cards.index(card)
    if card_index is None:
      raise Exception("error : card not found ({})".format(card))

    return self.draw_card(card_index)

  def add_card(self, card):
    self.cards.append(card)

  def sort(self):
    # todo : optimiser algo de tri
    new_cards = []
    for card in self.cards:
      print(card)
      print(new_cards)
      i = 0
      while len(new_cards) and i < len(new_cards) and (card % 13) > (new_cards[i] % 13):
        i += 1
      print(i)
      new_cards.insert(i, card)

    self.cards = new_cards
