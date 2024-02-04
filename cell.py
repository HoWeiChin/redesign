from dataclasses import dataclass
from numpy import subtract


@dataclass(frozen=True)
class TwoDCoord:
    x: int
    y: int


@dataclass
class TwoDCell:
    """a cell with 2 coordinates for a grid"""
    coord: TwoDCoord
    is_alive: bool = False


def check_in_bound_2d(start_coord: TwoDCoord, end_coord: TwoDCoord, cell: TwoDCell):
    return sum(subtract(cell.coord, start_coord)) > 0 and sum(subtract(cell.coord, end_coord))
