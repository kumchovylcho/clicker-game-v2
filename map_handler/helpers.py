import os

from map_handler.monster import Monster
import pygame as pg


def get_monsters_on_chosen_map(map_name: str):
    """
    :return: list of monster objects for the given map
    """
    monsters = []
    directory_path = 'images/monsters'
    for map_n in os.listdir(directory_path):
        if map_n != map_name:
            continue

        file_path = os.path.join(directory_path, map_n)
        for file in os.listdir(file_path):
            image_path = os.path.join(file_path, file)
            monster_img = pg.image.load(image_path).convert_alpha()

            monsters.append(Monster(monster_img, 0))

        return monsters

    if not monsters:
        raise ValueError(f"Invalid map name. {map_name} is non existent.")


def get_all_map_names():
    directory_path = 'images/map_backgrounds'

    return [map_name.split(".")[0] for map_name in os.listdir(directory_path)]


def get_map_images():
    """
    :return: [Surface object, ...]
    """
    directory_path = 'images/map_backgrounds'

    images = []
    for bg in os.listdir(directory_path):
        bg_path = os.path.join(directory_path, bg)

        images.append(pg.image.load(bg_path).convert_alpha())

    return images


def get_number_of_monsters_on_every_map():
    directory_path = 'images/monsters/desert'

    return len(os.listdir(directory_path))


def get_bridge_to_platforms():
    """
    :return: {hell: Surface object, ...}
    """
    directory_path = 'images/platforms'

    bridge = {}
    for platform_name in os.listdir(directory_path):
        name = platform_name.split(".")[0]
        platform_img = pg.image.load(f"{directory_path}/{platform_name}").convert_alpha()

        bridge[name] = platform_img

    return bridge


def get_platform_positions():
    """
    :return: {map_name: Tuple(x, y), ...}
    """

    platform_positions = {
        "desert": {"platform_pos": (500, 500), "monster_pos": (600, 370)},
        "hell": {"platform_pos": (500, 300), "monster_pos": (590, 360)},
        "mountain": {"platform_pos": (470, 300), "monster_pos": (590, 370)},
        "no_sea_sky": {"platform_pos": (500, 320), "monster_pos": (600, 370)},
        "rocks": {"platform_pos": (500, 300), "monster_pos": (600, 360)},
        "sea_sky": {"platform_pos": (500, 450), "monster_pos": (590, 390)},
        "volcano": {"platform_pos": (470, 300), "monster_pos": (590, 350)},
    }

    return platform_positions
