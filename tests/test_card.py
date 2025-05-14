import pytest
from unoEngine import Card, Colors, CardTypes, Rules
from itertools import product

for_all_rules = pytest.mark.parametrize(
    'black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable, draw_until_play, mandatory_playing',
    list(product([False, True], repeat=7))
)


@for_all_rules
def test_playable_number_cards(black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                               draw_until_play, mandatory_playing):
    rules = Rules(7, black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                  draw_until_play, mandatory_playing)

    assert Card(Colors.BLUE, CardTypes.NUMBER_0).other_is_playable(
        Card(Colors.BLUE, CardTypes.NUMBER_7), rules=rules)

    assert Card(Colors.BLUE, CardTypes.NUMBER_0).other_is_playable(
        Card(Colors.GREEN, CardTypes.NUMBER_0), rules=rules)

    assert Card(Colors.BLUE, CardTypes.NUMBER_0).other_is_playable(Card(
        Colors.BLUE, CardTypes.NUMBER_0), rules=rules)

    assert not Card(Colors.BLUE, CardTypes.NUMBER_0).other_is_playable(Card(
        Colors.GREEN, CardTypes.NUMBER_7), rules=rules)


@for_all_rules
def test_playable_black_on_black(black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                                 draw_until_play, mandatory_playing):
    rules = Rules(7, black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                  draw_until_play, mandatory_playing)

    assert Card(Colors.BLACK, CardTypes.COLOR_SELECT).other_is_playable(
        Card(Colors.BLACK, CardTypes.COLOR_SELECT), rules=rules, previous_color_selection=Colors.RED) is black_on_black

    assert Card(Colors.BLACK, CardTypes.COLOR_SELECT).other_is_playable(
        Card(Colors.BLACK, CardTypes.ADD4), rules=rules, previous_color_selection=Colors.RED) is black_on_black

    assert Card(Colors.BLACK, CardTypes.ADD4).other_is_playable(
        Card(Colors.BLACK, CardTypes.COLOR_SELECT), rules=rules, previous_color_selection=Colors.RED) is black_on_black

    assert Card(Colors.BLACK, CardTypes.ADD4).other_is_playable(
        Card(Colors.BLACK, CardTypes.ADD4), rules=rules, previous_color_selection=Colors.RED) is black_on_black


@for_all_rules
def test_playable_colored_card_on_black(black_on_black, zero_passes_on, seven_swaps, add_2_stackable,
                                        add_4_challengeable, draw_until_play, mandatory_playing):
    rules = Rules(7, black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                  draw_until_play, mandatory_playing)

    assert Card(Colors.BLACK, CardTypes.COLOR_SELECT).other_is_playable(Card(Colors.GREEN, CardTypes.ROTATE),
                                                                        rules=rules,
                                                                        previous_color_selection=Colors.GREEN)


@for_all_rules
def test_playable_add2_on_number_card(black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                                      draw_until_play, mandatory_playing):
    rules = Rules(7, black_on_black, zero_passes_on, seven_swaps, add_2_stackable, add_4_challengeable,
                  draw_until_play, mandatory_playing)

    assert Card(Colors.GREEN, CardTypes.NUMBER_1).other_is_playable(
        Card(Colors.GREEN, CardTypes.ADD2), rules=rules)

    assert not Card(Colors.BLUE, CardTypes.NUMBER_1).other_is_playable(
        Card(Colors.GREEN, CardTypes.ADD2), rules=rules)

    assert Card(Colors.BLACK, CardTypes.ADD4).other_is_playable(
        Card(Colors.GREEN, CardTypes.ADD2), rules=rules, previous_color_selection=Colors.GREEN)

    assert not Card(Colors.BLACK, CardTypes.ADD4).other_is_playable(
        Card(Colors.GREEN, CardTypes.ADD2), rules=rules, previous_color_selection=Colors.RED)

    assert Card(Colors.BLUE, CardTypes.ADD2).other_is_playable(
        Card(Colors.GREEN, CardTypes.ADD2), rules=rules) is add_2_stackable

    assert Card(Colors.BLUE, CardTypes.ADD2).other_is_playable(
        Card(Colors.GREEN, CardTypes.ADD2), rules=rules) is add_2_stackable
