from typing import List, Literal

from .constants import *

class Tile:
  def __init__(self, image, edges: list) -> None:
    self._image = image
    self._edges = edges

    self._connection_rules = {UP: [], RIGHT: [], DOWN: [], LEFT: []}

  @property
  def image(self):
    return self._image
  
  @property
  def edges(self) -> list:
    return self._edges
  
  @property
  def rules(self) -> dict:
    return self._connection_rules
  
  @property
  def up(self) -> List['Tile']:
    return self._connection_rules[UP]
  
  @property
  def left(self) -> List['Tile']:
    return self._connection_rules[LEFT]
  
  @property
  def down(self) -> List['Tile']:
    return self._connection_rules[DOWN]
  
  @property
  def right(self) -> List['Tile']:
    return self._connection_rules[RIGHT]
  
  def rotate(self, times: Literal[1, 2, 3]) -> 'Tile':
    new_image = self.image.rotate(-90 * times)
    new_edges = self.edges.copy()

    leng = len(self.edges)
    for i in range(leng):
      new_edges[i] = self.edges[(i - times + leng) % leng]

    return Tile(new_image, new_edges)
  
  def analyze_edges(self, tiles: List['Tile']) -> None:
    for tile in tiles:
      if tile.edges[DOWN] == self.edges[UP][::-1]:
        self.rules[UP].append(tile)

      if tile.edges[LEFT] == self.edges[RIGHT][::-1]:
        self.rules[RIGHT].append(tile)

      if tile.edges[UP] == self.edges[DOWN][::-1]:
        self.rules[DOWN].append(tile)

      if tile.edges[RIGHT] == self.edges[LEFT][::-1]:
        self.rules[LEFT].append(tile)