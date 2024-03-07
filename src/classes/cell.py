from typing import List, Dict, Literal
import random

from .constants import *
from .tile import Tile

class Cell:
  def __init__(self, tiles: list) -> None:
    self._collapsed: bool                     = False
    self._neighbors: Dict[int, List['Cell']]  = {}
    self._possible_tiles                      = tiles

  @property
  def collapsed(self) -> bool:
    return self._collapsed
  
  @collapsed.setter
  def collapsed(self, value: bool):
    self._collapsed = value

  @property
  def neighbors(self) -> Dict[int, List['Cell']]:
    return self._neighbors
  
  @property
  def possible_tiles(self) -> List[Tile]:
    return self._possible_tiles
  
  @possible_tiles.setter
  def possible_tiles(self, value: List[Tile]):
    self._possible_tiles = value

  def _check_validity(self, options: List[Tile], valids: List[Tile]) -> None:
    for i in range(len(options) - 1, -1, -1):
      element = options[i]
      if element not in valids:
        options.pop(i)

  def collapse(self) -> None:
    self.collapsed = True
    pick = random.choice(self.possible_tiles)
    self.possible_tiles = [pick]

    self.propagate_changes_to_neighbors()
    
  def add_neighbor(self, direction: Literal[0, 1, 2, 3, 4], neighbor: 'Cell') -> None:
    self._neighbors[direction] = neighbor

  def propagate_changes_to_neighbors(self) -> None:
    for direction, neighbor in self.neighbors.items():
      if neighbor.collapsed:
        continue

      options = [tile for tile in neighbor.possible_tiles]
      valid_options = set(valid for tile in self.possible_tiles for valid in tile._connection_rules[direction])

      self._check_validity(options, valid_options)

      if options != neighbor.possible_tiles and options != []:
        neighbor.possible_tiles = options
        try:
          neighbor.propagate_changes_to_neighbors()
        except RecursionError: pass