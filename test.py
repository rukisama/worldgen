import tcod as tdl

tdl.console_set_custom_font('potash_10x10.png', tdl.FONT_TYPE_GREYSCALE | tdl.FONT_LAYOUT_ASCII_INROW)
tdl.console_init_root(80, 50, 'None')

tdl_key = tdl.Key()
tdl_mouse = tdl.Mouse()

while not tdl.console_is_window_closed():
    event_type_flags = tdl.EVENT_KEY_PRESS | tdl.EVENT_MOUSE
    tdl.sys_check_for_event(event_type_flags, tdl_key, tdl_mouse)

    if tdl_key.vk != 0:
        print(tdl_key.pressed)
