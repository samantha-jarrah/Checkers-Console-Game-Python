# Author: Samantha Jarrah
# GitHub username: samantha-jarrah
# Date: 3/10/23
# Description: Contains unit tests for CheckersGame. Tests init of game board, Player class,
# get_checker_details, get_which_players_turn, Game class, get_jump_just_occurred, and get_king_count.
# Tests jumping a checker piece, capturing a checker piece, and updating king count due to a capture.

import unittest
from CheckersGame import Checkers, Player


class CheckersTests(unittest.TestCase):

    def test_create_checkers_game(self):
        """Test init of game board"""
        game = Checkers()
        self.assertEqual(game._board, [
             ["__", "White", "__", "White", "__", "White", "__", "White"],
             ["White", "__", "White", "__", "White", "__", "White", "__"],
             ["__", "White", "__", "White", "__", "White", "__", "White"],
             ["__", "__", "__", "__", "__", "__", "__", "__"],
             ["__", "__", "__", "__", "__", "__", "__", "__"],
             ["Black", "__", "Black", "__", "Black", "__", "Black", "__"],
             ["__", "Black", "__", "Black", "__", "Black", "__", "Black"],
             ["Black", "__", "Black", "__", "Black", "__", "Black", "__"]])

    def test_create_player(self):
        """Test get_name and get_checker_color"""
        player1 = Player("Sami", "Black")
        player2 = Player("Cole", "White")
        self.assertEqual(player1.get_name(), "Sami")
        self.assertEqual(player2.get_name(), "Cole")
        self.assertEqual(player1.get_checker_color(), "Black")
        self.assertEqual(player2.get_checker_color(), "White")

    def test_get_checker_details(self):
        """Test get_checker_details"""
        game = Checkers()
        self.assertEqual(game.get_checker_details((7,0)), "Black")
        self.assertEqual(game.get_checker_details((7,1)), None)

    def test_which_players_turn(self):
        """Test getting which player is up to play"""
        game = Checkers()
        self.assertEqual(game.get_which_players_turn(), "Black")
        game.set_which_players_turn()
        self.assertEqual(game.get_which_players_turn(), "White")

    def test_jump_standard_checker(self):
        """
        Test of jumping as well as incrementing/resetting captured_pieces_count and total_captured_pieces
        """
        game = Checkers()
        game.create_player("Sam", "White")
        game.create_player("Faris", "Black")
        game.play_game("Faris", (5, 2), (4, 1))
        game.play_game("Sam", (2, 3), (3, 2))
        game.play_game("Faris", (4, 1), (2, 3))
        for player_obj in game._players:
            if game._players[player_obj][0] == "Faris":
                player_object = player_obj
        self.assertEqual(player_object.get_captured_pieces_count(), 0)
        self.assertEqual(player_object.get_total_captured_pieces_count(), 1)
        self.assertEqual(game.get_which_players_turn(), "White")

    def test_king(self):
        """
        Test to see if subsequent jumps can occur and if standard pieces are king-ed when they reach opponents side
        """

        game = Checkers()
        game.create_player("Sam", "White")
        game.create_player("Faris", "Black")
        game.play_game("Faris", (5, 2), (4, 1))
        game.play_game("Sam", (2, 3), (3, 2))
        game.play_game("Faris", (4, 1), (2, 3))
        game.play_game("Sam", (1, 2), (3, 4))
        game.play_game("Faris", (5, 4), (4, 5))
        game.play_game("Sam", (0, 1), (1, 2))
        game.play_game("Faris", (4, 5), (2, 3))
        self.assertNotEqual(game.get_checker_details((2, 3)), "Black_king")
        game.play_game("Faris", (2, 3), (0, 1))
        self.assertEqual(game.get_checker_details((0, 1)), "Black_king")

    def test_jump_just_occurred(self):
        """Test to see if jump_just_occurred updates to True when a jump happens"""

        game = Checkers()
        game.create_player("Sam", "White")
        game.create_player("Faris", "Black")
        game.play_game("Faris", (5, 2), (4, 1))
        game.play_game("Sam", (2, 3), (3, 2))
        self.assertFalse(game.get_jump_just_occurred())
        game.play_game("Faris", (4, 1), (2, 3))
        game.play_game("Sam", (1, 2), (3, 4))
        game.play_game("Faris", (5, 4), (4, 5))
        game.play_game("Sam", (0, 1), (1, 2))
        game.play_game("Faris", (4, 5), (2, 3))
        self.assertTrue(game.get_jump_just_occurred())

    def test_king_count_after_capture(self):
        """Check player's king count after their king has been captured"""

        game = Checkers()
        game.create_player("Sam", "White")
        game.create_player("Faris", "Black")
        game.play_game("Faris", (5, 2), (4, 1))
        game.play_game("Sam", (2, 3), (3, 2))
        game.play_game("Faris", (4, 1), (2, 3))
        game.play_game("Sam", (1, 2), (3, 4))
        game.play_game("Faris", (5, 4), (4, 5))
        game.play_game("Sam", (0, 1), (1, 2))
        game.play_game("Faris", (4, 5), (2, 3))
        game.play_game("Faris", (2, 3), (0, 1))
        game.play_game("Sam", (2, 7), (3, 6))
        game.play_game("Faris", (6, 3), (5, 2))
        game.play_game("Sam", (2, 5), (3, 4))
        game.play_game("Faris", (0, 1), (4, 5))
        game.play_game("Sam", (3, 6), (5, 4))
        for player_obj in game._players:
            if game._players[player_obj][0] == "Faris":
                player_object = player_obj
        self.assertNotEqual(player_object.get_king_count(), 1)


if __name__ == '__main__':
    unittest.main()
