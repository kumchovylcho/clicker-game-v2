import pygame as pg


def create_font(value:str, font:str, size_font:int, colour: tuple, bold=True, antialias=True):
    font = pg.font.SysFont(font, size_font, bold)
    return font.render(value, antialias, colour)


def numbers_format(num):
    num = float(f'{num:.3g}')
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    result = f"{str(num).rstrip('0').rstrip('.')}{['', 'K', 'M', 'B', 'T'][magnitude]}"
    return result


def calculate_center(main_obj_width, child_obj_width):
    """
    :return: int(pixels) of the X position where the child object must be placed
    """
    middle_of_main_obj = main_obj_width // 2
    middle_of_child_obj = child_obj_width // 2

    return middle_of_main_obj - middle_of_child_obj


def get_screen_size():
    return 900, 800
