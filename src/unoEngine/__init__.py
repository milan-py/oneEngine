from unoEngine.enums import *
from unoEngine.game import *


def main():
    g = Game(2, Rules())
    g.open_deck.append(Card(Colors.BLUE, CardTypes.NUMBER_5))

    g.player_decks[0][0] = Card(Colors.BLUE, CardTypes.NUMBER_7)

    print(g.player_decks)


if __name__ == '__main__':
    main()
