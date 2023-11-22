import os
import pygame
import sys
from shelve import open as shopen
from random import choices

import player_script
from jivda_script import Jivdu

# load resources
datapath = os.path.join(os.path.dirname(__file__), './data/playerdata')
highscore = '0'
score = '0'
start_time = 0
game_over = True

pygame.init()
screen_surface = pygame.display.set_mode((800,400))
pygame.display.set_caption('lol game')
font_obj = pygame.font.Font('assets/font/Pixeltype.ttf',50)
clk = pygame.time.Clock()

bg_music = pygame.mixer.Sound('assets/audio/music.wav')
bg_music.set_volume(0.55)
bg_music.play(loops=-1)
start_sound = pygame.mixer.Sound('assets/audio/maximize_005.ogg')
fail_sound = pygame.mixer.Sound('assets/audio/minimize_005.ogg')
cool_sound = pygame.mixer.Sound('assets/audio/confirmation_002.ogg')

ground_img_surf = pygame.image.load('assets/graphics/ground.png').convert()
sky_img_surf = pygame.image.load('assets/graphics/Sky.png').convert()

enemy_spawn_event = pygame.event.Event(pygame.event.custom_type())
pygame.time.set_timer(enemy_spawn_event,1000)
point_timer = pygame.event.Event(pygame.event.custom_type())

player_animation_frames = [pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha(), pygame.image.load('assets/graphics/Player/player_walk_2.png').convert_alpha()]
player_jump_frame = pygame.image.load('assets/graphics/Player/jump.png').convert_alpha()
player_jump_sound = pygame.mixer.Sound('assets/audio/jump.mp3')
player_resources = player_animation_frames,player_jump_frame,player_jump_sound

fly_animation_frames = [pygame.image.load('assets/graphics/Fly/Fly1.png').convert_alpha(),pygame.image.load('assets/graphics/Fly/Fly2.png').convert_alpha()]
snail_animation_frames = [pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha(),pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()]
fly_resources = 'maakhi',fly_animation_frames
snail_resources = 'gokalgaai',snail_animation_frames

def show_score():
    score = str(int(pygame.time.get_ticks()/1000) - start_time)
    text_surf = font_obj.render(f'Score: {score}', False, 'green')
    text_rect = text_surf.get_rect(center=(400,50))
    screen_surface.blit(text_surf,text_rect)
    return score

with shopen(datapath) as cupboard:
    cupboard.setdefault('highscore',highscore)
    highscore = cupboard['highscore']

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            match e.type:
                case enemy_spawn_event.type:
                    jivda.add(Jivdu(*(choices((fly_resources,snail_resources),weights=(1/3,2/3),k=1)[0])))
                case pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE and player.sprite.rect.bottom==300:
                        player.sprite.gravity = -20
                        player.sprite.jump_sound.play()
                case point_timer.type:
                    cool_sound.play()

        else:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                game_over = False
                player = player_script.reset(*player_resources)
                jivda = pygame.sprite.Group()
                start_time = int(pygame.time.get_ticks()/1000)
                start_sound.play()
                pygame.time.set_timer(point_timer,10000)

    if not game_over:

        player.update()
        jivda.update()

        if pygame.sprite.spritecollide(player.sprite,jivda,False) : game_over = True

        screen_surface.blit(ground_img_surf,(0,300))
        screen_surface.blit(sky_img_surf,(0,0))
        player.draw(screen_surface)
        jivda.draw(screen_surface)
        score = show_score()

    else:
        screen_surface.blit(ground_img_surf,(0,300))
        screen_surface.blit(sky_img_surf,(0,0))
        player_img_surf = pygame.image.load('assets/graphics/Player/player_stand.png').convert_alpha()
        player_surf = pygame.transform.rotozoom(player_img_surf,0,2)
        screen_surface.blit(player_surf,player_surf.get_rect(center=(400,170)))

        text_surf = font_obj.render('Press  Enter  to  Start', False, 'green')
        text_rect = text_surf.get_rect(center=(400,50))
        screen_surface.blit(text_surf,text_rect)

        text_surf = font_obj.render(f'Current  Score: {score}', False, 'blue')
        text_rect = text_surf.get_rect(left=30,y=150)
        screen_surface.blit(text_surf,text_rect)

        # save the high score
        if int(score) > int(highscore):
            highscore = score
            with shopen(datapath) as cupboard:
                cupboard['highscore'] = highscore
        
        text_surf = font_obj.render(f'Best  Score: {highscore}', False, 'red')
        text_rect = text_surf.get_rect(right=770,y=150)
        screen_surface.blit(text_surf,text_rect)

    pygame.display.update()
    clk.tick(60)