import pygame
import random


green = (100, 200, 100)
pink = (250, 150, 200)


def random_color():
    r = random.randrange(1, 255)
    g = random.randrange(1, 255)
    b = random.randrange(1, 255)
    return r, g, b


class Bullet:
    def __init__(self, x, y):
        self.hidden = False
        self.rect = pygame.Rect(x, y, 15, 15)


class Weapon:
    def __init__(self, x, y, type):
        self.bullet_list = []
        self.rect = pygame.Rect(x, y, 50, 50)
        self.delay = 0
        self.animation_delay = 0
        self.weapon_type = type
        self.dead = False

        if type == 1: self.health = 5
        elif type == 2: self.health = 10
        elif type == 3: self.health = 20
        elif type == 4: self.health = 1

        self.image_x = 0
        self.image_y = 0

        self.thrower_sprite = pygame.image.load("thrower.png")
        self.sorcerer_sprite = pygame.image.load("sorcerer.png")
        self.pig_sprite = pygame.image.load("pig.png")
        self.maiden_sprite = pygame.image.load("maiden.png")

    def update(self):
        if self.dead is True:
            self.image_y = 50

            if self.animation_delay == 5:
                self.image_x += 50
                self.animation_delay = 0
            else:
                self.animation_delay += 1

            if self.weapon_type == 2:
                if self.image_x > 250:
                    weapon_list.remove(self)
            elif self.weapon_type == 4 or self.weapon_type == 3 or self.weapon_type == 1:      
                if self.image_x > 200:
                    weapon_list.remove(self)
        else:
            if self.animation_delay == 16:
                self.image_x += 50
                self.animation_delay = 0
            else:
                self.animation_delay += 1

            if self.weapon_type == 1:
                if self.image_x > 650:
                    self.image_x = 0
            elif self.weapon_type == 2:
                if self.image_x > 400:
                    self.image_x = 0
            elif self.weapon_type == 3:
                if self.image_x > 350:
                    self.image_x = 0
            elif self.weapon_type == 4:
                if self.image_x > 200:
                    self.image_x = 0

            if self.weapon_type == 1:
                if self.delay == 200:
                    user_interface.points += 20
                    self.delay = 0
                else:
                    self.delay += 1
            elif self.weapon_type == 2:
                if self.delay == 150:
                    if self.image_x == 400:
                        self.bullet_list.append(Bullet(self.rect.right, (self.rect.y+((50/2)-5))))
                        self.delay = 0
                else:
                    self.delay += 1

                for bullet in self.bullet_list:
                    bullet.rect.x += 2

                    for enemy in enemy_list:
                        if bullet.rect.colliderect(enemy.rect):
                            if bullet.hidden is False:
                                hit_sound.play()
                                enemy.health -= 1
                                bullet.hidden = True
                                if enemy.health <= 0:
                                    enemy.dead = True
                                    user_interface.enemies_killed += 1

    def draw(self, display):
        if self.weapon_type == 1:
            display.blit(self.sorcerer_sprite, (self.rect.x, self.rect.y), (self.image_x, self.image_y, 50, 50))
        elif self.weapon_type == 2:
            display.blit(self.thrower_sprite, (self.rect.x, self.rect.y), (self.image_x, self.image_y, 50, 50))
        elif self.weapon_type == 3:
            display.blit(self.pig_sprite, (self.rect.x, self.rect.y), (self.image_x, self.image_y, 50, 50))
        elif self.weapon_type == 4:
            display.blit(self.maiden_sprite, (self.rect.x, self.rect.y), (self.image_x, self.image_y, 50, 50))


