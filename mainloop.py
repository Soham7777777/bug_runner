import pygame
import game_script
import eventloop
game = game_script.Game()

def play(AI_ENABLE):
    game.AI_ENABLED = AI_ENABLE
    while True:
        eventloop.loop(game)

        if not game.game_over:
            game.update_sprites()

            if pygame.sprite.spritecollide(game.player.sprite if not AI_ENABLE else game.AI_player.sprite,game.jivda,False):
                game.after_game_over()
            
            game.draw_sprites()

            # handle AI
            if game.AI_ENABLED:
                inputs = game.generate_input(game.AI_player.sprite)
                game.AI_player.update(inputs)
                if game.AI_player.sprite.output > 0.5 and game.AI_player.sprite.rect.bottom == 300:
                    game.AI_player.sprite.gravity = -15
                    game.AI_player.sprite.jump_sound.play()
                game.AI_player.draw(game.screen_surface)


        else:
            game.show_homescreen()

        pygame.display.update()
        game.clk.tick(60)
