from random import randint
import pygame

class Jivdu(pygame.sprite.Sprite):
    def __init__(self,type,animation_frame) -> None:
        super().__init__()
        if type == 'maakhi': y = 200
        elif type == 'gokalgaai': y = 300
        
        self.animation_frames = animation_frame
        self.index = 0
        self.image = self.animation_frames[self.index]
        self.rect = self.image.get_rect(bottomleft=(randint(900,1500),y))
        self.speed = 9
    
    def animate(self):
        self.index = (self.index + 0.2) % len(self.animation_frames)
        self.image = self.animation_frames[int(self.index)]

    def move(self):
        self.rect.x -= self.speed

    def destroy(self):
        if self.rect.x <= -100 : self.kill()

    def update(self):
        self.animate()
        self.move()
        self.destroy()