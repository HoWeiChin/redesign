from dataclasses import dataclass
from numpy import subtract, add


@dataclass(frozen=True)
class TwoDCoord:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"


@dataclass
class TwoDCell:
    """a cell with 2 coordinates for a grid"""
    coord: TwoDCoord
    is_alive: bool = False


def is_same_coord(coord: TwoDCoord, cell: TwoDCell) -> bool:
    """Check if cell has the same coordinate as coord"""
    return sum(subtract(cell.coord, coord)) == 0


def is_in_bound_2d(start_coord: TwoDCoord, end_coord: TwoDCoord, coord: TwoDCoord) -> bool:
    return sum(subtract(coord, start_coord)) >= 0 and sum(subtract(coord, end_coord)) >= 0


def offset_2d_coord(coord_to_offset: TwoDCoord, offset: TwoDCoord) -> TwoDCoord:
    result_coord = add(coord_to_offset, offset)
    return TwoDCoord(x=result_coord[0], y=result_coord[1])
