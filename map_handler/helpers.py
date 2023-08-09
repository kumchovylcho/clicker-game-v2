import os

from map_handler.monster import Monster
import pygame as pg


def get_monsters_on_chosen_map(map_name: str):
    """
    :return: list of monster objects for the given map
    """
    monster_positions = get_monster_positions()

    monsters = []
    directory_path = 'images/monsters'
    for map_n in os.listdir(directory_path):
        if map_n != map_name:
            continue

        file_path = os.path.join(directory_path, map_n)
        for file in os.listdir(file_path):
            image_path = os.path.join(file_path, file)
            monster_img = pg.image.load(image_path).convert_alpha()

            monsters.append(Monster(image=monster_img,
                                    health=0,
                                    x_pos=monster_positions[map_n][0],
                                    y_pos=monster_positions[map_n][1]))

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

    platform_positions = {
        "desert": (500, 500),
        "hell": (500, 300),
        "mountain": (470, 300),
        "no_sea_sky": (500, 320),
        "rocks": (500, 300),
        "sea_sky": (500, 450),
        "volcano": (470, 300),
    }

    return platform_positions


def get_monster_positions():
    monster_positions = {
        "desert": (600, 370),
        "hell": (590, 360),
        "mountain": (590, 370),
        "no_sea_sky": (600, 370),
        "rocks": (600, 360),
        "sea_sky": (590, 390),
        "volcano": (590, 350),
    }

    return monster_positions
