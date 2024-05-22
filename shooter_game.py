#Создай собственный Шутер!

from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
            
            
    
    def fire(self):
        global bullets
        bullet = Bullet('bullet.png', self.rect.x, self.rect.y, 5)
        mixer.music.load('fire.ogg')
        mixer.music.play()
        bullets.add(bullet)


lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(0, 500)
            lost = lost + 1


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(0, 500)




class Bullet(GameSprite):
    def update(self): 
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            

 

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80)



win_width = 700
win_height = 500
mw = display.set_mode(
    (win_width, win_height)
)
display.set_caption('Shuter')
background = transform.scale(
    image.load('galaxy.jpg'),
    (win_width, win_height)
)

clock = time.Clock()
FPS = 60

#TODO Музыка

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

player = Player('rocket.png', 350, 410, 5)

#? Монстры

monster1 = Enemy('ufo.png', randint(0, 500), 0, randint(1, 6))
monster2 = Enemy('ufo.png', randint(0, 500), 0, randint(1, 6))
monster3 = Enemy('ufo.png', randint(0, 500), 0, randint(1, 6))
monster4 = Enemy('ufo.png', randint(0, 500), 0, randint(1, 6))
monster5 = Enemy('ufo.png', randint(0, 500), 0, randint(1, 6))

monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

#! Пули

bullets = sprite.Group()

asteroid1 = Asteroid('asteroid.png', randint(0, 500), 0, randint(1, 6))
asteroid2 = Asteroid('asteroid.png', randint(0, 500), 0, randint(1, 6))
asteroid3 = Asteroid('asteroid.png', randint(0, 500), 0, randint(1, 6))

#* Астероиды

asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)

finish = False

win = 0

life_counter = 3

game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    if not finish:
        mw.blit(background, (0, 0))
        player.reset()
        player.update()
        bullets.update()
        bullets.draw(mw)
        monsters.draw(mw)
        monsters.update()
        asteroids.draw(mw)
        asteroids.update()
        sprite_list = sprite.groupcollide(
            monsters, bullets, True, True
        )
        collide = sprite.spritecollide(
            player, monsters, True
        )
        collide1 = sprite.spritecollide(
            player, asteroids, True
        )
        for e in sprite_list:
            win += 1
            monster = Enemy('ufo.png', randint(0, 500), 0, randint(1, 6))
            monsters.add(monster)
        if win >= 10:
            finish = True
            win1 = font1.render('You win!', 1, (255,255,255))
            mw.blit(win1, (0, 0))
        if len(collide) > 0 or lost >= 3:
            life_counter -= 1
            monster = Enemy('ufo.png', randint(0, 500), 0, randint(1, 6))
            monsters.add(monster)
        if len(collide1) > 0:
            life_counter -= 1
            asteroid = Asteroid('asteroid.png', randint(0, 500), 0, randint(1, 6))
            asteroids.add(asteroid)
        if life_counter <= 0:
            finish = True
            lose = font1.render('You lose!', 1, (255,255,255))
            mw.blit(lose, (0, 0))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text_win = font1.render('Счёт:' + str(win), 1, (255, 255, 255))
        text_life = font2.render(str(life_counter), 1, (255, 0, 0))
        mw.blit(text_lose, (50, 80))
        mw.blit(text_win, (50, 50))
        mw.blit(text_life, (650, 50))
        display.update()
        clock.tick(FPS)