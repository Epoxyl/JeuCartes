from collections import Counter

from Game.Deck import get_card_string
from Game.IA.PresidentEnvironment import PresidentAgent
from Game.Plateau import Plateau
from Game.Player import Player
from Game.Utils.Exceptions import InvalidCardException


class President(Plateau):
  def __init__(self, players):
    super().__init__(players, "Président")
    self.ditribute_to_players(7)

  def launch_game(self):
    """
    One game of a president. We launch "tours" while players have cards, and start a new one each time nobody can play.
    :return:
    """
    player_id = 0
    while self.players_have_cards():
      print("------------ Nouveau tour !--------------")
      player_id = self.tour(player_id)

    print("Fin du jeu !")
    print("Président : {}".format(self.classement[0]))
    print("Trou duc : {}".format(self.classement[-1]))

  def tour(self, player_id=0):
    """
    Game tour, while at least two players can play. Starts with the last player who finished previous tour, or the one next to him if he has no cards left.

    :param player_id: Id of the player to start the tour
    :return:
    """
    player = self.players[player_id]
    print("##########{} commence :###############".format(player))
    self.show(player, True)

    if player.__class__ == PresidentAgent:
      print("here")
      player.get_action(self)
    else:
      # Player and self.defausse is the observation in this context. player_choose_card is the get_action function in this context
      card = self.player_choose_card(player)

      # card is the action in this context. play_card is the step function in this context
      nb_cards = self.play_card(player, card)
      if nb_cards == 0:
        self.add_winner(player)

    last_played = player_id
    player_id = (player_id + 1) % len(self.players)

    didnt_play = 0
    # We continue while at least 2 players are still playing
    while len(self.players) - didnt_play >= 2:
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
    """
    Returns if a player can play currently
    :param player: Current player to play
    :param only: if True, the player has to play only the current card ("xxx ou rien")
    :return:
    """
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

  def player_choose_card(self, player, starting=False):
    """
    Make the player (AI or human) choose a card to play. Observations are the player's hand and the defausse.
    :param player:
    :param starting: The playter is starting the round
    :return: Played card
    """
    card = player.choose_card()

    if not starting:
      last_card = self.defausse.cards[-1]

      if player.is_agent and card % 13 < last_card % 13:
        raise InvalidCardException(
          "Carte {} plus basse que {}. Veuillez en choisir une autre.".format(get_card_string(card),
                                                                              get_card_string(last_card)))

      while card % 13 < last_card % 13:
        print("Carte {} plus basse que {}. Veuillez en choisir une autre.".format(get_card_string(card),
                                                                                  get_card_string(last_card)))
        card = player.choose_card()

    return card

  def play_card(self, player, card):
    """
    :param Player player:
    :return:
    """

    self.defausse.add_card(card)
    new_hand_length = player.remove_card(card)
    return new_hand_length

  def add_winner(self, player):
    print("{} a fini son jeu ! Bien joué !")
    self.classement.append(player)

  def _get_obs(self, player):
    last_card = self.defausse.cards[-1] if len(self.defausse.cards) else 0
    return [player.hand, last_card]  # todo: Add played cards
