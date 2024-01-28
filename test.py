import unittest

from game_of_life import Game, Grid
from game_rules import rules_factory


class Testbirth_rule(unittest.TestCase):
    birth_rule = rules_factory["BirthRule"]
    def test_birth_rule_with_dead_cell_and_three_live_neighbors(self):
        self.assertEqual(birth_rule(0, 3), 1, "Dead cell with 3 live neighbors should be born.")

    def test_birth_rule_with_dead_cell_and_two_live_neighbors(self):
        self.assertIsNone(birth_rule.apply(0, 2), "Dead cell with 2 live neighbors should remain dead.")

    def test_birth_rule_with_alive_cell(self):
        self.assertIsNone(birth_rule.apply(1, 3), "Alive cell should not be affected by birth_rule.")

    def test_birth_rule_with_dead_cell_and_four_live_neighbors(self):
        self.assertIsNone(birth_rule.apply(0, 4), "Dead cell with 4 live neighbors should remain dead.")


class Testlonely_death_rule(unittest.TestCase):
    lonely_death_rule = rules_factory["LonelyDeathRule"]
    def test_lonely_death_rule_with_alive_cell_and_one_live_neighbor(self):
        self.assertEqual(lonely_death_rule.apply(1, 1), 0, "Alive cell with 1 live neighbor should die.")

    def test_lonely_death_rule_with_alive_cell_and_zero_live_neighbors(self):
        self.assertEqual(lonely_death_rule.apply(1, 0), 0, "Alive cell with 0 live neighbors should die.")

    def test_lonely_death_rule_with_alive_cell_and_two_live_neighbors(self):
        self.assertIsNone(lonely_death_rule.apply(1, 2), "Alive cell with 2 live neighbors should not be affected by lonely_death_rule.")

    def test_lonely_death_rule_with_dead_cell(self):
        self.assertIsNone(lonely_death_rule.apply(0, 1), "Dead cell should not be affected by lonely_death_rule.")


class Teststay_alive_rule(unittest.TestCase):
    stay_alive_rule = rules_factory["stay_alive_rule"]
    def test_stay_alive_rule_with_alive_cell_and_two_live_neighbors(self):
        self.assertEqual(stay_alive_rule.apply(1, 2), 1, "Alive cell with 2 live neighbors should stay alive.")

    def test_stay_alive_rule_with_alive_cell_and_three_live_neighbors(self):
        self.assertEqual(stay_alive_rule.apply(1, 3), 1, "Alive cell with 3 live neighbors should stay alive.")

    def test_stay_alive_rule_with_alive_cell_and_one_live_neighbor(self):
        self.assertIsNone(stay_alive_rule.apply(1, 1),
                          "Alive cell with 1 live neighbor should not be affected by stay_alive_rule.")

    def test_stay_alive_rule_with_alive_cell_and_four_live_neighbors(self):
        self.assertIsNone(stay_alive_rule.apply(1, 4),
                          "Alive cell with 4 live neighbors should not be affected by stay_alive_rule.")

    def test_stay_alive_rule_with_dead_cell(self):
        self.assertIsNone(stay_alive_rule.apply(0, 2), "Dead cell should not be affected by stay_alive_rule.")


class Testoverpopulate_rule(unittest.TestCase):
    overpopulate_rule = rules_factory["overpopulate_rule"]
    def test_over_populate_rule_with_alive_cell_and_four_live_neighbors(self):
        self.assertEqual(overpopulate_rule.apply(1, 4), 0, "Alive cell with 4 live neighbors should die.")

    def test_over_populate_rule_with_alive_cell_and_five_live_neighbors(self):
        self.assertEqual(overpopulate_rule.apply(1, 5), 0, "Alive cell with 5 live neighbors should die.")

    def test_over_populate_rule_with_alive_cell_and_three_live_neighbors(self):
        self.assertIsNone(overpopulate_rule.apply(1, 3), "Alive cell with 3 live neighbors should not be affected by overpopulate_rule.")

    def test_over_populate_rule_with_dead_cell(self):
        self.assertIsNone(overpopulate_rule.apply(0, 4), "Dead cell should not be affected by overpopulate_rule.")


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(3, 3)  # Create a 3x3 grid for testing

    def test_initialization(self):
        self.assertEqual(len(self.grid.grid), 3, "Grid should have 3 rows.")
        self.assertEqual(len(self.grid.grid[0]), 3, "Grid should have 3 columns.")

    def test_is_cell_in_bounds(self):
        self.assertTrue(self.grid.is_cell_in_bounds(0, 0))
        self.assertTrue(self.grid.is_cell_in_bounds(2, 2))
        self.assertFalse(self.grid.is_cell_in_bounds(-1, 0))
        self.assertFalse(self.grid.is_cell_in_bounds(0, 3))
        self.assertFalse(self.grid.is_cell_in_bounds(3, 0))
        self.assertFalse(self.grid.is_cell_in_bounds(3, 3))

    def test_is_alive_with_dead_cell(self):
        self.assertEqual(self.grid.is_alive(1, 1), 0, "Cell should be dead initially.")

    def test_is_alive_with_alive_cell(self):
        self.grid.grid[1][1] = 1
        self.assertEqual(self.grid.is_alive(1, 1), 1, "Cell should be alive after being set.")

    def test_is_alive_with_out_of_bounds_cell(self):
        self.assertEqual(self.grid.is_alive(-1, 1), 0, "Out of bounds cell should be considered dead.")

    def test_alive_neighbors_for_center_cell(self):
        self.grid.grid[0][1] = 1
        self.grid.grid[1][0] = 1
        self.grid.grid[1][2] = 1
        self.assertEqual(self.grid.alive_neighbors(1, 1), 3, "Center cell should have 3 alive neighbors.")

    def test_alive_neighbors_for_corner_cell(self):
        self.grid.grid[0][1] = 1
        self.grid.grid[1][0] = 1
        self.assertEqual(self.grid.alive_neighbors(0, 0), 2, "Top-left corner cell should have 2 alive neighbors.")


class TestGame(unittest.TestCase):
    def setUp(self):
        self.rules = [birth_rule, lonely_death_rule, stay_alive_rule, overpopulate_rule]

    def test_grid_1(self):
        initial_state = [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
        expected_state = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ]

        game = Game(3, 3, self.rules)
        game.grid.grid = initial_state
        game.update()
        self.assertEqual(game.grid.grid, expected_state)

    def test_grid_2(self):
        initial_state = [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1]
        ]
        expected_state = [
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 1]
        ]

        game = Game(4, 4, self.rules)
        game.grid.grid = initial_state
        game.update()
        self.assertEqual(game.grid.grid, expected_state)

    def test_grid_3(self):
        initial_state = [
            [1, 1, 1],
            [1, 1, 1],
            [0, 1, 0]
        ]
        expected_state = [
            [1, 0, 1],
            [0, 0, 0],
            [1, 1, 1]
        ]

        game = Game(3, 3, self.rules)
        game.grid.grid = initial_state
        game.update()
        self.assertEqual(game.grid.grid, expected_state)