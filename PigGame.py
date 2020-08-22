__author__ = 'XemyL'
# -*- coding: utf-8 -*-

# Surface (width, height) - drawing on it
# Rect (top, left, width, height) - save coords and size
# pygame.get_rect(Surface, corner or side=(x, y)) - return Rect object

# Surface.get_rect - return Rect object
# Surface.get_size - return tuple(width, height)
# Surface.blit(surface, coords, (area=)) - on this.blit(draw this, (x, y), area=rect)

# event: ACTIVEEVENT: gain, state
# Event(32768-ActiveEvent {'gain': 1, 'state': 2, 'window': None}
# what is "gain" and "state"

# pygame.display.setmode(size=width, height) - not any size

import pygame
from sys import exit
from os import listdir
from json import load

pygame.init()
# pygame.display.init() -2mb ram


class MainGame:
    def __init__(self):
        # Create useful variables
        self.playing = False
        self.event_queue = []
        self.window = pygame.display
        self.window_width = self.window.Info().current_w
        self.window_height = self.window.Info().current_h

        self.clock = pygame.time.Clock()
        self.screenSurface = self.window.set_mode\
        (size=(self.window_width, self.window_height), flags=pygame.FULLSCREEN, depth=32)
        self.window.set_caption('Pig Game')

        # Load textures
        self.textures = {}  # {name: texture (surface)}
        self.load_textures()

        self.button_startRect = self.textures['start_button'].get_rect \
        (topleft=(((self.window_width - self.textures['start_button'].get_width()) / 2),
                  ((self.window_height - self.textures['start_button'].get_height()) / 2)))

        self.create_menu()

    def load_textures(self):
        for texture in listdir(path='sprites'):
            # Pycharm can't recognize f-strings -> highlights this like error
            self.textures[texture[:len(texture) - 4]] = pygame.image.load(f'sprites/{texture}').convert_alpha()

    def create_menu(self):
        self.screenSurface.blit(self.textures['bg'], (0, 0))
        self.screenSurface.blit(self.textures['start_button'], self.button_startRect)

    def mainloop(self):
        while 1:
            self.clock.tick(60) # N iterations per second
            if self.playing == True:
                self.event_queue = pygame.event.get()
                self.press_buttons()
                self.playable_character.move()
                self.redraw_screen(self.playable_character)
                self.window.update(self.playable_character.Rect_on_screen)
            if self.playing == False:
                self.event_queue = pygame.event.get()
                self.press_buttons()
                self.window.update(self.button_startRect)

    # Button binds
    def press_buttons(self):
        for click in self.event_queue:
            if click.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif click.type == pygame.KEYDOWN:
                if click.key == pygame.K_F4 and click.mod == pygame.KMOD_LALT:
                    pygame.quit()
                    exit()

            # Alt+Tab redrawing
            if self.playing == True and click.type == pygame.ACTIVEEVENT:
                self.screenSurface.blit(self.textures['bg'], (0, 0))
                level.map_drawing()
                pig.move()
                self.screenSurface.blit(self.textures['pig'], (pig.Rect[0], pig.Rect[1]))
                self.window.update()
            elif self.playing == False and click.type == pygame.ACTIVEEVENT:
                self.create_menu()
                self.window.update()

            # Button "Start"
            if self.playing == False and click.type == pygame.MOUSEMOTION:
                if self.button_startRect[0] + self.button_startRect[2] > click.pos[0] > self.button_startRect[0] and \
                    self.button_startRect[1] + self.button_startRect[3] > click.pos[1] > self.button_startRect[1]:
                    self.screenSurface.blit(self.textures['start_button_hovered'], self.button_startRect)
                else:
                    self.screenSurface.blit(self.textures['start_button'], self.button_startRect)
            if self.playing == False and click.type == pygame.MOUSEBUTTONDOWN and click.button == 1:
                if self.button_startRect[0] + self.button_startRect[2] > click.pos[0] > self.button_startRect[0] and \
                    self.button_startRect[1] + self.button_startRect[3] > click.pos[1] > self.button_startRect[1]:
                        self.start()
                        self.playing = True

            # Button "Quit"

    def start(self):
        # Find center of screen with playable character in it
        self.screenRect = pygame.Rect(level.start_pos[0] - (self.window_width / 2),
                                      level.start_pos[1] - (self.window_height / 2), self.window_width, self.window_height)
        # Choosen character
        self.playable_character = pig

    def redraw_screen(self, character): # character - object of class PlayableCharacter
        self.screen_scroll(character)
        self.screenSurface.blit(self.textures['bg'], (0, 0))  # draw bg on screenSurface
        self.screenSurface.blit(self.textures['bg'], (character.Rect_on_screen[0], character.Rect_on_screen[1]), area=character.Rect_on_screen)  # removing old playable character
        pig.Rect.move_ip(pig.speed[0], pig.speed[1])  # new playable character coords
        self.screenSurface.blit(self.textures['pig'], character.Rect_on_screen)  # draw playable character on screenSurface
        self.screenSurface.blit(level.levelSurface, (0, 0), area=self.screenRect)  # draw part of levelSurface on screenSurface

    def screen_scroll(self, character): # Move screen
        if pig.speed[0] > 0 and character.Rect_on_screen[0] + character.Rect_on_screen[2] > (self.window_width - 300):
            self.screenRect[0] += pig.speed[0]
        elif pig.speed[0] < 0 and character.Rect_on_screen[0] < 300:
            self.screenRect[0] += pig.speed[0]
        if pig.speed[1] < 0 and character.Rect_on_screen[1] < 200:
            self.screenRect[1] += pig.speed[1]
        elif self.screenRect[1] + self.screenRect[3] + pig.speed[1] < level.levelSurface_height:
            if pig.speed[1] > 0 and character.Rect_on_screen[1] > (self.window_height - 200):
                self.screenRect[1] += pig.speed[1]


