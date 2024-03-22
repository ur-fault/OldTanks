import pygame as pg
from settings import *
from tilemap import collide_hit_rect
import math
vec = pg.math.Vector2


class Turret(pg.sprite.Sprite):
    def __init__(self, game, x, y, rot, my_tank, is_main):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.turret_imgs[my_tank.tank_num]
        self.rect = self.image.get_rect()
        self.rot = rot
        self.pos = vec(x, y)
        self.rect.center = self.pos
        if is_main:
            self.rot_speed = 0

        self.my_tank = my_tank


class Tank(pg.sprite.Sprite):

    def __init__(self, game, x, y, rot, is_main, tank_num):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.player_imgs[tank_num]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.rect.center = self.hit_rect.center

        self.is_main = is_main
        self.tank_num = tank_num
        self.rot = 0
        self.turret = Turret(self.game, self.pos.x, self.pos.y, rot, self, is_main)

        if is_main:
            self.rot_speed = 0
            self.vel = vec(0, 0)
            self.pos_to_send = [self.tank_num, self.pos.x, self.pos.y, self.rot, self.turret.rot]
            self.last_shot = 0
            self.sent_bullet = False


    def get_keys(self):
        if self.is_main:
            self.sent_bullet = False
        self.rot_speed = 0
        self.vel = vec(0, 0)
        self.turret.rot_speed = 0
        keys = pg.key.get_pressed()
        if (keys[pg.K_w] or keys[pg.K_UP]) and not(keys[pg.K_s] or keys[pg.K_DOWN]):
            self.vel = vec(PLAYER_SPEED, 0).rotate(self.rot)
            if (keys[pg.K_a] or keys[pg.K_LEFT]) and not(keys[pg.K_d] or keys[pg.K_RIGHT]):
                self.rot_speed = -PLAYER_ROT_SPEED
                self.turret.rot_speed -= PLAYER_ROT_SPEED
            if (keys[pg.K_d] or keys[pg.K_RIGHT]) and not(keys[pg.K_a] or keys[pg.K_LEFT]):
                self.rot_speed = +PLAYER_ROT_SPEED
                self.turret.rot_speed += PLAYER_ROT_SPEED
        if (keys[pg.K_s] or keys[pg.K_DOWN]) and not(keys[pg.K_w] or keys[pg.K_UP]):
            self.vel = vec(-PLAYER_SPEED, 0).rotate(self.rot)
            if (keys[pg.K_a] or keys[pg.K_LEFT]) and not(keys[pg.K_d] or keys[pg.K_RIGHT]):
                self.rot_speed = +PLAYER_ROT_SPEED
                self.turret.rot_speed += PLAYER_ROT_SPEED
            if (keys[pg.K_d] or keys[pg.K_RIGHT]) and not(keys[pg.K_a] or keys[pg.K_LEFT]):
                self.rot_speed = -PLAYER_ROT_SPEED
                self.turret.rot_speed -= PLAYER_ROT_SPEED

        if self.turret.rot_speed == 0:
            if (keys[pg.K_a] or keys[pg.K_LEFT]) and not(keys[pg.K_d] or keys[pg.K_RIGHT]):
                self.rot_speed = -PLAYER_ROT_SPEED
                self.turret.rot_speed -= PLAYER_ROT_SPEED
            if (keys[pg.K_d] or keys[pg.K_RIGHT]) and not(keys[pg.K_a] or keys[pg.K_LEFT]):
                self.rot_speed = +PLAYER_ROT_SPEED
                self.turret.rot_speed += PLAYER_ROT_SPEED

        if keys[pg.K_q]:
            self.turret.rot_speed -= PLAYER_TURRET_SPEED
        if keys[pg.K_e]:
            self.turret.rot_speed += PLAYER_TURRET_SPEED

        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(self.turret.rot)
                Bullet(self.game, self.pos, dir, self.turret.rot)
                self.sent_bullet = True

    def get_info(self):
        # print("Read this:", data)
        data = self.game.network.data
        if data[0] == self.tank_num and data[0] != self.game.tank_num:
            self.pos.x = data[1]
            # print("pos x:", data[1])
            self.pos.y = data[2]
            # print("pos y:", data[2])
            self.rot = data[3]
            # print("rot:", data[3])
            self.turret.rot = data[4]
            # print("turret rot:", data[4])
            if len(data) > 5:
                Bullet(self.game, vec(data[1], data[2]),
                       vec(0, 1).rotate(data[4] - 90), data[4])


    def collide_with_walls(self, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls,
                                           False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.walls,
                                           False, collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def update(self):
        if self.is_main:
            self.get_keys()
            self.rot = int((self.rot + self.rot_speed * self.game.dt) % 360)
            self.pos += self.vel * self.game.dt
            self.hit_rect.centerx = self.pos.x
            self.collide_with_walls("x")
            self.hit_rect.centery = self.pos.y
            self.collide_with_walls("y")
        else:
            self.get_info()

        self.image = pg.transform.rotate(self.game.player_imgs[self.tank_num],
                                         -self.rot - 90)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        if self.is_main:
            self.turret.rot = int((self.turret.rot + self.turret.rot_speed
                                   * self.game.dt) % 360)

        self.turret.rect = self.turret.image.get_rect()
        self.turret.rect.center = self.rect.center
        self.turret.pos = self.turret.rect.center
        self.turret.image = pg.transform.rotate(self.game.turret_imgs[self.tank_num], -self.turret.rot - 90)
        #print("Turret rot speed: " + str(self.turret.rot_speed) + ", Turret rot: " + str(self.turret.rot))
        self.pos_to_send = [self.tank_num, self.pos.x, self.pos.y, self.rot, self.turret.rot]
        if self.is_main:
            if self.sent_bullet:
                self.pos_to_send.append(True)
        #self.game.network.send()

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, rot):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate(game.bullet_img, -rot - 90)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = vec(pos)
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        # self.image = pg.Surface((w, h))
        # self.image.fill(BLACK)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
