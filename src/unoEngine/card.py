from dataclasses import dataclass

from unoEngine.enums import *
from unoEngine.rules import Rules


@dataclass
class Card:
    color: Colors
    card_type: CardTypes

    def other_is_playable(self, other: 'Card', rules: Rules, previous_color_selection: Colors | None = None) -> bool:
        """
        determines whether a given card can be played on top self.
        :param other: other card that shall be stacked on self.
        :param rules: rules applying to the game.
        :param previous_color_selection: must be given if self is black and therefore a color has been selected.
        :return: True if other can be stacked on self.
        """
        if self.card_type.value <= 11:
            return self.card_type == other.card_type or self.color == other.color or other.color == Colors.BLACK

        if self.card_type == CardTypes.ADD2:
            return (self.color == other.color and other.card_type != CardTypes.ADD2) or (
                    other.card_type == CardTypes.ADD2 and rules.add_2_stackable)

        if self.color == Colors.BLACK:
            return other.color == previous_color_selection or (other.color == Colors.BLACK and rules.black_on_black)

        return rules.black_on_black

    def filter_playable_cards(self, deck: list['Card'], rules: Rules,
                              previous_color_selection: Colors | None = None) -> list['Card']:
        """
        :param deck: list of cards that should be filtered
        :param rules: rules applying to the game.
        :param previous_color_selection: must be given if self is black and therefore a color has been selected.
        :return: list of cards that can be stacked on self.
        """
        return [card for card in deck if self.other_is_playable(card, rules, previous_color_selection)]

    def __repr__(self):
        return f'Card(Colors.{self.color.name}, CardTypes.{self.card_type.name})'


def get_standard_card_deck() -> list[Card]:
    """
    :return: standard uno deck see: https://de.m.wikipedia.org/wiki/Datei:UNO_cards_deck.svg
    """
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
