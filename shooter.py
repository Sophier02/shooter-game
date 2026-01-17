from random import randint
from pygame import *
from time import time as timer
init()
window = display.set_mode((700, 500))
win_width = 700
win_height = 500
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
FPS = 50
mixer.init()
fire_sound = mixer.Sound('fire.ogg')
# mixer.music.load('space.ogg')
# mixer.music.play()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 7, self.rect.top, 3)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(5, 650)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        self.image = transform.scale(self.image, (15, 20))
bullets = sprite.Group()
enemies = sprite.Group()
asteroids = sprite.Group()
player = Player('rocket.png', 350, 400, 3)
enemy1 = Enemy('ufo.png', randint(5, 650), 10, randint(1, 2))
enemy2 = Enemy('ufo.png', randint(5, 650), 10, randint(1, 2))
enemy3 = Enemy('ufo.png', randint(5, 650), 10, randint(1, 2))
enemy4 = Enemy('ufo.png', randint(5, 650), 10, randint(1, 2))
asteroid1 = Enemy('asteroid.png', randint (5, 650), 10, randint(1, 2))
asteroid2 = Enemy('asteroid.png', randint (5, 650), 10, randint(1, 2))
asteroid3 = Enemy('asteroid.png', randint (5, 650), 10, randint(1, 2))
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)
enemies.add(enemy4)
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
lost = 0
killed = 0
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 50)
text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
text_counter = font1.render('Счет:' + str(killed), 1, (255, 255, 255))
game = True
finish = False
rel_time = False
num_fire = 0
while game:
    window.blit(background,(0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
             if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                   num_fire = num_fire + 1
                   fire_sound.play()
                   player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if rel_time == True:
        now_time = timer()
        if now_time - last_time < 1:
            reload = font2.render('Wait, reload...', 1, (150, 0, 0))
            window.blit(reload, (260, 460))
        else:
            num_fire = 0
            rel_time = False
            fire_sound.play()
            player.fire()
    sprites_list = sprite.groupcollide(enemies, bullets, True, True)
    sprite_list = sprite.spritecollide(player, asteroids, False)
    sprit_list = sprite.spritecollide(player, enemies, False)
    if len(sprite_list) != 0:
        finish = True
        text_over = font2.render('YOU LOSE', 1, (255, 0, 0))
        window.blit(text_over, (300, 250))
    if len(sprit_list) != 0:
        finish = True
        text_over = font2.render('YOU LOSE', 1, (255, 0, 0))
        window.blit(text_over, (300, 250))
    for thing in sprites_list:
        killed += 1
        enemy5 = Enemy('ufo.png', randint(5, 650), 10, randint(1, 2))
        enemies.add(enemy5)
    text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
    text_counter = font1.render('Счет:' + str(killed), 1, (255, 255, 255))
    if lost >= 5:
        finish = True
        text_over = font2.render('YOU LOSE', 1, (255, 0, 0))
        window.blit(text_over, (300, 250))
    if killed >= 10:
        finish = True
        text_win = font2.render('YOU WIN', 1, (250, 250, 5))
        window.blit(text_win, (300, 250))
    if finish != True:
        asteroids.update()
        asteroids.draw(window)
        enemies.draw(window)
        player.reset()
        enemies.update()
        player.update()
        bullets.update()
        bullets.draw(window)
        window.blit(text_lose, (10, 10))
        window.blit(text_counter, (10, 35))
    display.update()
    clock.tick(FPS)