class Enemy:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.move_delay = 0
        self.animation_delay = 0
        self.attack_delay = 0
        self.image_x = 150
        self.image_y = 0
        self.enemy_type = type
        self.dead = False

        if self.enemy_type == 1:
            self.sprite = pygame.image.load("bear.png")
            self.attack_sound = pygame.mixer.Sound("chomp.wav")
            self.health = 10
            self.damage = 1
        elif self.enemy_type == 2:
            self.sprite = pygame.image.load("gorilla.png")
            self.attack_sound = pygame.mixer.Sound("chomp.wav")
            self.health = 15
            self.damage = 1
        elif self.enemy_type == 3:
            self.sprite = pygame.image.load("panda.png")
            self.attack_sound = pygame.mixer.Sound("panda_hit.wav")
            self.health = 30
            self.damage = 3

    def update(self):
        if self.dead is True:
            self.image_y = 100
            if self.animation_delay == 5:
                self.image_x += 50
                self.animation_delay = 0
            else:
                self.animation_delay += 1

            if self.image_x > 150:
                enemy_list.remove(self)
                if self.enemy_type == 1 or self.enemy_type == 2:
                    minion_death.play()
                elif self.enemy_type == 3:
                    panda_death.play()
                    user_interface.boss_killed = True
        else:
            if self.move_delay == 5:
                self.rect.x -= user_interface.enemy_move_speed
                self.move_delay = 0

                if self.animation_delay == 2:
                    self.image_x += 50
                    self.animation_delay = 0
                else:
                    self.animation_delay += 1

                if self.image_y == 50:
                    if self.image_x > 50:
                        self.image_x = 0
                else:
                    if self.image_x > 150:
                        self.image_x = 0
            else:
                self.move_delay += 1

        for weapon in weapon_list:
            if self.rect.colliderect(weapon.rect):
                self.rect.left = weapon.rect.right
                if self.attack_delay == 5:
                    self.attack_sound.play()
                    weapon.health -= self.damage
                    if weapon.health <= 0 and weapon.dead is False:
                        weapon.dead = True
                        weapon.image_x = 0
                        weapon.animation_delay = 0
                        if weapon.weapon_type == 1:
                            sorcerer_death.play()
                        elif weapon.weapon_type == 2:
                            thrower_death.play()
                        elif weapon.weapon_type == 3:
                            pig_death.play()
                        elif weapon.weapon_type == 4:
                            maiden_death.play()
                    self.attack_delay = 0
                    if weapon.weapon_type == 4 and weapon.dead is True:
                        for enemy in enemy_list:
                            if enemy.rect.y == weapon.rect.y:
                                enemy.dead = True
                                enemy.image_x = 0
                                user_interface.enemies_killed += 1
                else:
                    self.attack_delay += 1

    def draw(self, game_display):
        collide = False
        for weapon in weapon_list:
            if weapon.rect.right == enemy.rect.left:
                if weapon.rect.top == enemy.rect.top:
                    collide = True
                    break

        if collide:
            enemy.image_y = 50
        else:
            enemy.image_y = 0

        if self.dead is True:
            enemy.image_y = 100

        game_display.blit(self.sprite, (self.rect.x, self.rect.y), (self.image_x, self.image_y, 50, 50))


class UI:
    def __init__(self):
        self.points = 200
        self.font = pygame.font.SysFont('arial', 40)
        self.box_a = pygame.Rect(0, 0, 50, 50)
        self.box_b = pygame.Rect(50, 0, 50, 50)
        self.box_c = pygame.Rect(100, 0, 50, 50)
        self.enemies_killed = 0
        self.enemies_spawned = 0
        self.enemy_move_speed = 1
        self.spawn_delay = 200
        self.level = 1
        self.boss_killed = False

        self.sorcerer_icon = pygame.image.load("sorcerer_icon.png")
        self.thrower_icon = pygame.image.load("thrower_icon.png")
        self.pig_icon = pygame.image.load("pig_icon.png")


    def draw(self, display):
        string = "points: " + str(self.points)
        
        game_display.blit(self.sorcerer_icon, (self.box_a.x, self.box_a.y), (0, 0, 50, 50))
        game_display.blit(self.thrower_icon, (self.box_b.x, self.box_b.y), (0, 0, 50, 50))
        game_display.blit(self.pig_icon, (self.box_c.x, self.box_c.y), (0, 0, 50, 50))
        points_label = self.font.render(str(string), True, (255, 255, 255))
        score_label = self.font.render(str(self.enemies_killed), True, (255, 255, 255))
        display.blit(points_label, (screen_width/2 - 60, -3))
        display.blit(score_label, (500, -3))