class Sprite:
    def __init__(self, texture, gravity, position):
        self.Rect = pygame.Surface.get_rect(texture, bottomleft=position)
        self.coords = None # [top, left, bottom, right]
        self.speed = [0, 0] # speed = [x, y]
        self.gravity = gravity
        self.on_ground = None

    def collision_check(self, tiles):
        for tile in tiles: # tile[top, left, bottom, right]
            # Check collision only if any corner of tile may be within the screen
            if game.screenRect[0] < tile[0] < game.screenRect[0] + game.screenRect[2] or \
               game.screenRect[0] < tile[2] < game.screenRect[0] + game.screenRect[2] or \
               game.screenRect[1] < tile[1] < game.screenRect[1] + game.screenRect[3] or \
               game.screenRect[1] < tile[3] < game.screenRect[1] + game.screenRect[3]:
                    self.collision_line_x(tile)
                    self.collision_line_y(tile)


    def collision_line_y(self, tile):
        if tile[1] < self.coords[1] + self.speed[1] < tile[3]:  # within tile y top
            if self.coords[0] + self.speed[0] < tile[2] and self.coords[2] + self.speed[0] > tile[0]:
                self.speed[1] = 0
                self.Rect.move_ip(0, tile[3] - self.coords[1])
        if tile[1] < self.coords[3] + self.speed[1] < tile[3]:  # within tile y bottom
            if self.coords[0] + self.speed[0] < tile[2] and self.coords[2] + self.speed[0] > tile[0]:
                self.on_ground = True
                self.speed[1] = 0
                self.Rect.move_ip(0, tile[1] - self.coords[3])
            if self.speed[1] != 0:
                self.on_ground = False

    def collision_line_x(self, tile):
        if tile[0] < self.coords[2] + self.speed[0] < tile[2] or tile[0] < self.coords[0] + self.speed[0] <  tile[2]:  # within tile x
            if tile[1] < self.coords[1] < tile[3] or tile[1] < self.coords[3] < tile[3] or \
            (self.coords[1] <= tile[1] and self.coords[3] >= tile[3]):
                self.speed[0] = 0


