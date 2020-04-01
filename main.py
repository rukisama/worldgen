import tcod as libtcod

from graphics import init_graphics, render_all
from mapgen import WorldMap
from input_functions import handle_keys

noise_zoom = 2
noise_octaves = 20
key = libtcod.Key()
mouse = libtcod.Mouse()

screen_width = 100
screen_height = 100

cursor_x = 10
cursor_y = 10

if __name__ == '__main__':

    world_map = WorldMap(screen_width, screen_height)
    world_map.generate_map(noise_zoom, noise_octaves)

    root_console = init_graphics(screen_width, screen_height)

    avg_fps = []

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        new_fps = render_all(root_console, world_map, cursor_x, cursor_y)
        avg_fps.append(new_fps)

        action = handle_keys(key)

        exit = action.get('exit')
        move = action.get('move')
        data = action.get('data')

        if move:
            dx, dy = move
            if cursor_x + dx < 0:
                cursor_x = 0
            elif cursor_x + dx > screen_width - 1:
                cursor_x = screen_width - 1
            else:
                cursor_x += dx
            if cursor_y + dy < 0:
                cursor_y = 0
            elif cursor_y + dy > screen_height - 1:
                cursor_y = screen_height - 1
            else:
                cursor_y += dy

        if data:
            pass

        if exit:
            fps = sum(avg_fps) / len(avg_fps)
            print(fps)
            break

