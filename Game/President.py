from collections import Counter

from Game.Deck import get_card_string, Deck
from Game.IA.PresidentEnvironment import PresidentAgent, GreedPlayer
from Game.Plateau import Plateau
from Game.Player import Player
from Game.Utils.Exceptions import InvalidCardException
from Game.__main__ import Results


class President(Plateau):
  agents_reward = [20, 10, 5, 1]

  def __init__(self, players, add_agent=False, environment=None):
    super().__init__(players, "Président", add_agent, environment)

  def launch_game(self):
    """
    One game of a president. We launch "tours" while players have cards, and start a new one each time nobody can play.
    :return:
    """
    self.classement = []

    self.deck = Deck(52)
    self.deck.shuffle_cards()

    self.empty_player_cards()
    self.empty_played_cards()
    self.ditribute_to_players(7)

    player_id = 0
    while self.players_have_cards():
      print("------------ Nouveau tour !--------------")
      while not len(self.players[player_id].hand_values()):
        player_id = (player_id + 1) % len(self.players)
      player_id = self.tour(player_id)
      print("------------ Fin du tour !--------------")

    print("Fin du jeu !")
    print("Président : {}".format(self.classement[0]))
    print("Trou duc : {}".format(self.classement[-1]))

  def launch_training_game(self):
    self.classement = []

    self.deck = Deck(52)

    self.empty_player_cards()
    self.empty_played_cards()
    self.ditribute_to_players(7)

    player_id = 0
    while self.players_have_cards():
      print("------------ Nouveau tour !--------------")
      while not len(self.players[player_id].hand_values()):
        player_id = (player_id + 1) % len(self.players)
      player_id = self.tour(player_id)
      print("------------ Fin du tour !--------------")

    print("Fin du jeu !")
    print("Président : {}".format(self.classement[0]))
    print("Trou duc : {}".format(self.classement[-1]))

  def tour(self, player_id=0):
    """
    Game tour, while at least two players can play. Starts with the last player who finished previous tour, or the one next to him if he has no cards left.

    :param player_id: Id of the player to start the tour
    :return:
    """
    self.empty_played_cards()

    player = self.players[player_id]
    print("##########{} commence :###############".format(player))
    self.show(player, True)

    # Different actions depending on if agent or human
    if player.__class__ == PresidentAgent:
      card = player.step(self.played_cards)
    else:
      card = self.player_choose_card(player)

    nb_cards = self.play_card(player, card)
    if nb_cards == 0:
      if self.add_winner(player):
        return player_id

    last_played = player_id
    player_id = (player_id + 1) % len(self.players)

    didnt_play = 0
    # We continue while at least 2 players are still playing
    while len(self.players) - didnt_play >= 2:
      player = self.players[player_id]
      print("##########Au tour de {} :###############".format(player))
      if self.can_play(player):
        self.show(player)
        # Different actions depending on if agent or human
        if player.__class__ == PresidentAgent:
          card = player.step(self.played_cards)
        else:
          card = self.player_choose_card(player)

        nb_cards = self.play_card(player, card)
        if nb_cards == 0:
          if self.add_winner(player):
            return player_id

        didnt_play = 0
        last_played = player_id
      else:
        print("{} ne peut pas jouer ou a déjà fini, il doit passer son tour !".format(player))
        didnt_play += 1

      player_id = (player_id + 1) % len(self.players)

    if not len(self.players[last_played].hand.cards):
      original_last_played = last_played
      last_played = (last_played + 1) % len(self.players)
      while last_played != original_last_played and not len(self.players[last_played].hand.cards):
        last_played = (last_played + 1) % len(self.players)

    return last_played

  def can_play(self, player, only=False):
    """
    Returns if a player can play currently
    :param player: Current player to play
    :param only: if True, the player has to play only the current card ("xxx ou rien")
    :return:
    """
    if not len(self.played_cards.cards):
      return True

    if not len(player.hand.cards):
      return False

    last_card_value = self.played_cards.cards[-1] % 13 if len(self.played_cards.cards) else 0

    for card in player.hand.cards:
      if only and (card % 13) == last_card_value:
        return True
      elif (card % 13) >= last_card_value:
        return True

    return False

  def player_choose_card(self, player, starting=False):
    """
    Make the player (AI or human) choose a card to play. Observations are the player's hand and the played_cards.
    :param player:
    :param starting: The playter is starting the round
    :return: Played card
    """

    last_card = self.played_cards.cards[-1] if len(self.played_cards.cards) else 0

    if player.__class__ == GreedPlayer:
      ecart = 14
      played_card = player.hand.cards[0]
      for card in player.hand.cards:
        if 0 <= card % 13 - last_card % 13 < ecart:
          played_card = card
          ecart = card % 13 - last_card % 13

      return played_card
    else:
      card = player.choose_card()

      if not starting:
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

    print(card)
    self.played_cards.add_card(card)
    new_hand_length = player.remove_card(card)
    return new_hand_length

  def add_winner(self, player):
    """
    Returns : if the winner is president
    :param player:
    :return:
    """
    print("{} a fini son jeu ! Bien joué !".format(player.name))
    self.classement.append(player)
    if player.__class__ == PresidentAgent:
      print(len(self.classement))
      print(len(self.agents_reward))
      player.current_reward += self.agents_reward[len(self.classement) - 1]
      Results.savelog(0, player.current_reward)
      player.update(player.current_obs, player.last_action, player.current_reward, True, next_obs=None)
    return len(self.classement) == 1

  def _get_obs(self, player):
    last_card = self.played_cards.cards[-1] if len(self.played_cards.cards) else 0
    return [player.hand, last_card]  # todo: Add played cards
