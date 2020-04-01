import tcod as libtcod


def handle_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    if key.vk == libtcod.KEY_UP and key.shift:
        return {'move': (0, -10)}
    elif key.vk == libtcod.KEY_DOWN and key.shift:
        return {'move': (0, 10)}
    elif key.vk == libtcod.KEY_LEFT and key.shift:
        return {'move': (-10, 0)}
    elif key.vk == libtcod.KEY_RIGHT and key.shift:
        return {'move': (10, 0)}
    elif key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}

    if key.vk == libtcod.KEY_ENTER:
        return {'data': True}

    return {}
