import json
import time

from game_rules import rules_factory
from cell import TwoDCoord, TwoDCell, is_in_bound_2d, is_same_coord, offset_2d_coord


class Grid:
    def __init__(self, rows, cols):
        self.start_coord = TwoDCoord(0, 0)
        self.end_coord = TwoDCoord(rows, cols)
        self.cells = [TwoDCell(TwoDCoord(row, col))
                      for row in range(rows) for col in range(cols)]

    def is_alive(self, coord: TwoDCoord) -> bool:

        if not is_in_bound_2d(self.start_coord, self.end_coord, coord):
            raise ValueError(
                "Coord {coord} is not in bound of start: {self.start_coord} and end: {self.end_coord}")

        target_cell = None
        for cell in self.cells:
            if is_same_coord(coord, cell):
                target_cell = cell
                break

        return target_cell.is_alive

    def alive_neighbors(self, coord: TwoDCell):
        offsets = [TwoDCoord(x=-1, y=-1), TwoDCoord(x=-1, y=0), TwoDCoord(x=-1, y=1), TwoDCoord(x=0, y=-1),
                   TwoDCoord(x=0, y=1), TwoDCoord(x=1, y=-1), TwoDCoord(x=1, y=0), TwoDCoord(x=1, y=1)]
        return sum(
            [self.is_alive(offset_2d_coord(coord, offset_coord))
             for offset_coord in offsets]
        )


class Game:
    def __init__(self, rows, cols, rules=None):
        self.grid = Grid(rows, cols)
        self.rules = rules if rules else []

    def update(self):
        new_grid = [[0 for _ in range(self.grid.cols)]
                    for _ in range(self.grid.rows)]
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                cell = self.grid.grid[row][col]
                alive_neighbors = self.grid.alive_neighbors(row, col)

                new_cell = None
                for rule in self.rules:
                    rule_callable = rules_factory[rule]
                    result = rule_callable(cell, alive_neighbors)
                    if result is not None:
                        new_cell = result
                        break

                new_grid[row][col] = new_cell if new_cell is not None else cell

        self.grid.grid = new_grid


def main():
    with open("game_config.json") as json_file:
        game_config = json.load(json_file)

    game = Game(game_config["rows"], game_config["cols"], game_config["rules"])

    game.grid.grid[0][2] = 1
    game.grid.grid[1][3] = 1
    game.grid.grid[2][1] = 1
    game.grid.grid[2][2] = 1
    game.grid.grid[2][3] = 1

    if game_config["output_type"] == "visualizer":
        from visualizer import visualize
        visualize(game, game_config["generations"], game_config["sleep_time"])

    elif game_config["output_type"] == "console":
        for generation in range(1, game_config["generations"] + 1):
            game.update()
            print(f"Generation {generation}:\n")
            print(game.grid)
            time.sleep(game_config["sleep_time"])


if __name__ == "__main__":
    main()
