from pygame import mixer
import random
import pygame

pygame.init()

mixer.init()

mixer.music.load('space.ogg')
mixer.music.play(-1, 0.0)
fire_sound = mixer.Sound('fire.ogg')
explosion_sound = mixer.Sound('8-bit-explosion_F.wav')

screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Shooter")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_bullet = "bullet.png"
img_enemy = "ufo.png"

background = pygame.image.load(img_back)
hero_img = pygame.image.load(img_hero)
bullet_img = pygame.image.load(img_bullet)
enemy_img = pygame.image.load(img_enemy)


background = pygame.transform.scale(background, (700, 500)) 
hero_img = pygame.transform.scale(hero_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))
enemy_img = pygame.transform.scale(enemy_img, (40, 40)) 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = hero_img
        self.rect = self.image.get_rect(center=(700 // 2, 500 - 20))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < 700:
            self.rect.x += 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(20, 700-20), 0))

    def update(self):
        self.rect.y += 3
        if self.rect.top > 500:
            self.kill()
            global missed_enemies
            missed_enemies += 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 7
        if self.rect.bottom < 0:
            self.kill()

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

running = True
clock = pygame.time.Clock()
score = 0
missed_enemies = 0

while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            new_bullet = Bullet(player.rect.centerx, player.rect.top)
            all_sprites.add(new_bullet)
            bullets.add(new_bullet)
            fire_sound.play()

    if random.randint(1, 40) == 1:
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)

    all_sprites.update()

    for bullet in bullets:
        hits = pygame.sprite.spritecollide(bullet, enemies, True)
        if hits:
            bullet.kill()
            score += 1
            explosion_sound.play()

    all_sprites.draw(screen)

    font = pygame.font.Font(None, 36)
    text = font.render("Рахунок: " + str(score) + " | Пропущено: " + str(missed_enemies), True, WHITE)
    screen.blit(text, (10, 10))

    if score >= 30:
        win_text = font.render("ВИГРАВ!", True, GREEN)
        screen.blit(win_text, (700 // 2 - 50, 500 // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
    if missed_enemies >= 3:
        lose_text = font.render("ПРОГРАВ!", True, RED)
        screen.blit(lose_text, (700 // 2 - 50, 500 // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    pygame.display.flip()

pygame.quit()
 