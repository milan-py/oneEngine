from random import seed

import pytest

from unoEngine import Card, Colors, CardTypes, Game, Rules


@pytest.mark.parametrize(
    'zero_passes_on,expected', [
        (True, True),
        (False, False)
    ]
)
def test_zero_passes_on_rule(zero_passes_on, expected):
    seed(1)

    g = Game(3, Rules(zero_passes_on=zero_passes_on))
    assert g.step(2)  # Player 0, Green 4
    assert g.step(0, color_selection=Colors.GREEN)  # Player 1, Color select
    assert g.step(4)  # Player 2, Green 3
    assert g.current_turn == 0
    assert g.step(2)  # Player 0, Green 1
    assert g.step(3)  # Player 1, Green 1
    player1_deck = g.player_decks[1]
    assert g.step(0)  # Player 2, Green 0
    assert (player1_deck == g.player_decks[2]) is expected  # shifted with 0 if zero_passes_on applies
    assert g.open_card == Card(Colors.GREEN, CardTypes.NUMBER_0)


@pytest.mark.parametrize(
    'challenge_add_4,challenge_success', [
        (True, True),
        (False, False)
    ]
)
def test_challenge_rule(challenge_add_4, challenge_success):
    from random import seed
    seed(1)

    g = Game(3, Rules())
    assert g.step(2)  # Player 0, Green 4
    player1_card_count = len(g.player_decks[1])
    player2_card_count = len(g.player_decks[2])
    assert g.step(2, color_selection=Colors.RED,
                  add_4_challenged=challenge_add_4)  # Player 1, add4, challenged by Player 2
    assert g.step(None)  # Player 2, draws
    assert (len(g.player_decks[1]) == player1_card_count + 5 and len(
        g.player_decks[2]) == player2_card_count + 1) is challenge_success
    assert (len(g.player_decks[1]) == player1_card_count - 1 and len(
        g.player_decks[2]) == player2_card_count + 5) is not challenge_success
