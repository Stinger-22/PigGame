__author__ = 'XemyL'
# -*- coding: utf-8 -*-


class WorldBuilder:
    def __init__(self):
        tile_size = 32
        x, y = 0, 0
        self.tiles_group = []
        self.mergedtiles_group = []
        map1 = ['0001',
                '0001',
                '11010011',
                '11010011',
                '11111111']
        # По одному
        for row in map1:
            x = 0
            for tile in row:
                if tile == '0':
                    x += tile_size
                elif tile == '1':
                    add_tile = [x, y, x + tile_size, y + tile_size]
                    self.tiles_group.append(add_tile)
                    x += tile_size
            y += tile_size
        self.to_merge_tiles = []
        self.merge_tiles_row(self.tiles_group)

    # Малюю
    # .........

    # Об'єдную
    def merge_tiles_row(self, tiles):
        if tiles == []:
            self.to_merge_tiles.sort(key=lambda tile: tile[0])
            self.merge_tiles_column(self.to_merge_tiles)
        else:
            tile = tiles[0]
            while len(tiles) > 1 and tile[2] == tiles[1][0] and tile[1] == tiles[1][1] and \
            tile[3] == tiles[1][3]:
                tile[2], tile[3] = tiles[1][2], tiles[1][3]
                tiles.pop(1)
            self.to_merge_tiles.append(tile)
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

world = WorldBuilder()
