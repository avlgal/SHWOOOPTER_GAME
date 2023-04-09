from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('vzryiv-yadernoy-bombyi.ogg')

img_back = 'kapook_world-670869.jpg'
img_hero = '123456.jpg'
img_enemy = '2423.jpg'
img_bullet = '1.png'
img_ast = 'asteroid.png'

font.init()
font2 = font.SysFont('Arial', 36)

lost = 0
score = 0

win_w = 1300
win_h = 700
display.set_caption('Shwooopterio')
window = display.set_mode((win_w, win_h))
background = transform.scale(image.load(img_back), (win_w, win_h))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
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
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top,  15, 20, -40)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, isLostable = True):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.isLostable = isLostable
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.x = randint(80, win_w - 80)
            self.rect.y = 0
            if self.isLostable:
                lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
            
player = Player(img_hero, 5 , win_h-100,65, 65, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_w - 80), -40, 65, 65, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy(img_ast, randint(30, win_w - 30), -40, 80 ,50, randint(1,7), False)
    asteroids.add(asteroid)

bullets = sprite.Group()

finish = False
run = True

rel_time = False
num_fire = 0

win = font2.render('YOU WIN!!!', True, (0,255,0))
lose = font2.render('YOU LOSER!!!', True, (255,0,0))


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 20 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 20 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_r:
                finish = False
                score = 0
                lost = 0
                for b in bullets:
                    b.kill()
                for m in monsters:
                    m.kill()
                for a in asteroids:
                    a.kill()
                for i in range(5):
                    monster = Enemy(img_enemy, randint(80, win_w - 80), -40, 65, 65, randint(1, 5))
                    monsters.add(monster)
                for i in range(3):
                    asteroid = Enemy(img_ast, randint(30, win_w - 30), -40, 80 ,50, randint(1,7), False)
                    asteroids.add(asteroid)


    if not finish:
        window.blit(background, (0, 0))

        player.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        text = font2.render(f'Сбито: {score}', 1, (255,255,255))
        window.blit(text, (10,20))
        text_lose = font2.render(f'Пропущено: {lost}', 1, (255,255,255))
        window.blit(text_lose, (10,50))
        text_help1 = font2.render(f'Для перезапуска нажмите R', 1, (255,255,255))
        window.blit(text_help1, (850, 550))
        text_help2 = font2.render(f'Для выстрела нажмите SPACE', 1, (255,255,255))
        window.blit(text_help2, (850, 600))
        text_help3 = font2.render(f'Для перемещения нажмите < или >', 1, (255,255,255))
        window.blit(text_help3, (850, 650))
        player.reset()

        if rel_time:

            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('reload', 1, (255,255,255))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_w - 80), -40, 65, 65, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player,asteroids , False) or lost >= 5:
            finish = True
            window.blit(lose, (200, 200))

        if score >= 10:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    time.delay(30)





