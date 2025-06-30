from dataclasses import dataclass

from oneEngine.enums import Color, CardType
from oneEngine.rules import Rules


@dataclass(frozen=True)
class Card:
    color: Color
    card_type: CardType

    def __post_init__(self):
        if self.color is Color.BLACK and self.card_type not in (CardType.COLOR_SELECT, CardType.ADD4):
            raise ValueError(f'Card of type {self.card_type} cannot be black')
        elif self.card_type in (CardType.COLOR_SELECT, CardType.ADD4) and self.color is not Color.BLACK:
            raise ValueError(f'Card of type {self.card_type} must be black')

    def other_is_playable(self, other: 'Card', rules: Rules, previous_color_selection: Color | None = None) -> bool:
        """
        determines whether a given card can be played on top self.
        :param other: other card that shall be stacked on self.
        :param rules: rules applying to the game.
        :param previous_color_selection: must be given if self is black and therefore a color has been selected.
        :return: True if other can be stacked on self.
        """
        if self.card_type.value <= 11:
            return self.card_type == other.card_type or self.color is other.color or other.color is Color.BLACK

        if self.card_type is CardType.ADD2:
            return (self.color is other.color and other.card_type is not CardType.ADD2) or (
                    other.card_type is CardType.ADD2 and rules.add_2_stackable)

        if self.color is Color.BLACK:
            return other.color is previous_color_selection or (other.color is Color.BLACK and rules.black_on_black)

        return rules.black_on_black

    def filter_playable_cards(self, deck: list['Card'], rules: Rules,
                              previous_color_selection: Color | None = None) -> list['Card']:
        """
        :param deck: list of cards that should be filtered
        :param rules: rules applying to the game.
        :param previous_color_selection: must be given if self is black and therefore a color has been selected.
        :return: list of cards that can be stacked on self.
        """
        return [card for card in deck if self.other_is_playable(card, rules, previous_color_selection)]

    def __repr__(self):
        return f'Card(Color.{self.color.name}, CardType.{self.card_type.name})'


def get_standard_card_deck() -> list[Card]:
    """
    :return: standard uno deck, see: https://de.m.wikipedia.org/wiki/Datei:UNO_cards_deck.svg
    """
    card_deck: list[Card] = []

    for color in range(4):
        for card_type in range(1, 10):
            card_deck.append(Card(Color(color), CardType(card_type)))

        card_deck.append(Card(Color(color), CardType.BLOCK))
        card_deck.append(Card(Color(color), CardType.ROTATE))
        card_deck.append(Card(Color(color), CardType.ADD2))

    card_deck = card_deck * 2

    for color in range(4):
        card_deck.append(Card(Color(color), CardType.NUMBER_0))

    card_deck += [Card(Color.BLACK, CardType.COLOR_SELECT)] * 4
    card_deck += [Card(Color.BLACK, CardType.ADD4)] * 4

    return card_deck
