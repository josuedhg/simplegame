#!/usr/bin/env python3

import pygame
from enum import Enum


class SpriteSheetImage:
    def __init__(self, image_path: str, width: int, height: int):
        self.image = pygame.image.load(image_path)
        self.width = width
        self.height = height
        self.image.convert()


class SpriteState(Enum):
    MOVING = 0
    STOPPED = 1


class SpriteSheetAnimation:
    def __init__(self, image: SpriteSheetImage, animation: int, index: int,
                 num_max_frames: int, num_frames: int, num_animations: int,
                 initial_position: (int, int)):
        self.image = image
        self.animation = animation
        self.index = index
        self.num_frames = num_frames
        self.frame_width = self.image.width / num_max_frames
        self.frame_height = self.image.height / num_animations
        self.frames = [self._create_sprite_rect(i) for i in range(num_frames)]
        self.state = SpriteState.STOPPED
        self.position = initial_position

    def _create_sprite_rect(self, index: int):
        return pygame.Rect(self.frame_width * index,
                           self.frame_height * self.animation,
                           self.frame_width, self.frame_height)

    def animate(self):
        self.state = SpriteState.MOVING

    def stop(self):
        self.state = SpriteState.STOPPED

    def set_position(self, position: (int, int)):
        self.position = position

    def refresh(self, screen):
        screen.blit(self.image.image, self.position, self.frames[self.index])
        if self.state == SpriteState.MOVING:
            self.index = (self.index + 1) % self.num_frames


class Player(pygame.sprite.Sprite):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    movement_values = [
        (0, -5),
        (5, 0),
        (0, 5),
        (-5, 0)
    ]

    def __init__(self, animations: list):
        super().__init__()
        self.animations = animations
        self.direction = self.SOUTH
        self.position_increment = (0, 0)
        self.position = self.animations[self.direction].position

    def refresh(self, screen):
        self.position = (
            self.position[0] + self.position_increment[0],
            self.position[1] + self.position_increment[1])
        for animation in self.animations:
            animation.set_position(self.position)
        self.animations[self.direction].refresh(screen)

    def move(self, direction):
        self.direction = direction
        self.animations[self.direction].animate()
        self.position_increment = self.movement_values[direction]

    def stop(self, direction):
        self.direction = direction
        self.animations[self.direction].stop()
        self.position_increment = (0, 0)

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.move(self.EAST)
            elif event.key == pygame.K_LEFT:
                self.move(self.WEST)
            elif event.key == pygame.K_UP:
                self.move(self.NORTH)
            elif event.key == pygame.K_DOWN:
                self.move(self.SOUTH)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.stop(self.EAST)
            elif event.key == pygame.K_LEFT:
                self.stop(self.WEST)
            elif event.key == pygame.K_UP:
                self.stop(self.NORTH)
            elif event.key == pygame.K_DOWN:
                self.stop(self.SOUTH)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        spriteimage = SpriteSheetImage("playersprite.png", 832, 1344)
        self.player = Player(
            [
                SpriteSheetAnimation(spriteimage, 8, 0, 13, 9, 21, (0, 0)),
                SpriteSheetAnimation(spriteimage, 11, 0, 13, 9, 21, (0, 0)),
                SpriteSheetAnimation(spriteimage, 10, 0, 13, 9, 21, (0, 0)),
                SpriteSheetAnimation(spriteimage, 9, 0, 13, 9, 21, (0, 0)),
            ])

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.player.event_handler(event)
                elif event.type == pygame.KEYUP:
                    self.player.event_handler(event)

            self.screen.fill((255, 255, 255))
            self.player.refresh(self.screen)
            self.clock.tick(10)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
