from PIL import Image

from classes.wave_function_collapse_manager import WaveFunctionCollapseManager
from classes.tile import Tile

if __name__ == '__main__':
  manager = WaveFunctionCollapseManager(
    grid_size=20,
    width=800,
    height=800
  )

  path = "./src/tiles/circuit-board"
  for i in range(13):
    manager.add_tile_image(Image.open(f'{path}/{i}.png'))

  manager.add_tile(Tile(manager.tile_images[0], ["AAA", "AAA", "AAA", "AAA"]))
  manager.add_tile(Tile(manager.tile_images[1], ["BBB", "BBB", "BBB", "BBB"]))
  manager.add_tile(Tile(manager.tile_images[2], ["BBB", "BCB", "BBB", "BBB"]))
  manager.add_tile(Tile(manager.tile_images[3], ["BBB", "BDB", "BBB", "BDB"]))
  manager.add_tile(Tile(manager.tile_images[4], ["ABB", "BCB", "BBA", "AAA"]))
  manager.add_tile(Tile(manager.tile_images[5], ["ABB", "BBB", "BBB", "BBA"]))
  manager.add_tile(Tile(manager.tile_images[6], ["BBB", "BCB", "BBB", "BCB"]))
  manager.add_tile(Tile(manager.tile_images[7], ["BDB", "BCB", "BDB", "BCB"]))
  manager.add_tile(Tile(manager.tile_images[8], ["BDB", "BBB", "BCB", "BBB"]))
  manager.add_tile(Tile(manager.tile_images[9], ["BCB", "BCB", "BBB", "BCB"]))
  manager.add_tile(Tile(manager.tile_images[10], ["BCB", "BCB", "BCB", "BCB"]))
  manager.add_tile(Tile(manager.tile_images[11], ["BCB", "BCB", "BBB", "BBB"]))
  manager.add_tile(Tile(manager.tile_images[12], ["BBB", "BCB", "BBB", "BCB"]))

  for i in range(2, len(manager.tiles), 1):
    for rotation in range(1, 4, 1):
      manager.tiles.append(manager.tiles[i].rotate(rotation))

  manager.run()