def start_screen():
    play_button = pygame.image.load("play_button.png")
    quit_button = pygame.image.load("quit_button.png")
    logo = pygame.image.load("logo.png")
    bg_1 = pygame.image.load("scroll_bg.png")
    bg_2 = pygame.image.load("scroll_bg.png")
    bg_1_x = 0
    bg_2_x = -screen_width

    start_screen_done = False
    font = pygame.font.SysFont('arial', 50)
    label = font.render(str("The Wild"), True, (255, 255, 255))

    while not start_screen_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(-1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit(-1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if (screen_width/2 - 60)+140 > mouse[0] > (screen_width/2 - 60) and (screen_height/2)+40 > mouse[1] > (screen_height/2):
                    start_screen_done = True
                elif (screen_width/2 - 60)+140 > mouse[0] > (screen_width/2 - 60) and (screen_height/2+70)+40 > mouse[1] > (screen_height/2+70):
                    exit(-1)

        bg_1_x += 2
        bg_2_x += 2

        if bg_1_x >= screen_width:
            bg_1_x = -screen_width
        elif bg_2_x >= screen_width:
            bg_2_x = -screen_width

        game_display.fill((200, 150, 100))
        game_display.blit(menu_bg_sprite, (0, 0))
        game_display.blit(bg_1, (bg_1_x, 0))
        game_display.blit(bg_2, (bg_2_x, 0))
        game_display.blit(play_button, (screen_width/2 - 60, screen_height/2), (0, 0, 140, 50))
        game_display.blit(quit_button, (screen_width/2 - 60, screen_height/2 + 70), (0, 0, 140, 50))
        game_display.blit(logo, (50, 80))

        pygame.display.update()
        clock.tick(FPS)

    return


def success_screen():
    play_button = pygame.image.load("play_button.png")
    quit_button = pygame.image.load("quit_button.png")

    start_screen_done = False
    font = pygame.font.SysFont('arial', 50)
    string = "Level " + str(user_interface.level)
    label = font.render(str(string), True, (255, 255, 255))

    while not start_screen_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(-1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit(-1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if (screen_width/2 - 60)+140 > mouse[0] > (screen_width/2 - 60) and (screen_height/2)+40 > mouse[1] > (screen_height/2):
                    start_screen_done = True
                elif (screen_width/2 - 60)+140 > mouse[0] > (screen_width/2 - 60) and (screen_height/2+70)+40 > mouse[1] > (screen_height/2+70):
                    exit(-1)

        game_display.fill((200, 150, 100))
        game_display.blit(menu_bg_sprite, (0, 0))
        game_display.blit(play_button, (screen_width/2 - 60, screen_height/2), (0, 0, 140, 50))
        game_display.blit(quit_button, (screen_width/2 - 60, screen_height/2 + 70), (0, 0, 140, 50))
        game_display.blit(label, (screen_width/2 - 60, screen_height/2 - 80))

        pygame.display.update()
        clock.tick(FPS)

    return


def fail_screen():
    play_again_button = pygame.image.load("play_again_button.png")
    quit_button = pygame.image.load("quit_button.png")

    start_screen_done = False
    font = pygame.font.SysFont('arial', 50)
    string = "Game Over"
    label = font.render(str(string), True, (255, 255, 255))

    while not start_screen_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(-1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit(-1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if (screen_width/2 - 20)+140 > mouse[0] > (screen_width/2 - 60) and (screen_height/2)+40 > mouse[1] > (screen_height/2):
                    start_screen_done = True
                elif (screen_width/2 - 20)+140 > mouse[0] > (screen_width/2 - 60) and (screen_height/2+70)+40 > mouse[1] > (screen_height/2+70):
                    exit(-1)

        game_display.fill((200, 150, 100))
        game_display.blit(menu_bg_sprite, (0, 0))
        game_display.blit(play_again_button, (screen_width/2 - 60, screen_height/2), (0, 0, 140, 50))
        game_display.blit(quit_button, (screen_width/2 - 60, screen_height/2 + 70), (0, 0, 140, 50))
        game_display.blit(label, (screen_width/2 - 100, screen_height/2 - 80))

        pygame.display.update()
        clock.tick(FPS)

    return


pygame.init()
screen_width = 600
screen_height = 400
game_display = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
done = False
FPS = 60

bg_sprite = pygame.image.load("background.png")
menu_bg_sprite = pygame.image.load("menu_bg.png")
grass_sprite = pygame.image.load("grass.png")
sky_sprite = pygame.image.load("sky.png")
rock_sprite = pygame.image.load("rock.png")
sorcerer_cursor = pygame.image.load("sorcerer_cursor.png")
thrower_cursor = pygame.image.load("thrower_cursor.png")
pig_cursor = pygame.image.load("pig_cursor.png")

plant_sound = pygame.mixer.Sound("plant.wav")
bullet_sound = pygame.mixer.Sound("bullet.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
bg_sound = pygame.mixer.Sound("ambient.wav")
select_sound = pygame.mixer.Sound("select.wav")
minion_death = pygame.mixer.Sound("minion_death.wav")
panda_hit = pygame.mixer.Sound("panda_hit.wav")
panda_death = pygame.mixer.Sound("panda_death.wav")

thrower_spawn = pygame.mixer.Sound("thrower_spawn.wav")
thrower_death = pygame.mixer.Sound("thrower_death.wav")
sorcerer_spawn = pygame.mixer.Sound("sorcerer_spawn.wav")
sorcerer_death = pygame.mixer.Sound("sorcerer_death.wav")
pig_spawn = pygame.mixer.Sound("pig_spawn.wav")
pig_death = pygame.mixer.Sound("pig_death.wav")
maiden_death = pygame.mixer.Sound("maiden_death.wav")

font = pygame.font.SysFont('arial', 50)
label = font.render(str("COLLIDE"), True, (255, 255, 255))

block_list = []

x = y = 0
for i in range(8):
    for j in range(12):
        block_list.append(pygame.Rect(x, y, 50, 50))
        x += 50
    y += 50
    x = 0

weapon_list = []
enemy_list = []
spawn_delay = 0
spawn_type = 1
spawn_gorilla = 0
user_interface = UI()

bg_sound.play(loops=-1)
start_screen()

y_list = []
for i in range(3):
    y = random.randrange(1, 8)
    if y not in y_list:
        y_list.append(y)
        weapon_list.append(Weapon(0, y*50, 4))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            for block in block_list:
                if block.x+50 > mouse[0] > block.x and block.y+50 > mouse[1] > block.y:
                    if mouse[1] > 50:
                        if not enemy_list:
                            collide = False
                            for weapon in weapon_list:
                                if weapon.rect.colliderect(block):
                                    collide = True
                                    break
                            if collide is False:
                                if spawn_type == 1 and user_interface.points >= 50:
                                    user_interface.points -= 50
                                    weapon_list.append(Weapon(block.x, block.y, spawn_type))
                                    #plant_sound.play()
                                    sorcerer_spawn.play()
                                elif spawn_type == 2 and user_interface.points >= 100:
                                    user_interface.points -= 100
                                    weapon_list.append(Weapon(block.x, block.y, spawn_type))
                                    #plant_sound.play()
                                    thrower_spawn.play()
                                elif spawn_type == 3 and user_interface.points >= 50:
                                    user_interface.points -= 100
                                    weapon_list.append(Weapon(block.x, block.y, spawn_type))
                                    #plant_sound.play()
                                    pig_spawn.play()

                        else:
                            collide = False
                            for enemy in enemy_list:
                                if enemy.rect.colliderect(block):
                                    collide = True
                                    break
                            if collide is False:
                                collide = False
                                for weapon in weapon_list:
                                    if weapon.rect.colliderect(block):
                                        collide = True
                                        break
                                if collide is False:
                                    if spawn_type == 1 and user_interface.points >= 50:
                                        user_interface.points -= 50
                                        weapon_list.append(Weapon(block.x, block.y, spawn_type))
                                        #plant_sound.play()
                                        sorcerer_spawn.play()
                                    elif spawn_type == 2 and user_interface.points >= 100:
                                        user_interface.points -= 100
                                        weapon_list.append(Weapon(block.x, block.y, spawn_type))
                                        #plant_sound.play()
                                        thrower_spawn.play()
                                    elif spawn_type == 3 and user_interface.points >= 50:
                                        user_interface.points -= 50
                                        weapon_list.append(Weapon(block.x, block.y, spawn_type))
                                        #plant_sound.play()
                                        pig_spawn.play()
                    else:
                        if mouse[0] < 50:
                            spawn_type = 1
                            select_sound.play()
                        elif 50 <= mouse[0] < 100:
                            spawn_type = 2
                            select_sound.play()
                        elif 100 <= mouse[0] < 150:
                            spawn_type = 3
                            select_sound.play()
                            
    # spawn enemy
    if spawn_delay == user_interface.spawn_delay:
        rect = pygame.Rect(screen_width, (random.randrange(1, 8)*50), 50, 50)

        for enemy in enemy_list:
            while rect.colliderect(enemy.rect):
                rect = pygame.Rect(screen_width, (random.randrange(1, 8)*50), 50, 50)

        if spawn_gorilla == 4:  # spawn a gorilla for every 4 polar bears
            enemy_spawn = 2
            spawn_gorilla = 0
        else:
            enemy_spawn = 1
            spawn_gorilla += 1

        if user_interface.enemies_spawned < 15:
            enemy_list.append(Enemy(rect.x, rect.y, enemy_spawn))
            user_interface.enemies_spawned += 1
        elif user_interface.enemies_spawned == 15:
            if user_interface.enemies_killed >= 15:
                user_interface.enemy_move_speed = 3
                enemy_list.append(Enemy(rect.x, rect.y, 3))
                user_interface.enemies_spawned += 1

        spawn_delay = 0
    else:
        spawn_delay += 1

    # update enemy
    for enemy in enemy_list:
        enemy.update()

        if enemy.rect.x == 0:
            fail_screen()
            enemy_list = []
            weapon_list = []
            user_interface.points = 200
            user_interface.enemies_killed = 0
            user_interface.enemies_spawned = 0
            user_interface.spawn_delay = 200
            user_interface.level = 1

            y_list = []
            for i in range(3):
                y = random.randrange(1, 8)
                if y not in y_list:
                    y_list.append(y)
                    weapon_list.append(Weapon(0, y*50, 4))

    # shoot bullets from weapons
    for weapon in weapon_list:
        weapon.update()

    if user_interface.boss_killed is True:
        enemy_list = []
        weapon_list = []
        user_interface.enemies_killed = 0
        user_interface.enemies_spawned = 0
        user_interface.spawn_delay -= 15
        user_interface.level += 1
        user_interface.points = 200
        user_interface.enemy_move_speed = 1
        user_interface.boss_killed = False

        y_list = []
        for i in range(3):
            y = random.randrange(1, 8)
            if y not in y_list:
                y_list.append(y)
                weapon_list.append(Weapon(0, y*50, 4))

        success_screen()

    game_display.fill((255, 255, 255))

    for block in block_list:
        if block.y == 0:
            game_display.blit(sky_sprite, (block.x, block.y), (0, 0, 50, 50))
        else:
            game_display.blit(grass_sprite, (block.x, block.y), (0, 0, 50, 50))

    game_display.blit(bg_sprite, (0, 0))

    mouse = pygame.mouse.get_pos()

    for block in block_list:
        if block.x+50 > mouse[0] > block.x and block.y+50 > mouse[1] > block.y:
            if spawn_type == 1 and mouse[1] > 50:
                game_display.blit(sorcerer_cursor, (block.x, block.y), (0, 0, 50, 50))
            elif spawn_type == 2 and mouse[1] > 50:
                game_display.blit(thrower_cursor, (block.x, block.y), (0, 0, 50, 50))
            elif spawn_type == 3 and mouse[1] > 50:
                game_display.blit(pig_cursor, (block.x, block.y), (0, 0, 50, 50))
        
    for weapon in weapon_list:
        weapon.draw(game_display)

    for weapon in weapon_list:
        for bullet in weapon.bullet_list:
            if bullet.hidden is False:
                game_display.blit(rock_sprite, (bullet.rect.x, bullet.rect.y), (0, 0, 15, 15))

    for enemy in enemy_list:
        enemy.draw(game_display)

    user_interface.draw(game_display)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
