import os
import pygame
import game_script
import sys
import neat
import ai_body
from random import choices
from jivda_script import Jivdu
import visualize
from shelve import open as shopen

game = game_script.Game()

def train(configpath):
    settings = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         configpath)

    ai_colony = neat.Population(settings)

    ai_colony.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    ai_colony.add_reporter(stats)

    best_AI = ai_colony.run(play,50)
    with shopen('AI') as cupboard:
        cupboard['AI'] = best_AI

    print(f"BEST AI : {best_AI}")
    visualize.draw_net(settings, best_AI, True)

def set_envirnment():
    game.jivda = pygame.sprite.Group()
    game.start_time = int(pygame.time.get_ticks()/1000)
    pygame.time.set_timer(game.point_timer,10000)

def eventloop():
    for e in pygame.event.get():
        match e.type:
            case pygame.QUIT:
                pygame.quit()
                sys.exit()
            case game.enemy_spawn_event.type:
                game.jivda.add(Jivdu(*(choices((game.fly_resources,game.snail_resources),weights=(1/3,2/3),k=1)[0])))
            case game.point_timer.type:
                game.cool_sound.play()

def play(DNAs, settings):
    updated_DNAs = []
    set_envirnment()
    robots = pygame.sprite.Group()
    for id, DNA in DNAs:
        ai_resources = id,DNA,settings
        robots.add(ai_body.Robot(*ai_resources, *game.player_resources))

    while any(robots):
        eventloop()

        # draw robots
        game.bg_group.draw(game.screen_surface)
        game.jivda.draw(game.screen_surface)
        robots.draw(game.screen_surface)
        game.show_score()
        for robot in robots:
            if pygame.sprite.spritecollide(robot,game.jivda,False):
                robot.DNA.fitness -= 5.0
                updated_DNAs.append((robot.id,robot.DNA.fitness))
                robot.kill()
        else:
            game.bg_group.update()
            game.jivda.update()

            for robot in robots:
                if robot.output > 0.5 and robot.rect.bottom==300:
                    robot.gravity = -15
                    robot.jump_sound.play()
                robot.DNA.fitness =  float(game.score)
                robot.update(game.generate_input(robot))
                
        pygame.display.update()
        game.clk.tick(60)
    
    for id, DNA in DNAs:
        for id_, fitness in updated_DNAs:
            if id == id_: 
                DNA.fitness = fitness
                break


def run():
    configpath = os.path.join(os.path.dirname(__file__), 'AI_training_config.txt')
    train(configpath)
