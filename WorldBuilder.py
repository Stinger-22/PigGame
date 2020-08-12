__author__ = 'XemyL'
# -*- coding: utf-8 -*-


class WorldBuilder:
    def __init__(self):
        tile_size = 32
        x, y = 0, 0
        self.tile_group = []
        self.connected_tiles = []
        # current_coords = [x, y]
        map1 = ['110',
                '010',
                '011']
        # По одному
        for row in map1:
            x = 0
            for tile in row:
                if tile == '0':
                    x += tile_size
                elif tile == '1':
                    add_tile = [x, y, x + tile_size, y + tile_size]
                    self.tile_group.append(add_tile)
                    x += tile_size
            y += tile_size
        self.to_connect_tiles(self.tile_group)

    # Малюю
    # .........

    # Об'єдную
    def to_connect_tiles(self, tiles):
        if tiles == []:
            return
        else:
            tile = self.tile_group[0]
            while len(tiles) > 1 and tile[2] == tiles[1][0] and tile[1] == tiles[1][1] and \
            tile[3] == tiles[1][3]:
                tile[2], tile[3] = tiles[1][2], tiles[1][3]
                tiles.pop(1)
            self.connected_tiles.append(tile)
            tiles.pop(0)
            self.to_connect_tiles(tiles)

world = WorldBuilder()
