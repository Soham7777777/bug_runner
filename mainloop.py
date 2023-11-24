import pygame
import game_script
import eventloop
game = game_script.Game()

def play():
    while True:
        eventloop.loop(game)

        if not game.game_over:
            game.update_sprites()

            if pygame.sprite.spritecollide(game.player.sprite,game.jivda,False):
                game.after_game_over()
            
            game.draw_sprites()
        else:
            game.show_homescreen()

        pygame.display.update()
        game.clk.tick(60)