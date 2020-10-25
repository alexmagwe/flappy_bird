import pygame,sys,random
from collections import deque

#game variables
pipe_heights = [400,600,800]
pipe_originx = 700
pipe_dx= 4
screen_height=1024
screen_width=576
gravity = 0.25
pipe_list = deque(maxlen=5)
game_active=False
pipe_speed=1500
flap_speed=200
jump_height=8
original_bird_pos=(100,int(screen_height/2))
scorex_pos=screen_width-120
score=0
high_score=0
scorey_pos=80
game_over=False

def create_pipe():
    height = random.choice(pipe_heights)
    pipe = pipe_surface.get_rect(midtop  =  (pipe_originx,height))
    top_pipe = pipe_surface.get_rect(midbottom = (pipe_originx,height-300))
    return pipe,top_pipe

def rotate_bird(bird):
    rotated_bird = pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return rotated_bird
    
def move_pipes(pipe_list):
    for pipe in pipe_list:
        pipe.centerx -=  pipe_dx
    return pipe_list

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=screen_height:
            screen.blit(pipe_surface,pipe)
        else:
            flipped_pipe=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flipped_pipe,pipe)
            
def draw_floor():
    screen.blit(floor,(floor_x,screen_height-floor_height))
    screen.blit(floor,(floor_x + screen_width,screen_height-floor_height))
    
def detect_collision():
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            return True 
    return False

def bird_flap():
    new_bird_surface=bird_frames[frame_index%len(bird_frames)]#cycle between frame index values
    new_bird_rect=new_bird_surface.get_rect(center=(100,bird_rect.centery))
    return new_bird_surface,new_bird_rect

def display_score():
    score_surface=game_font.render(f'score:{score}',True,(255,255,255))#middle arg true is to set antialiasing
    score_rect=score_surface.get_rect(center=(scorex_pos,scorey_pos))   
    high_score_surface=game_font.render(f'High score:{high_score}',True,(255,255,255))
    high_score_rect=high_score_surface.get_rect(center=(scorex_pos,scorey_pos-40))
    screen.blit(high_score_surface,high_score_rect) 
    screen.blit(score_surface,score_rect) 
# pygame.mixer.pre_init(frequency=44100,size=16,channels=1,buffer=512)
pygame.init()
game_font=pygame.font.Font('assets/04B_19.TTF',32)

screen = pygame.display.set_mode([screen_width,screen_height])
clock = pygame.time.Clock()
bird_movement = 0

pipe_surface = pygame.image.load('assets/sprites/pipe-green.png').convert()
pipe_surface=pygame.transform.scale2x(pipe_surface)

bg_surface = pygame.transform.scale2x(pygame.image.load('assets/sprites/background-day.png').convert())
floor = pygame.transform.scale2x(pygame.image.load('assets/sprites/base.png').convert())
floor_height = floor.get_height()-100
floor_x = 0

game_over_surface=pygame.transform.scale2x(pygame.image.load('assets/sprites/gameover.png').convert_alpha())
game_over_rect=game_over_surface.get_rect(center=(int(screen_width/2),int(screen_height/2)))

bird_surface1 = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha())
bird_surface2 = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha())
bird_surface3 = pygame.transform.scale2x(pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha())
bird_frames=[bird_surface1,bird_surface2,bird_surface3]
frame_index=0
bird_surface=bird_frames[frame_index]#cycle betweeen index values of bird frames
bird_rect = bird_surface.get_rect(center = original_bird_pos)
#sounds
flap_sound=pygame.mixer.Sound('assets/audio/wing.ogg')
death_sound=pygame.mixer.Sound('assets/audio/hit.ogg')
#events
SPAWNPIPE = pygame.USEREVENT+1
BIRDFLAP = pygame.USEREVENT+2
UPDATE_SCORE=pygame.USEREVENT+3
pygame.time.set_timer(SPAWNPIPE,pipe_speed)   
pygame.time.set_timer(BIRDFLAP,flap_speed) 
pygame.time.set_timer(UPDATE_SCORE,500)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= jump_height
                flap_sound.play()
            if event.key ==pygame.K_SPACE and not game_active:
                pipe_list.clear()
                bird_movement=0
                bird_rect.center=original_bird_pos
                score=0
                game_active=True
        if event.type == BIRDFLAP and game_active:
            frame_index+=1
            bird_surface,bird_rect=bird_flap()
        if game_active and event.type ==SPAWNPIPE:
            pipe_list.extend(create_pipe())#extend destructures the tuple into the list
        if event.type == UPDATE_SCORE and game_active:
            
            score+=1
    screen.blit(bg_surface,(0,0))
    bird=rotate_bird(bird_surface)
    screen.blit(bird,bird_rect)
    draw_pipes(pipe_list)
    if detect_collision() and game_active:
        death_sound.play()
        game_active = False
        game_over=True
    if game_active:
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        bird_movement += gravity
        bird_rect.centery += int(bird_movement)
        floor_x -= 5
        if bird_rect.bottom >= 1024-floor_height:
            bird_rect.bottom = 1024-floor_height
        if bird_rect.top<=0:
            bird_rect.top = 0
        if floor_x <= -576:
            floor_x = 0
    else:
        if score>high_score:
            high_score=score
        if game_over:
            screen.blit(game_over_surface,game_over_rect)
   
    draw_floor()
    display_score()
    pygame.display.update()
    clock.tick(120)#fps of game
