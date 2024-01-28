import json
import time

from game_rules import rules_factory

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0] * self.cols for _ in range(self.rows)]

    def is_cell_in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_alive(self, row, col):
        return self.grid[row][col] == 1 if self.is_cell_in_bounds(row, col) else 0

    def alive_neighbors(self, row, col):
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return sum(
            [self.is_alive(row + off_y, col + off_x) for off_y, off_x in offsets]
        )

    def __str__(self):
        rows = ["  ".join(map(str, row)) for row in self.grid]
        return "\n".join(rows)


class Game:
    def __init__(self, rows, cols, rules=None):
        self.grid = Grid(rows, cols)
        self.rules = rules if rules else []

    def update(self):
        new_grid = [[0 for _ in range(self.grid.cols)] for _ in range(self.grid.rows)]
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