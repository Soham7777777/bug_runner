import pygame
import neat

class Robot(pygame.sprite.Sprite):
    def __init__(self,id,DNA,settings,animation_frames,jump_frame,jump_sound) -> None:
        super().__init__()
        self.id = id
        self.DNA = DNA
        self.settings = settings
        self.brain = neat.nn.FeedForwardNetwork.create(DNA,settings) 
        self.DNA.fitness = 0.0

        self.animation_frames = animation_frames
        self.jump_surf = jump_frame
        self.rect = self.animation_frames[0].get_rect(midbottom=(100,300))
        self.index = 0
        self.image = self.animation_frames[self.index]
        self.gravity = 0
        self.jump_sound = jump_sound
        self.jump_sound.set_volume(0.5)

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.jump_surf
            return
        
        self.image = self.animation_frames[int(self.index)]
        self.index =  (self.index + 0.2) % len(self.animation_frames)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300

    def update(self):
        self.apply_gravity()
        self.animate()