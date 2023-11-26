import pygame
from random import choices
from jivda_script import Jivdu
import sys

def loop(game):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game.game_over:
            match e.type:
                case game.enemy_spawn_event.type:
                    game.jivda.add(Jivdu(*(choices((game.fly_resources,game.snail_resources),weights=(1/3,2/3),k=1)[0])))
                case pygame.KEYDOWN:
                    if not game.AI_ENABLED and e.key == pygame.K_SPACE and game.player.sprite.rect.bottom==300:
                        game.player.sprite.gravity = -15
                        game.player.sprite.jump_sound.play()
                case game.point_timer.type:
                    game.cool_sound.play()

        else:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                game.start_sound.play()
                game.set_playground()
                if game.AI_ENABLED:
                    game.load_AI()
                else:
                    game.load_human()