# Internal modules
from collision import collision


def change_action(action_var, frame, new_value):
    '''Capture an action.'''

    if action_var != new_value:
        action_var = new_value
        frame = 0

    return action_var, frame


def move(rect, movement, tiles):
    '''Function responsible for the movement.'''

    collision_types = {}

    collision_types['top'] = False
    collision_types['bottom'] = False
    collision_types['left'] = False
    collision_types['right'] = False

    rect.x += movement[0]
    hit_list = collision(rect, tiles)

    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True

        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision(rect, tiles)

    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True

        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types
