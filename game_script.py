import os
import pygame
from shelve import open as shopen
import player_script

from background import Background

class Game:
    def __init__(self) -> None:
        self.datapath = os.path.join(os.path.dirname(__file__), './data/playerdata')
        self.highscore = '0'
        self.score = '0'
        self.start_time = 0
        self.game_over = True

        pygame.init()

        self.screen_surface = pygame.display.set_mode((800,400))
        pygame.display.set_caption('Bug Runner')
        self.font_obj = pygame.font.Font('assets/font/Pixeltype.ttf',50)
        self.clk = pygame.time.Clock()

        self.bg_music = pygame.mixer.Sound('assets/audio/music.wav')
        self.bg_music.set_volume(0.55)
        self.bg_music.play(loops=-1)
        self.start_sound = pygame.mixer.Sound('assets/audio/maximize_005.ogg')
        self.fail_sound = pygame.mixer.Sound('assets/audio/minimize_005.ogg')
        self.cool_sound = pygame.mixer.Sound('assets/audio/confirmation_002.ogg')

        ground_img_surf = pygame.image.load('assets/graphics/ground.png').convert()
        sky_img_surf = pygame.image.load('assets/graphics/Sky.png').convert()
        self.bg_group = pygame.sprite.Group(Background(ground_img_surf,(0,300),10),Background(ground_img_surf,(800,300),10), Background(sky_img_surf,(0,0),5),Background(sky_img_surf,(800,0),5))

        self.enemy_spawn_event = pygame.event.Event(pygame.event.custom_type())
        pygame.time.set_timer(self.enemy_spawn_event,900)
        self.point_timer = pygame.event.Event(pygame.event.custom_type())

        player_animation_frames = [pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha(), pygame.image.load('assets/graphics/Player/player_walk_2.png').convert_alpha()]
        player_jump_frame = pygame.image.load('assets/graphics/Player/jump.png').convert_alpha()
        player_jump_sound = pygame.mixer.Sound('assets/audio/jump.mp3')
        self.player_resources = player_animation_frames,player_jump_frame,player_jump_sound

        fly_animation_frames = [pygame.image.load('assets/graphics/Fly/Fly1.png').convert_alpha(),pygame.image.load('assets/graphics/Fly/Fly2.png').convert_alpha()]
        snail_animation_frames = [pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha(),pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()]
        self.fly_resources = 'maakhi',fly_animation_frames
        self.snail_resources = 'gokalgaai',snail_animation_frames

        self.load_highscore()

    def show_score(self):
        score = str(int(pygame.time.get_ticks()/1000) - self.start_time)
        text_surf = self.font_obj.render(f'Score: {score}', False, 'green')
        text_rect = text_surf.get_rect(center=(400,50))
        self.screen_surface.blit(text_surf,text_rect)
        self.score = score
    
    def load_highscore(self):
        with shopen(self.datapath) as cupboard:
            cupboard.setdefault('highscore',self.highscore)
            self.highscore = cupboard['highscore']
        
    def show_homescreen(self):
        self.bg_group.draw(self.screen_surface)
        player_img_surf = pygame.image.load('assets/graphics/Player/player_stand.png').convert_alpha()
        player_surf = pygame.transform.rotozoom(player_img_surf,0,2)
        self.screen_surface.blit(player_surf,player_surf.get_rect(center=(400,170)))

        text_surf = self.font_obj.render('Press  Enter  to  Start', False, 'green')
        text_rect = text_surf.get_rect(center=(400,50))
        self.screen_surface.blit(text_surf,text_rect)

        text_surf = self.font_obj.render(f'Current  Score: {self.score}', False, 'blue')
        text_rect = text_surf.get_rect(left=30,y=150)
        self.screen_surface.blit(text_surf,text_rect)
        
        text_surf = self.font_obj.render(f'Best  Score: {self.highscore}', False, 'red')
        text_rect = text_surf.get_rect(right=770,y=150)
        self.screen_surface.blit(text_surf,text_rect)
    
    def after_game_over(self):
        self.game_over = True
        self.fail_sound.play()
        self.save_highscore()
    
    def set_playground(self):
        self.game_over = False
        self.player = player_script.reset(*self.player_resources)
        self.jivda = pygame.sprite.Group()
        self.start_time = int(pygame.time.get_ticks()/1000)
        pygame.time.set_timer(self.point_timer,10000)
    
    def update_sprites(self):
        self.bg_group.update()
        self.player.update()
        self.jivda.update()
    
    def draw_sprites(self):
        self.bg_group.draw(self.screen_surface)
        self.player.draw(self.screen_surface)
        self.jivda.draw(self.screen_surface)
        self.show_score()
    
    def save_highscore(self):
        if int(self.score) > int(self.highscore):
            self.highscore = self.score
            with shopen(self.datapath) as cupboard:
                cupboard['highscore'] = self.highscore