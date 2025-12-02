from scenes.road_intro import road_intro_scene
from entities.player import Player
from game_data import player_start_stats

player = Player(**player_start_stats, inventory={})

road_intro_scene(player)

