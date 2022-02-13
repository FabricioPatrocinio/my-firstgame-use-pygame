def collision(rect, tiles):
    '''Collision between objects.'''

    hit_list = []

    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)

    return hit_list
