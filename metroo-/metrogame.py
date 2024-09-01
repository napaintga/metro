from pygame import *
from random import randint
from time import time as timer
mixer.init()
fire_sound = mixer.Sound("bulletsound.mp3") 




wn = display.set_mode((640*1.5,243*1.5))
clock = time.Clock()
display.set_caption("Шутер")
font.init()
font1 = font.Font(None,36)
background = transform.scale(image.load("metro1.png"),(640*1.5,243*1.5))
background2 = transform.scale(image.load("metro2.png"),(640*1.5,243*1.5))
background3 = transform.scale(image.load("metro3.png"),(640*1.5,243*1.5))
w_e = 320
x_e= 240
enemy_l = []

for i in range(1,10):
    img = image.load(f"en/video_00{i}.png")
    scaled_img = transform.scale(img, (w_e, x_e))
    enemy_l.append(scaled_img)
    enemy_l.append(scaled_img)

for i in range(10,64):
    img = image.load(f"en/video_0{i}.png")
    scaled_img = transform.scale(img, (w_e, x_e))
    enemy_l.append(scaled_img)
    enemy_l.append(scaled_img)

FPS = 40
class GameSprite(sprite.Sprite):
    def __init__(self,pl_image,pl_x,pl_y,size_x,size_y,pl_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pl_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
        self.speed = pl_speed
        self.size_x = size_x
        self.count=0
    def reset(self):
        wn.blit(self.image,(self.rect.x,self.rect.y))
    def animation(self,list):
                self.count = (self.count + 1) % len(list)  
                wn.blit(list[self.count], (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 63:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 1000 - self.size_x:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("abullet.png", self.rect.centerx+42, self.rect.top+20,15,20, 5)
        bullets.add(bullet)

#enemyl = [transform.scale(  image.load(''), (70, 110)),
          #transform.scale(  image.load('pr1.png'), (70, 110)),]

class Enemy(GameSprite):
    
    
    def update(self):
        global lose

        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(75,620)
            self.speed = randint(1,5)

bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
            self.rect.x += self.speed
            if self.rect.x > 640*1.5:
                self.kill()

            
game = True
num_bul = 6
cur_bul = 0
fire_bul= True
hero = Player("hero.png", 100,150,132,132,5)
enemy1 = Enemy("en/video_001.png", 500,100,132,132,5)
enemy1_show = 1
enemy1_kill = 0
enemy1_hp = 10
global last_time
last_time = 0 

level1 = True
level2 = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if cur_bul <= num_bul and fire_bul == False:
                    fire_sound.play()
                    hero.fire()
                    cur_bul +=1
                elif  cur_bul >= num_bul and fire_bul == False:
                    fire_bul = True
                    hero.fire()
                    last_time = timer()
        
    if level1:
        wn.blit(background,(0,0))
        text_score = font1.render("Рахунок: " + str(hero.rect.x),1,(255,255,255))
        wn.blit(text_score,(10,20))
        hero.reset()
        hero.update()
        if enemy1_show:
            enemy1.animation(enemy_l)
        if enemy1_kill:
            enemy1.reset()
                
        bullets.draw(wn)
        bullets.update()

        if fire_bul == True:
                now_time = timer()
                if now_time - last_time < 2:
                    reload = font1.render("RELOAD: ", 1,(160,25,2))
                    wn.blit(reload,(250,10))
                else:
                    fire_bul = False
                    cur_bul = 0




        collides_enemy = sprite.spritecollide(enemy1,bullets,True)
        if collides_enemy:
            enemy1_show = 0
            enemy1_kill = 1

        if  610 < hero.rect.x   <670:
            level1 = False
            level2 = True
            enemy1_kill = 0
            
    if level2:
        wn.blit(background2,(0,0))
        text_score = font1.render("Рахунок: " + str(hero.rect.x),1,(255,255,255))
        wn.blit(text_score,(10,20))
        hero.reset()
        hero.update()
        if enemy1_show:
            enemy1.animation(enemy_l)
        bullets.draw(wn)
        bullets.update()


    clock.tick(FPS)
    display.update()