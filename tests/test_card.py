from itertools import product

import pytest

from oneEngine import Card, Color, CardType, Rules

for_all_rules = pytest.mark.parametrize(
    'black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable, draw_until_play, mandatory_playing',
    list(product([False, True], repeat=7))
)


@for_all_rules
def test_playable_number_cards(black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                               draw_until_play, mandatory_playing):
    rules = Rules(7, black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                  draw_until_play, mandatory_playing)

    assert Card(Color.BLUE, CardType.NUMBER_0).other_is_playable(
        Card(Color.BLUE, CardType.NUMBER_7), rules=rules)

    assert Card(Color.BLUE, CardType.NUMBER_0).other_is_playable(
        Card(Color.GREEN, CardType.NUMBER_0), rules=rules)

    assert Card(Color.BLUE, CardType.NUMBER_0).other_is_playable(Card(
        Color.BLUE, CardType.NUMBER_0), rules=rules)

    assert not Card(Color.BLUE, CardType.NUMBER_0).other_is_playable(Card(
        Color.GREEN, CardType.NUMBER_7), rules=rules)


@for_all_rules
def test_playable_black_on_black(black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                                 draw_until_play, mandatory_playing):
    rules = Rules(7, black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                  draw_until_play, mandatory_playing)

    assert Card(Color.BLACK, CardType.COLOR_SELECT).other_is_playable(
        Card(Color.BLACK, CardType.COLOR_SELECT), rules=rules, previous_color_selection=Color.RED) is black_on_black

    assert Card(Color.BLACK, CardType.COLOR_SELECT).other_is_playable(
        Card(Color.BLACK, CardType.ADD4), rules=rules, previous_color_selection=Color.RED) is black_on_black

    assert Card(Color.BLACK, CardType.ADD4).other_is_playable(
        Card(Color.BLACK, CardType.COLOR_SELECT), rules=rules, previous_color_selection=Color.RED) is black_on_black

    assert Card(Color.BLACK, CardType.ADD4).other_is_playable(
        Card(Color.BLACK, CardType.ADD4), rules=rules, previous_color_selection=Color.RED) is black_on_black


@for_all_rules
def test_playable_colored_card_on_black(black_on_black, zero_passes_on, seven_swaps, add_2_stackable,
                                        add_4_challengeable, draw_until_play, mandatory_playing):
    rules = Rules(7, black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                  draw_until_play, mandatory_playing)

    assert Card(Color.BLACK, CardType.COLOR_SELECT).other_is_playable(Card(Color.GREEN, CardType.ROTATE),
                                                                      rules=rules,
                                                                      previous_color_selection=Color.GREEN)


@for_all_rules
def test_playable_add2_on_number_card(black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                                      draw_until_play, mandatory_playing):
    rules = Rules(7, black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                  draw_until_play, mandatory_playing)

    assert Card(Color.GREEN, CardType.NUMBER_1).other_is_playable(
        Card(Color.GREEN, CardType.ADD2), rules=rules)

    assert not Card(Color.BLUE, CardType.NUMBER_1).other_is_playable(
        Card(Color.GREEN, CardType.ADD2), rules=rules)

    assert Card(Color.BLACK, CardType.ADD4).other_is_playable(
        Card(Color.GREEN, CardType.ADD2), rules=rules, previous_color_selection=Color.GREEN)

    assert not Card(Color.BLACK, CardType.ADD4).other_is_playable(
        Card(Color.GREEN, CardType.ADD2), rules=rules, previous_color_selection=Color.RED)

    assert Card(Color.BLUE, CardType.ADD2).other_is_playable(
        Card(Color.GREEN, CardType.ADD2), rules=rules) is add_2_stackable

    assert Card(Color.BLUE, CardType.ADD2).other_is_playable(
        Card(Color.GREEN, CardType.ADD2), rules=rules) is add_2_stackable


@pytest.mark.parametrize(
    'color, card_type, exception_expected',
    [
        (Color.GREEN, CardType.ROTATE, False),
        (Color.BLUE, CardType.ADD2, False),
        (Color.BLACK, CardType.ADD4, False),
        (Color.BLACK, CardType.COLOR_SELECT, False),
        (Color.BLACK, CardType.ROTATE, True),
        (Color.BLACK, CardType.ADD2, True),
        (Color.RED, CardType.ADD4, True),
        (Color.YELLOW, CardType.COLOR_SELECT, True),
    ]
)
def test_color_validation(color, card_type, exception_expected):
    if exception_expected:
        with pytest.raises(ValueError):
            Card(color, card_type)
    else:
        Card(color, card_type)
