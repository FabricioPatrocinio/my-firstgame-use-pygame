# External modules
import pygame
from pygame.locals import *


def load_animation(path, frame_durations):
    '''[7,7] animation person.'''

    global animation_frames

    animation_frames = {}
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0

    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'

        animation_image = pygame.image.load(img_loc).convert()

        animation_image.set_colorkey((255, 255, 255))
        animation_frames[animation_frame_id] = animation_image.copy()

        for i in range(frame):
            animation_frame_data.append(animation_frame_id)

        n += 1

    return animation_frame_data
