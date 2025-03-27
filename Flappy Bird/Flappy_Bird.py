import pygame
import random
from bird import Bird
from pipe import Pipe

pygame.init()

def generate_pipes(last_pipe_time, pipe_frequency, pipe_group):
    now = pygame.time.get_ticks()
    if now - last_pipe_time >= pipe_frequency:
        random_height = random.randint(-100, 100)
        pipe_btm = Pipe(WIDTH, HEIGHT/2 + pipe_gap/2 + random_height, pipe_img, False)
        pipe_top = Pipe(WIDTH, HEIGHT/2 - pipe_gap/2 + random_height, pipe_reverse_img, True)
        pipe_group.add(pipe_btm)
        pipe_group.add(pipe_top)
        return now
    return last_pipe_time

def draw_score():
    score_text = score_font.render(str(score), True, WHITE)
    window.blit(score_text, (WIDTH/2-score_text.get_width()/2, 20))


# Settings
WIDTH, HEIGHT = 780, 600
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('可愛的鳥鳥')
clock = pygame.time.Clock()
ground_x = 0
WHITE = (255,255,255)

# Load images
bg = pygame.transform.scale(pygame.image.load('assets/bg.png'), (WIDTH, HEIGHT))
ground_img = pygame.image.load('assets/ground.png')

pipe_img = pygame.image.load('assets/pipe.png')
pipe_reverse_img = pygame.transform.flip(pipe_img,False, True)
restart_img = pygame.image.load('assets/restart.png')
bird_imgs = []
for i in range(1, 3):
    bird_imgs.append(pygame.image.load(f"assets/bird{i}.png"))
pygame.display.set_icon(bird_imgs[0])

# 載入字體
score_font = pygame.font.Font("微軟正黑體.ttf", 60)


ground_speed = 4
ground_x = 0
ground_top = HEIGHT-100
pipe_gap = 150
pipe_frequency = 1500
last_pipe_time = pygame.time.get_ticks() - pipe_frequency
game_over = False
score = 0 

# Sprite groups
bird = Bird(100, 300, bird_imgs)
bird_group = pygame.sprite.Group()
bird_group.add(bird)

pipe_group = pygame.sprite.Group()



run = True
while run:

    clock.tick(FPS)

    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not game_over:
                bird.jump()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                score = 0
                last_pipe_time = pygame.time.get_ticks()-pipe_frequency
                bird.reset()
                pipe_group.empty()
                # for pipe in pipe_group.sprites():
                #     pipe.kill()

    #更新遊戲
    bird_group.update(ground_top)
    
    if not game_over: 
        pipe_group.update()
        last_pipe_time = generate_pipes(last_pipe_time, pipe_frequency, pipe_group)
        #判斷鳥通過管子
        first_pipe = pipe_group.sprites()[0]
        if not first_pipe.bird_pass:
            if first_pipe.rect.right < bird.rect.left:
                score += 1
                first_pipe.bird_pass = True


        #移動地板
        ground_x -= ground_speed
        if ground_x < -100:
            ground_x = 0
        

    #碰撞判斷
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or\
        bird.rect.top <= 0 or\
        bird.rect.bottom >= ground_top:
            game_over = True
            bird.game_over()

    #畫面顯示
    window.blit(bg, (0,0))
    pipe_group.draw(window)
    window.blit(ground_img, (ground_x, ground_top))
    # window.blit(bird_img, (100,100))
    bird_group.draw(window)
    draw_score()
    if game_over:
        window.blit(restart_img,(WIDTH/2-restart_img.get_width()/2, HEIGHT/2-restart_img.get_height()/2))
    pygame.display.update()

pygame,quit()
