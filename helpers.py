import pygame as pg
import os

from map_handler.monster import Monster


def create_font(value:str, font:str, size_font:int, colour: tuple, bold=True, antialias=True):
    font = pg.font.SysFont(font, size_font, bold)
    return font.render(value, antialias, colour)


def calculate_center(main_obj_width, child_obj_width):
    """
    :return: int(pixels) of the X position where the child object must be placed
    """
    middle_of_main_obj = main_obj_width // 2
    middle_of_child_obj = child_obj_width // 2

    return middle_of_main_obj - middle_of_child_obj


def get_screen_size():
    return 900, 800


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
