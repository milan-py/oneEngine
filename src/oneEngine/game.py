from collections import deque
from random import shuffle

from oneEngine.card import Card, get_standard_card_deck
from oneEngine.enums import CardType, Color, Directions
from oneEngine.rules import Rules


class GameStop(Exception):
    def __init__(self):
        super().__init__()


class Game:
    @property
    def current_player_deck(self) -> list[Card]:
        return self.player_decks[self.current_turn]

    @property
    def open_card(self):
        """
        :return: last card of self.open_deck (i.e. most upper card)
        """
        return self.open_deck[-1]

    def __init__(self, player_count: int, rules: Rules, deck: list[Card] | None = None):
        """
        :param player_count:
        :param rules:
        :param deck: list of cards that should be used in the game. get_standard_card_deck() used if None.
        """
        if deck is None:
            deck = get_standard_card_deck()
        self.closed_deck: deque[Card] = deque(deck)
        shuffle(self.closed_deck)

        self.open_deck: deque[Card] = deque([self.closed_deck.pop()])
        illegal_initial_card_types = [CardType.BLOCK, CardType.ROTATE, CardType.ADD2, CardType.ADD4,
                                      CardType.COLOR_SELECT]
        while self.open_deck[0].card_type in illegal_initial_card_types:
            self.open_deck[0] = self.closed_deck.pop()

        self.player_decks: list[list[Card]] = [[] for _ in range(player_count)]  # sorted clockwise

        for _ in range(rules.player_card_count):
            for player in range(player_count):
                self.player_decks[player].append(self.closed_deck.pop())

        self.rules = rules
        self.current_turn: int = 0
        self.direction = Directions.CLOCKWISE
        self.color_selection: Color | None = None

    def step_index(self, current: int, steps: int) -> int:
        """
        :param current: starting point
        :param steps: number of steps taken in clockwise direction.
        :return: index after taking steps from current.
        """
        return (current + steps) % len(self.player_decks)

    def _draw(self, player_index: int):
        self.player_decks[player_index].append(self.closed_deck.pop())

    def _raise_step_exception(self, message: str, played_card_index: int, played_card: Card):
        self.current_player_deck.insert(played_card_index, played_card)  # inserts removed card again
        raise ValueError(message)

    def step(self, played_card_index: int | None, color_selection: Color | None = None,
             swap_player_selection: int | None = None,
             add_4_challenged: bool = False, ) -> bool:
        """
        :param played_card_index: index of card played by current player. None if no card shall be played and instead a card should be drawn
        :param color_selection: a color except black must be given when played_card_index points to a card of type.
        :param swap_player_selection:
        :param add_4_challenged:
        :raises GameStop: raised when game stopped (i.e. no one has at least one card).
        :return: True if move is allowed.
        """
        if played_card_index is None:  # draw is attempted
            if self.rules.mandatory_playing and self.open_card.filter_playable_cards(self.current_player_deck,
                                                                                     self.rules, self.color_selection):
                return False

            self._draw(self.current_turn)

            if not self.closed_deck:  # reshuffles when closed deck is empty
                print('SHUFFLING')
                shuffle(self.open_deck)
                self.closed_deck = self.open_deck.copy()
                self.open_deck = []

            if not self.rules.draw_until_play:
                self.current_turn = self.step_index(self.current_turn, self.direction.value)
            return True

        played_card = self.current_player_deck[played_card_index]

        if not self.open_card.other_is_playable(played_card, self.rules, self.color_selection):
            return False

        del self.current_player_deck[played_card_index]

        match played_card.card_type:
            case CardType.NUMBER_0 if self.rules.zero_passes_on:
                if self.direction is Directions.CLOCKWISE:
                    self.player_decks.insert(0, self.player_decks.pop())
                else:
                    begin = self.player_decks[0]
                    del self.player_decks[0]
                    self.player_decks.append(begin)

            case CardType.NUMBER_7 if self.rules.seven_swaps:
                if swap_player_selection == self.current_turn or swap_player_selection is None:
                    self._raise_step_exception('swap player must be someone else', played_card_index, played_card)
                    return False

                self.player_decks[self.current_turn], self.player_decks[swap_player_selection] \
                    = self.player_decks[swap_player_selection], self.player_decks[self.current_turn]

            case CardType.BLOCK:
                self.current_turn = self.step_index(self.current_turn, self.direction.value)

            case CardType.ROTATE:
                self.direction = Directions.CLOCKWISE if self.direction is Directions.COUNTERCLOCKWISE else Directions.COUNTERCLOCKWISE

            case CardType.ADD2:
                index = self.step_index(self.current_turn, self.direction.value)
                self._draw(index)
                self._draw(index)

            case CardType.COLOR_SELECT:
                if color_selection is None or color_selection is Color.BLACK:
                    self._raise_step_exception('color except black must be selected', played_card_index, played_card)
                    return False
                self.color_selection = color_selection

            case CardType.ADD4:
                if color_selection is None or color_selection is Color.BLACK:
                    self._raise_step_exception('color except black must be selected', played_card_index, played_card)
                    return False
                self.color_selection = color_selection

                if (add_4_challenged and self.rules.add_4_challengeable and self.open_card.filter_playable_cards(
                        self.current_player_deck, self.rules,
                        self.color_selection
                )):  # player could have played different cards
                    for _ in range(6):
                        self._draw(self.current_turn)
                else:
                    for _ in range(4):
                        self._draw(self.step_index(self.current_turn, self.direction.value))

        self.current_turn = self.step_index(self.current_turn, self.direction.value)

        if not any(self.player_decks):
            raise GameStop()

        while not self.current_player_deck:  # skips players with no cards.
            self.current_turn = self.step_index(self.current_turn, 1)

        self.open_deck.append(played_card)

        if not any(self.player_decks):
            raise GameStop()

        if played_card.color != Color.BLACK:
            self.color_selection = None

        return True
