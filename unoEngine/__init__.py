from enum import Enum
from dataclasses import dataclass
from collections import deque
from random import shuffle
from pprint import pprint


class CardTypes(Enum):
    NUMBER_0 = 0
    NUMBER_1 = 1
    NUMBER_2 = 2
    NUMBER_3 = 3
    NUMBER_4 = 4
    NUMBER_5 = 5
    NUMBER_6 = 6
    NUMBER_7 = 7
    NUMBER_8 = 8
    NUMBER_9 = 9
    BLOCK = 10
    ROTATE = 11
    ADD2 = 12
    COLOR_SELECT = 13
    ADD4 = 14


class Colors(Enum):
    BLUE = 0
    GREEN = 1
    YELLOW = 2
    RED = 3
    BLACK = 4


class Directions(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


@dataclass()
class Rules:
    player_card_count = 7
    black_on_black = True
    zero_passes_on = True
    seven_swaps = True
    add_2_stackable = True
    add_4_challengeable = True
    draw_until_play = True
    mandatory_playing = True


@dataclass
class Card:
    color: Colors
    card_type: CardTypes

    def other_is_playable(self, other: 'Card', rules: Rules, previous_color_selection: Colors | None = None) -> bool:
        if self.card_type.value <= 11:
            return self.card_type == other.card_type or self.color == other.color or self.color == previous_color_selection
        if self.card_type == CardTypes.ADD2:
            return self.color == other.color or (other.card_type == CardTypes.ADD2 and rules.add_2_stackable)
        elif other.card_type.value <= 11:
            return True

        return rules.black_on_black

    def filter_playable_cards(self, deck: list['Card'], rules: Rules,
                              previous_color_selection: Colors | None = None) -> list['Card']:
        return list(filter(lambda card: self.other_is_playable(card, rules, previous_color_selection), deck))

    def __repr__(self):
        return f'Card({self.color.name}, {self.card_type.name})'


def get_standard_card_deck() -> list[Card]:
    card_deck: list[Card] = []

    for color in range(4):
        for card_type in range(1, 10):
            card_deck.append(Card(Colors(color), CardTypes(card_type)))

        card_deck.append(Card(Colors(color), CardTypes.BLOCK))
        card_deck.append(Card(Colors(color), CardTypes.ROTATE))
        card_deck.append(Card(Colors(color), CardTypes.ADD2))

    card_deck = card_deck * 2

    for color in range(4):
        card_deck.append(Card(Colors(color), CardTypes.NUMBER_0))

    card_deck += [Card(Colors.BLACK, CardTypes.COLOR_SELECT)] * 4
    card_deck += [Card(Colors.BLACK, CardTypes.ADD4)] * 4

    return card_deck


class Game:
    @property
    def current_player_deck(self) -> list[Card]:
        return self.player_decks[self.current_turn]

    @property
    def open_card(self):
        return self.open_deck[-1]

    def __init__(self, player_count: int, rules: Rules, deck: list[Card] | None = None):
        if deck is None:
            deck = get_standard_card_deck()
        self.closed_deck: deque[Card] = deque(deck)
        shuffle(self.closed_deck)

        self.open_deck: deque[Card] = deque([self.closed_deck.pop()])
        illegal_initial_card_types = [CardTypes.BLOCK, CardTypes.ROTATE, CardTypes.ADD2, CardTypes.ADD4,
                                      CardTypes.COLOR_SELECT]
        while self.open_deck[0].card_type in illegal_initial_card_types:
            self.open_deck[0] = self.closed_deck.pop()

        self.player_decks: list[list[Card]] = [[] for _ in range(player_count)]  # sorted clockwise

        for _ in range(rules.player_card_count):
            for player in range(player_count):
                self.player_decks[player].append(self.closed_deck.pop())

        self.rules = rules
        self.current_turn = 0
        self.direction = Directions.CLOCKWISE
        self.color_selection: Colors | None = None

    def _step_index(self, current: int, steps: int):
        return (current + steps) % len(self.player_decks)

    def _draw(self, player_index: int):
        self.player_decks[player_index].append(self.closed_deck.pop())

    def step(self, played_card_index: int | None, color_selection: Colors | None = None,
             swap_player_selection: int | None = None,
             add_4_challenged: bool = False, ) -> bool:
        """
        :param played_card_index: index of card played by current player. None if no card shall be played and instead a card should be drawn
        :param color_selection: a color except black must be given when played_card_index points to a card of type
        :param swap_player_selection: 
        :param add_4_challenged: 
        :return: True if card is playable or not playing is possible
        """
        if played_card_index is None:
            if self.rules.mandatory_playing and self.open_card.filter_playable_cards(self.current_player_deck, self.rules, self.color_selection):
                return False
            
            self._draw(self.current_turn)
            return True

        played_card = self.current_player_deck[played_card_index]

        if not self.open_card.other_is_playable(played_card, self.rules, self.color_selection):
            return False

        del self.current_player_deck[played_card_index]

        match played_card.card_type:
            case CardTypes.NUMBER_0 if self.rules.zero_passes_on:
                if self.direction == Directions.CLOCKWISE:
                    self.player_decks.insert(0, self.player_decks.pop())
                else:
                    begin = self.player_decks[0]
                    del self.player_decks[0]
                    self.player_decks.append(begin)

            case CardTypes.NUMBER_7 if self.rules.seven_swaps:
                if swap_player_selection == self.current_turn:
                    raise ValueError('swap player must be someone else')

                self.player_decks[self.current_turn], self.player_decks[swap_player_selection] \
                    = self.player_decks[swap_player_selection], self.player_decks[self.current_turn]

            case CardTypes.BLOCK:
                self.current_turn = self._step_index(self.current_turn, self.direction.value)

            case CardTypes.ROTATE:
                self.direction = Directions.CLOCKWISE if self.direction == Directions.COUNTERCLOCKWISE else Directions.COUNTERCLOCKWISE

            case CardTypes.ADD2:
                index = self._step_index(self.current_turn, self.direction.value)
                self._draw(index)
                self._draw(index)

            case CardTypes.COLOR_SELECT:
                if color_selection is None or color_selection == Colors.BLACK:
                    raise ValueError('color except black must be selected')
                self.color_selection = color_selection

            case CardTypes.ADD4:
                if color_selection is None or color_selection == Colors.BLACK:
                    raise ValueError('color except black must be selected')
                self.color_selection = color_selection

                if (add_4_challenged and
                    self.rules.add_4_challengeable and
                    self.open_card.filter_playable_cards(self.current_player_deck, self.rules, self.color_selection) # player could have played different cards
                ):
                    for _ in range(6):
                        self._draw(self.current_turn)
                else:
                    for _ in range(4):
                        self._draw(self._step_index(self.current_turn, self.direction.value))

        self.current_turn = self._step_index(self.current_turn, self.direction.value)

        return True

    @property
    def identities(self):
        return [id(i) for i in self.player_decks]


def main():
    game = Game(2, Rules())
    game.open_deck.append(Card(Colors.BLUE, CardTypes.NUMBER_5))

    game.player_decks[0][0] = Card(Colors.BLUE, CardTypes.NUMBER_7)

    print(game.player_decks)


if __name__ == '__main__':
    main()
