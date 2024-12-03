import pygame

pygame.init()

screen_title = 'GAME'
screen_width = 1000
screen_hight = 700
screen_color = (100, 100, 100)

screen = pygame.display.set_mode((screen_width, screen_hight))

fps = 60
clock = pygame.time.Clock()

class Hitbox():
    def __init__(self, x, y, width, hight, color):
        self.x = x
        self.y = y
        self.width = width
        self.hight = hight
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.hight)

    def draw_hitbox(self):
        pygame.draw.rect(screen, self.color, self.rect, 1)

class Picture(Hitbox):
    def __init__(self, x, y, width, hight, color, img_url):
        Hitbox.__init__(self, x, y, width, hight, color)
        self.img_url = img_url
        self.image = pygame.transform.scale(pygame.image.load(self.img_url).convert_alpha(), (self.width, self.hight))
    
    def draw_picture(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Pol(Picture):
    def __init__(self, x, y, width, hight, color, img_url):
        Picture.__init__(self, x, y, width, hight, color, img_url)
        self.o_type = 'D'

class Enemy(Picture):
    def __init__(self, x, y, width, height, color, img_url, speed):
        Picture.__init__(self, x, y, width, height, color, img_url)
        self.speed = speed
        self.dx = 0
        self.hp_enemy = 3
        self.o_type = 'B'
    
    def draw_enemy(self,):
        self.draw_picture()

    def bind_to_flet(self, bind_flet):
        self.bind_flet = bind_flet
        self.a = self.bind_flet.rect.left
        self.b = self.bind_flet.rect.right
        self.rect.bottom = self.bind_flet.rect.top
    
    def set_move(self, start_direction):
        self.rect.centerx = self.bind_flet.rect.centerx
        if start_direction == 'left':
            self.dx = -1
        elif start_direction == 'right':
            self.dx = 1
    
    def move_enemy(self):
        self.rect.x += self.speed * self.dx
        if self.rect.left < self.a:
            self.rect.left = self.a
            self.dx *= -1
        elif self.rect.right > self.b:
            self.rect.right = self.b
            self.dx *= -1

    

class Angel(Picture):
    def __init__(self, x, y, width, hight, color, img_url, speed):
        Picture.__init__(self, x, y, width, hight, color, img_url)
        self.speed = speed
        self.dx = 0
        self.dy = 0
        self.attack_direction = 'right'
        self.last_attack_direction = self.attack_direction
        self.graviti = 5
        self.o_type = 'A'
        self.on_grayn = False
        self.is_jamp = False
        self.jamp_force = 7
        self.jamp_count = -5
        self.hp = 5
        self.is_hitted = False
        self.shild_counter = 0
        self.shild_delay = 2

    def jamp(self):
        if self.is_jamp:
            self.rect.y += self.jamp_force * (self.jamp_count // 2)
            self.jamp_count += 0.5
        if self.jamp_count == 5:
            self.jamp_count = -5
            self.is_jamp = False

    def falling(self):
        if not self.is_jamp:
            self.rect.y += self.graviti
    
    def collid_pol(self, flets):
        for flet in flets:
            if self.rect.colliderect(flet.rect):
                self.on_grayn = True
                if self.rect.bottom - flet.rect.top <= self.graviti * 1.5:
                    self.rect.bottom = flet.rect.top
                '''else:
                    delta_x = min(abs(self.rect.left - flet.rect.right), abs(self.rect.right - flet.rect.left))
                    delta_y = min(abs(self.rect.top - flet.rect.bottom), abs(self.rect.bottom - flet.rect.top))
                    if delta_x > delta_y:
                        collision = 'vert'
                    elif delta_x < delta_y:
                        collision = 'horiz'
                    else:
                        collision = 'oth'
                    
                    if collision == 'vert':
                        self.rect.top = flet.rect.bottom
                        self.is_jamp = False
                    elif collision == 'horiz':
                        if self.dx < 0:
                            self.rect.left = flet.rect.right
                            self.is_jamp = False
                        elif self.dx > 0:
                            self.rect.right = flet.rect.left
                            self.is_jamp = False
                    elif collision == 'oth':
                        self.rect.top = flet.rect.bottom
                        if self.dx < 0:
                            self.rect.left = flet.rect.right
                        elif self.dx > 0:
                            self.rect.right = flet.rect.left
                        self.is_jamp = False'''
                break
            self.on_grayn = False

    def col_enemy(self, enemys):
        for enemy in enemys:
            if self.rect.colliderect(enemy.rect) and not self.is_hitted:
                self.hp -= 1
                self.is_hitted = True

    def chek_shild(self):
        if self.is_hitted == True:
            if self.shild_counter >= fps * self.shild_delay:
                self.shild_counter = 0
                self.is_hitted = False
            else:
                self.shild_counter += 1

    def control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.attack_direction = 'left'
            self.dx = -1
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.attack_direction = 'right'
            self.dx = 1
        else:
            self.dx = 0
        self.last_attack_direction = self.attack_direction
        if keys[pygame.K_w]:
            self.attack_direction = 'up'
        else:
            self.attack_direction = self.last_attack_direction
        if keys[pygame.K_SPACE]:
            if self.on_grayn:
                self.is_jamp = True

    def attack(self, sprait_list):
        for sprait in sprait_list:
            if abs(self.rect.centerx - sprait.rect.centerx) <= self.width // 2 + self.width // 2 + 50:
                if self.rect.centerx < sprait.rect.centerx:
                    if self.attack_direction == 'right':
                        sprait.hp_enemy -= 1
                elif self.rect.centerx > sprait.rect.centerx:
                    if self.attack_direction == 'left':
                        sprait.hp_enemy -= 1


    def move(self):
        self.rect.x += self.dx * self.speed

    def draw_angel(self):
        self.draw_picture()

echo = Angel(200, 300, 50, 50, (100, 250, 100), 'ghost.png', 5)
proto = Enemy(0, 0, 50, 50, (250, 100, 100), 'ufo.png', 4)

game_objects = {
    'A': echo,
    'B':[proto,],  
    #'C':
    'D':[Pol(0, 650, 1000, 50, (100, 100, 100), 'brick-wall.png'), Pol(700, 550, 300, 50, (100, 100, 100), 'brick-wall.png')]
}

game_objects['B'][0].bind_to_flet(game_objects['D'][1])
game_objects['B'][0].set_move('left')

font_family = None
font_size = 32
main_font = pygame.font.SysFont(font_family, font_size)
win = False
lose = False



is_on = True
while is_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_on = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                game_objects['A'].attack(game_objects['B'])


    screen.fill(screen_color)

    if not win and not lose:

        if game_objects['A'].hp != 0:
            for game_object in game_objects:
                if game_object == 'A':
                    game_objects[game_object].draw_angel()
                    game_objects[game_object].move()
                    game_objects[game_object].control()
                    game_objects[game_object].falling()
                    game_objects[game_object].collid_pol(game_objects['D'])
                    game_objects[game_object].jamp()
                    game_objects[game_object].col_enemy(game_objects['B'])
                    game_objects[game_object].chek_shild()
                elif game_object == 'B':
                    for i in game_objects[game_object]:
                        i.draw_enemy()
                        i.move_enemy()
                        if i.hp_enemy <= 0:
                            game_objects[game_object].remove(i)
                elif game_object == 'D':
                    for i in game_objects[game_object]:
                        i.draw_picture()

                screen.blit(main_font.render('Здаровье: ' + str(game_objects['A'].hp), True, (200, 200, 200)), (20, 20))
                screen.blit(main_font.render('Щит: ' + str(game_objects['A'].is_hitted), True, (200, 200, 200)), (20, 40))
                #screen.blit(main_font.render('Здаровье: ' + str(game_objects['B'][0].hp_enemy), True, (200, 200, 200)), (700, 20))

        #elif :
        #    win = True
        #    if win == True:
        #        screen.blit(main_font.render('ВЫ ВЫЙГРАЛИ', True, (200, 200, 200)), (200, 300))
    if game_objects['A'].hp <= 0:
        lose = True
        if lose == True:
            screen.blit(main_font.render('ВЫ ПРОИГРАЛИ', True, (200, 200, 200)), (200, 300))
    

    pygame.display.update()
    clock.tick(fps)
    '''Pol(350, 650, 300, 50, (100, 100, 100), 'brick-wall.png'), Pol(450, 500, 50, 50, (100, 100, 100), 'brick-wall.pn'''