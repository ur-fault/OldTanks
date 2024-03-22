# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 1
# Project setup
# Video link: https://youtu.be/3UxnelT9aCo
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
import network
import pickle
from math import atan, pi

class Game:
    def __init__(self):
        pg.init()
        self.load_data()
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.tanks = []

    def load_data(self):
        self.network = network.Network()

        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        map_folder = path.join(game_folder, "maps")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.map = TiledMap(path.join(map_folder, "battlefield0.tmx"))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.old_map = Map(path.join(game_folder, "map.txt"))
        self.player_imgs = [pg.image.load(path.join(img_folder, img)) for img in PLAYER_IMGS]
        self.turret_imgs = [pg.image.load(path.join(img_folder, img)) for img in TURRET_IMGS]
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG))
        self.tank_num = self.network.order[1:][self.network.order[0]]
        print("My tank number is", self.tank_num)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name in ["0", "1", "2", "3"]:
                print("Tile's number is", tile_object.name)
                if int(tile_object.name) == self.tank_num:
                    self.tanks.insert(0, Tank(self, tile_object.x, tile_object.y,
                                              (atan((tile_object.height - HEIGHT
                                                    / 2) / (tile_object.width -
                                                            WIDTH / 2)) * 180 /
                                              pi) - 180, True, self.tank_num))
                elif int(tile_object.name) in self.network.order[1:]:
                    self.tanks.insert(0, Tank(self, tile_object.x, tile_object.y,
                                              (atan((tile_object.height - HEIGHT
                                                      / 2) / (tile_object.width -
                                                              WIDTH / 2)) * 180 /
                                                pi) - 180, False, int(tile_object.name)))
                else:
                    self.tanks.insert(0, "None")
            if tile_object.name == "s_tree":
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            elif tile_object.name == "b_tree":
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            elif tile_object.name == "fence":
                 Obstacle(self, tile_object.x, tile_object.y,
                          tile_object.width, tile_object.height)
            elif tile_object.name == "cross":
                 Obstacle(self, tile_object.x, tile_object.y,
                          tile_object.width, tile_object.height)
            elif tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)

        print(str(self.tanks))
        self.player = self.tanks[self.tank_num]
        # while  "Wait" in self.network.recvieve():
        #     print("\n")

        self.network.send(self.player.pos_to_send)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        # print("Recieving info")
        self.network.data = self.network.recvieve()
        # print("Recv:", self.network.data)
        # print("Updating")
        self.all_sprites.update()
        self.network.send(self.player.pos_to_send)
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if not isinstance(sprite, Obstacle):
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:#
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