class PlayableCharacter(Sprite):
    def __init__(self, texture, gravity, start_pos, max_speed):
        super().__init__(texture, gravity, start_pos)
        self.max_speed = max_speed
        self.Rect_on_screen = None

    def move(self):
        self.coords = [self.Rect[0], self.Rect[1], self.Rect[0] + self.Rect[2], self.Rect[1] + self.Rect[3]]
        # Playable character coords on screen (within window_width and window_height)
        self.Rect_on_screen = pygame.Rect(self.Rect[0] - game.screenRect[0], self.Rect[1] - game.screenRect[1],
                                          self.Rect[2], self.Rect[3])
        keys = pygame.key.get_pressed()
        # Increase speed
        if keys[pygame.K_RIGHT] and self.speed[0] < self.max_speed:
            self.speed[0] += 1
        if keys[pygame.K_LEFT] and self.speed[0] > -self.max_speed:
            self.speed[0] -= 1
        if keys[pygame.K_SPACE] and self.on_ground == True:
            self.on_ground = False
            self.speed[1] = -15
        # Decrease speed
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            if self.speed[0] > 0:
                self.speed[0] -= 1
            if self.speed[0] < 0:
                self.speed[0] += 1
        if not keys[pygame.K_SPACE] or self.on_ground == False:
            if self.speed[1] + self.gravity < 32: # 32 - Falling speed can't be more than 32
                self.speed[1] += self.gravity

        self.collision_check(level.mergedtiles_group)

        # Game Over if character fell out
        if self.Rect[1] + self.Rect[3] > level.levelSurface_height + (game.window_height / 2):
            pygame.quit()
            exit()


class MapBuilder:
    def __init__(self):
        self.tile_size = 32  # tile = square
        self.x, self.y = 0, 0
        self.start_pos = []
        self.map_loading()

    def map_loading(self):
        self.tiles_group = []
        self.mergedtiles_group = []
        self.add_tile = []

        # Load level form json file
        with open('level.json', 'r') as level_json:
            level = load(level_json)
            level = level['level']

        for row in level:
            self.x = 0
            for tile in row:
                if tile == '0':
                    self.x += self.tile_size
                elif tile == '1':
                    self.add_tile = [self.x, self.y, self.x + self.tile_size, self.y + self.tile_size]
                    self.tiles_group.append(self.add_tile)
                    self.x += self.tile_size
                elif tile == 'S':  # S - spawntile pig
                    self.start_pos = [self.x, self.y]
                    self.add_tile = [self.x, self.y, self.x + self.tile_size, self.y + self.tile_size]
                    self.tiles_group.append(self.add_tile)
                    self.x += self.tile_size
            self.y += self.tile_size

        #  Set levelSurface
        biggest = ''
        for row in level:
            if len(row) > len(biggest):
                biggest = row
        self.levelSurface_width = len(biggest) * 32
        self.levelSurface_height = len(level) * 32
        self.levelSurface = pygame.Surface((self.levelSurface_width, self.levelSurface_height))  # +15mb ram (depends by level size)
        self.levelSurface.set_colorkey([0, 0, 0])

        self.map_drawing()
        self.to_merge_tiles_row = []
        self.tiles_group_merging = self.tiles_group[:]
        self.merge_tiles_row(self.tiles_group_merging)

    def map_drawing(self):
        for tile in self.tiles_group:
            self.tileRect = pygame.Surface.get_rect(game.textures['tile'], topleft=(tile[0], tile[1]))
            self.levelSurface.blit(game.textures['tile'], self.tileRect)

    def merge_tiles_row(self, tiles):
        if tiles == []:
            self.to_merge_tiles_row.sort(key=lambda tile: tile[0])
            self.merge_tiles_column(self.to_merge_tiles_row)
        else:
            tile = tiles[0]
            while len(tiles) > 1 and tile[2] == tiles[1][0] and tile[1] == tiles[1][1] and \
            tile[3] == tiles[1][3]:
                tile[2], tile[3] = tiles[1][2], tiles[1][3]
                tiles.pop(1)
            self.to_merge_tiles_row.append(tile)
            tiles.pop(0)
            self.merge_tiles_row(tiles)

    def merge_tiles_column(self, tiles):
        if tiles == []:
            return
        else:
            tile = tiles[0]
            while len(tiles) > 1 and tile[0] == tiles[1][0] and tile[2] == tiles[1][2] and \
            tile[3] == tiles[1][1]:
                tile[2], tile[3] = tiles[1][2], tiles[1][3]
                tiles.pop(1)
            self.mergedtiles_group.append(tile)
            tiles.pop(0)
            self.merge_tiles_column(tiles)

# Create window
game = MainGame()
# Load level
level = MapBuilder()
# Load playable characters
pig = PlayableCharacter(game.textures['pig'], 1, level.start_pos, 10)

# Start
game.mainloop()
