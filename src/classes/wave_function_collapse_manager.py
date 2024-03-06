from typing import List
import numpy as np
import cv2
import random

from .tile import Tile
from .cell import Cell
from .constants import *


class WaveFunctionCollapseManager:
  def __init__(
      self,
      grid_size: int,
      width: int,
      height: int,
      show_possibilities_remain: bool = False,
      show_cells_border: bool = False
  ) -> None:
    self._grid_size = grid_size
    self._width = width
    self._height = height

    self._show_possibilities_remain = show_possibilities_remain
    self._show_cells_border = show_cells_border


    self._tile_images = []
    self._tiles: List[Tile] = []
    self._grid: List[List[Cell]] = []
    self._populate_grid()

  @property
  def grid_size(self) -> int:
    return self._grid_size

  @property
  def width(self) -> int:
    return self._width

  @property
  def height(self) -> int:
    return self._height

  @property
  def grid(self) -> List[List[Cell]]:
    return self._grid

  @property
  def tiles(self) -> List[Tile]:
    return self._tiles

  @property
  def tile_images(self) -> list:
    return self._tile_images

  def _populate_grid(self) -> None:
    if self._grid:
      print('Grid already populated')
      return

    self._grid = [[Cell(self._tiles) for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    for i in range(self.grid_size):
      for j in range(self.grid_size):
        if i > 0:
          self._grid[i][j].add_neighbor(UP, self._grid[i - 1][j])
        if j < self.grid_size - 1:
          self._grid[i][j].add_neighbor(LEFT, self._grid[i][j + 1])
        if i < self.grid_size - 1:
          self._grid[i][j].add_neighbor(DOWN, self._grid[i + 1][j])
        if j > 0:
          self._grid[i][j].add_neighbor(RIGHT, self._grid[i][j - 1])

  def add_tile_image(self, image) -> None:
    self._tile_images.append(image)

  def add_tile(self, tile: Tile) -> None:
    self._tiles.append(tile)

  def _collapse(self) -> None:
    cells = [cell for row in self.grid for cell in row if not cell.collapsed]

    if not cells:
      return

    min_entropy = min(len(cell.possible_tiles) for cell in cells)
    min_entropy_cells = [cell for cell in cells if len(cell.possible_tiles) == min_entropy]

    cell = random.choice(min_entropy_cells)
    cell.collapse()

  def _generate_rules(self) -> None:
    for tile in self.tiles:
      tile.analyze_edges(self.tiles)

  def _generate_frame(self) -> np.ndarray:
    self._collapse()

    frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

    w = self.width // self.grid_size
    h = self.height // self.grid_size

    for i in range(self.grid_size):
      for j in range(self.grid_size):
        cell = self.grid[i][j]
        if cell.collapsed:
          tile = cell.possible_tiles[0].image
          tile = cv2.cvtColor(np.array(tile), cv2.COLOR_RGB2BGR)  # Convertendo de RGB para BGR
          tile_resized = cv2.resize(tile, (w, h))
          frame[i*h:(i+1)*h, j*w:(j+1)*w] = tile_resized
        else:
          if self._show_cells_border:
            cv2.rectangle(frame, (j*w, i*h), ((j+1)*w, (i+1)*h), (255, 255, 255), 1)

          if self._show_possibilities_remain:
            font_scale = min(w, h) / 50  # Ajuste o valor 50 conforme necessário para o tamanho desejado
            font_thickness = max(1, int(font_scale))  # Garante que a espessura da fonte seja pelo menos 1
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = str(len(cell.possible_tiles))
            text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
            text_x = int(j*w + (w - text_size[0]) / 2)
            text_y = int(i*h + (h + text_size[1]) / 2)
            cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

    return frame

  def run(self) -> None:
    self._generate_rules()

    while True:
      frame = self._generate_frame()
      cv2.imshow('image', frame)
      cv2.waitKey(1)
