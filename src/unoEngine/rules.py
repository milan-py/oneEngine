from dataclasses import dataclass


@dataclass()
class Rules:
    player_card_count: int = 7
    black_on_black: bool = True
    zero_passes_on: bool = True
    seven_swaps: bool = True
    add_2_stackable: bool = True
    add_4_challengeable: bool = True
    draw_until_play: bool = True
    mandatory_playing: bool = True
