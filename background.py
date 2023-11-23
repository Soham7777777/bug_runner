import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, surface,topleft,speed) -> None:
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=topleft)
        self.speed = speed

    def animate(self):
        self.rect.x -= self.speed
        if self.rect.x <= -800: self.rect.x = 800
    
    def update(self) -> None:
        self.animate()