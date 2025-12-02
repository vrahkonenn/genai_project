from scenes.road_intro import road_intro_scene
from scenes.village import village_scene
from scenes.forest import forest_scene
from scenes.cave import cave_scene

SCENES = {
    "road_intro": road_intro_scene,
    "village": village_scene,
    "forest": forest_scene,
    "cave": cave_scene,
}

def run_scene(scene_name, world_state, player):
    scene_func = SCENES[scene_name]
    next_scene = scene_func(world_state, player)
    return next_scene
