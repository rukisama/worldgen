import tcod as libtcod
import numpy
from random import randint


def init_graphics(screen_width, screen_height):

    libtcod.console_set_custom_font('potash_10x10.png', libtcod.FONT_LAYOUT_ASCII_INROW | libtcod.FONT_TYPE_GREYSCALE)
    root_console = libtcod.console_init_root(screen_width, screen_height, "World Map TCOD Test")

    return root_console


def render_all(root_console, world_map, cursor_x, cursor_y):

    root_console.ch[:] = ord(' ')

    root_console.fg[:] = world_map.fg_color[:]
    root_console.ch[:] = world_map.glyph[:]
    root_console.bg[:] = (0, 0, 0)  # world_map.local_map.bg_color[:]

    root_console.fg[cursor_y, cursor_x] = (0, 0, 0)
    root_console.bg[cursor_y, cursor_x] = (255, 255, 255)
    root_console.ch[cursor_y, cursor_x] = ord('X')

    root_console.print_(x=0, y=0, string=str(libtcod.sys_get_fps()))
    root_console.print_(x=97, y=0, string=str(int(world_map.elevation_map[cursor_y, cursor_x])))

    libtcod.console_flush()

    root_console.bg[:] = (0, 0, 0)

    fps = libtcod.sys_get_fps()

    return fps
