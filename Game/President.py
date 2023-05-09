from collections import Counter

from Game.Deck import get_card_string
from Game.Plateau import Plateau
from Game.Player import Player


class President(Plateau):
  def __init__(self):
    super().__init__(4, "Président")

  def players_have_cards(self):
    still_playing = False
    for player in self.players:
      if len(player.hand.cards):
        still_playing = True

    return still_playing

  def launch_game(self):
    player_id = 0
    while self.players_have_cards():
      print("------------ Nouveau tour !--------------")
      player_id = self.tour(player_id)

    print("Fin du jeu !")
    print("Président : {}".format(self.classement[0]))
    print("Trou duc : {}".format(self.classement[-1]))

  def tour(self, player_id=0):
    player = self.players[player_id]
    print("##########{} commence :###############".format(player))
    self.show(player, True)
    nb_cards = self.play_card(player, True)
    if nb_cards == 0:
      self.add_winner(player)
    last_played = player_id
    player_id = (player_id + 1) % len(self.players)

    didnt_play = 0
    while didnt_play <= len(self.players) - 2:
      player = self.players[player_id]
      print("##########Au tour de {} :###############".format(player))
      if self.can_play(player):
        self.show(player)
        nb_cards = self.play_card(player)
        didnt_play = 0
        if nb_cards == 0:
          self.add_winner(player)
        last_played = player_id
      else:
        print("{} ne peut pas jouer, il doit passer son tour !".format(player))
        didnt_play += 1

      player_id = (player_id + 1) % len(self.players)

    if not len(self.players[last_played].hand.cards):
      original_last_played = last_played
      last_played = (last_played + 1) % len(self.players)
      while last_played != original_last_played and not len(self.players[last_played].hand.cards):
        last_played = (last_played + 1) % len(self.players)

    print("Fin du tour.")
    return last_played

  def can_play(self, player, only=False):
    if not len(self.defausse.cards):
      return True

    if not len(player.hand.cards):
      return False

    defausse_value = self.defausse.cards[-1] % 13
    for card in player.hand.cards:
      if only and (card % 13) == defausse_value:
        return True
      elif (card % 13) >= defausse_value:
        return True

    return False

  def play_card(self, player, starting=False):
    """
    :param Player player:
    :return:
    """
    card = player.choose_card()

    if not starting:
      last_card = self.defausse.cards[-1]

      while card % 13 < last_card % 13:
        print("Carte {} plus basse que {}. Veuillez en choisir une autre.".format(get_card_string(card),
                                                                                  get_card_string(last_card)))
        card = player.choose_card()

    self.defausse.add_card(card)
    return player.remove_card(card)

  def add_winner(self, player):
    print("{} a fini son jeu ! Bien joué !")
    self.classement.append(player)
