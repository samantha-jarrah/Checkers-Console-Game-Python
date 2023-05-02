# Author: Samantha Jarrah
# GitHub username: samantha-jarrah
# Date: 3/10/23
# Description: Contains a Player Class, Checkers Class, and 3 exceptions that all work together to create a console
# version of checkers for two players.


class OutofTurn(Exception):
    """Raised if the wrong player tries to play"""
    pass


class InvalidPlayer(Exception):
    """Raised if the person attempting to make a move is not a player in the game"""
    pass


class InvalidSquare(Exception):
    """Raised if a player tries moving to a square that is invalid"""
    pass


class Player:
    """
    Represents a player that takes a name, and checker color to create player object
    Keeps track of the number of kings, triple kings, and captured opponent pieces
    Has get methods for each of these attributes and has set methods to update the king count, triple king count,
    and captured piece count.
    """

    def __init__(self, player_name, checker_color):
        self._player_name = player_name
        self._checker_color = checker_color
        self._kings = 0     # players begin with 0 kings
        self._triple_kings = 0  # players begin with 0 triple kings
        self._captured_pieces = 0   # players begin with 0 captured opponent pieces
        self._total_captured_pieces = 0

    def get_name(self):
        """Returns player name"""
        return self._player_name

    def get_checker_color(self):
        """Returns player checker color"""
        return self._checker_color

    def get_king_count(self):
        """Returns the number of kings the player currently has"""

        return self._kings

    def set_king_count(self, num_king):
        """
        Adjusts the king count
        num_king should be positive for gaining a king and negative for losing a king
        """

        self._kings += num_king

    def get_triple_king_count(self):
        """Returns the number of triple kings the player currently has"""

        return self._triple_kings

    def set_triple_king_count(self, num_triple_king):
        """
        Adjusts the triple king count
        num_triple_king should be positive for gaining a king and negative for losing a king
        """

        self._triple_kings += num_triple_king

    def get_captured_pieces_count(self):
        """Returns the number of captured opponent pieces the player got in that move"""

        return self._captured_pieces

    def set_captured_pieces_count(self, inc_reset):
        """If inc_reset == "increment", then increment captured_pieces by 1
        If inc_reset == "reset", then set captured_pieces to 0
        """

        if inc_reset == "increment":
            self._captured_pieces += 1
        elif inc_reset == "reset":
            self._captured_pieces = 0

    def get_total_captured_pieces_count(self):
        """Returns the total number of captured opponent pieces the player currently has"""

        return self._total_captured_pieces

    def set_total_captured_pieces(self):
        """Increments the total number of opponent pieces captured"""

        self._total_captured_pieces += 1


class Checkers:
    """
    Represents a checkers game that is initialized with a game board, black as the first player, and an empty dictionary
    to contain the player information.

    Creates players using the Player class and adds them to the player dictionary

    Has methods to return and print the game board, get details about the checker piece at a specific location, set/get
    which player's turn it is, update the board, capture a piece on the board, and get the winner(if there is one)
    """

    def __init__(self):
        # W=white, B=Black, empty=no checker piece in that square
        self._board = [
             ["__", "White", "__", "White", "__", "White", "__", "White"],
             ["White", "__", "White", "__", "White", "__", "White", "__"],
             ["__", "White", "__", "White", "__", "White", "__", "White"],
             ["__", "__", "__", "__", "__", "__", "__", "__"],
             ["__", "__", "__", "__", "__", "__", "__", "__"],
             ["Black", "__", "Black", "__", "Black", "__", "Black", "__"],
             ["__", "Black", "__", "Black", "__", "Black", "__", "Black"],
             ["Black", "__", "Black", "__", "Black", "__", "Black", "__"]]
        self._which_players_turn = "Black"      # Black plays first every game
        self._players = {}  # key=player object, value=list with player name and checker color
        self._jump_just_occurred = False        # keeps track of whether a jump just occurred to allow subsequent capture jumps by player that is not up

    def create_player(self, player_name, piece_color):
        """
        Creates and returns a Player object. Adds player object as key in player dictionary, player_name and piece_color
        are the values.
        """

        player = Player(player_name, piece_color)
        self._players[player] = [player_name, piece_color]
        return player

    def get_jump_just_occurred(self):
        """Returns the value in jump_just_occurred. Will be True or False"""

        return self._jump_just_occurred

    def set_jump_just_occurred(self, true_false):
        """Sets jump_just_occurred to either True or False"""

        self._jump_just_occurred = true_false

    def get_checker_details(self, square_location):
        """
        Returns information about what checker is in the passed square_location
        square_location is a tuple
        """

        row, column = square_location
        if row > 7 or row < 0:
            raise InvalidSquare
        elif column > 7 or column < 0:
            raise InvalidSquare

        location = self._board[row][column]

        if location == "__":
            return None
        else:
            return location

    def print_board(self):
        """Prints the current board"""

        print(self._board)

    def pretty_print_board(self):
        """Prints board list by list for more of grid visual"""

        for line in self._board:
            print(f"{line} \n")

    def set_which_players_turn(self):
        """Update which player is up to play"""

        if self._which_players_turn == "Black":
            self._which_players_turn = "White"
        else:
            self._which_players_turn = "Black"

    def get_which_players_turn(self):
        """Returns which player is up to play"""

        return self._which_players_turn

    def update_board(self, starting_square_location, destination_square_location, checker_piece_type):
        """Places the checker_piece_type at the destination_square_location"""

        end_row, end_column = destination_square_location
        start_row, start_column = starting_square_location

        self._board[end_row][end_column] = checker_piece_type
        self._board[start_row][start_column] = "__"

    def jump_procedure(self, starting_square_location, destination_square_location, current_checker, player_object):
        """
        Various method calls when a jump has occurred
        starting_square_location and destination_square_location must be tuples (row, column)
        Updates board, captures piece(s), sets jump_just_occurred to True, switches the player's turn
        """

        self.update_board(starting_square_location, destination_square_location, current_checker)
        self.capture_piece(starting_square_location, destination_square_location, player_object)
        self.set_jump_just_occurred(True)
        self.set_which_players_turn()

    def non_jump_procedure(self, starting_square_location, destination_square_location, current_checker):
        """
        Various method calls when no jump is being made
        starting_square_location and destination_square_location must be tuples (row, column)
        Updates board, sets jump_just_occurred to False, switches the player's turn
        """

        self.update_board(starting_square_location, destination_square_location, current_checker)
        self.set_jump_just_occurred(False)
        self.set_which_players_turn()

    def capture_piece(self, starting_square_location, destination_square_location, player_object):
        """
        Updates player_object's captured pieces count, and total captured pieces count.
        If opponent had king or triple king captured, those counts are updated.
        Clears the space of any captured piece
        """

        end_row, end_column = destination_square_location
        start_row, start_column = starting_square_location

        white = ["White", "White_king", "White_Triple_King"]
        black = ["Black", "Black_king", "Black_Triple_King"]

        if player_object.get_checker_color() == "White":  # White checker is moving
            # check each square in between start and finish in diagonal for opponent piece capture
            if start_column - end_column < 0:   # moved right
                if start_row - end_row < 0:     # moved down
                    num = 1
                    while num < end_column - start_column:
                        current_square = (start_row + num, start_column + num)
                        if self.get_checker_details(current_square) in black:  # we found an opponent piece
                            if self.get_checker_details(current_square) == "Black_king":   # capture a king
                                # reduce king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "Black":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_king_count(-1)
                            elif self.get_checker_details(current_square) == "Black_Triple_King":  # capture a triple king
                                # reduce triple king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "Black":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_triple_king_count(-1)
                            self._board[start_row + num][start_column + num] = "__"  # clear the captured piece space
                            player_object.set_captured_pieces_count("increment")
                            player_object.set_total_captured_pieces()
                        num += 1
                else:   # moved up
                    num = 1
                    while num < end_column - start_column:
                        current_square = (start_row - num, start_column + num)
                        if self.get_checker_details(current_square) in black:
                            if self.get_checker_details(current_square) == "Black_king":   # capture a king
                                # reduce king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "Black":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_king_count(-1)
                            elif self.get_checker_details(current_square) == "Black_Triple_King":  # capture a triple king
                                # reduce triple king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "Black":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_triple_king_count(-1)
                            self._board[start_row - num][start_column + num] = "__"  # clear the captured piece space
                            player_object.set_captured_pieces_count("increment")
                            player_object.set_total_captured_pieces()
                        num += 1
            else:   # moved left
                if start_row - end_row < 0:  # moved down
                    num = 1
                    while num < start_column - end_column:
                        current_square = (start_row + num, start_column - num)
                        if self.get_checker_details(current_square) in black:
                            if self.get_checker_details(current_square) == "Black_king":   # capture a king
                                # reduce king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "Black":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_king_count(-1)
                            elif self.get_checker_details(current_square) == "Black_Triple_King":  # capture a triple king
                                # reduce triple king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "Black":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_triple_king_count(-1)
                            self._board[start_row + num][start_column - num] = "__"  # clear the captured piece space
                            player_object.set_captured_pieces_count("increment")
                            player_object.set_total_captured_pieces()
                        num += 1
                else:       # moved up
                    num = 1
                    while num < start_column - end_column:
                        current_square = (start_row - num, start_column - num)
                        if self.get_checker_details(current_square) in black:
                            if self.get_checker_details(current_square) == "Black_king":   # capture a king
                                # reduce king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "Black":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_king_count(-1)
                            elif self.get_checker_details(current_square) == "Black_Triple_King":  # capture a triple king
                                # reduce triple king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "Black":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_triple_king_count(-1)
                            self._board[start_row - num][start_column - num] = "__"  # clear the captured piece space
                            player_object.set_captured_pieces_count("increment")
                            player_object.set_total_captured_pieces()
                        num += 1

        else:       # Black checker is moving
            # check each square in between start and finish in diagonal for opponent piece
            if start_column - end_column < 0:  # moved right
                if start_row - end_row < 0:  # moved down
                    num = 1
                    while num < end_column - start_column:
                        current_square = (start_row + num, start_column + num)
                        if self.get_checker_details(current_square) in white:
                            if self.get_checker_details(current_square) == "White_king":   # capture a king
                                # reduce king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "White":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_king_count(-1)
                            elif self.get_checker_details(current_square) == "White_Triple_King":  # capture a triple king
                                # reduce triple king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "White":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_triple_king_count(-1)
                            self._board[start_row + num][start_column + num] = "__"  # clear the captured piece space
                            player_object.set_captured_pieces_count("increment")
                            player_object.set_total_captured_pieces()
                        num += 1
                else:  # moved up
                    num = 1
                    while num < end_column - start_column:
                        current_square = (start_row - num, start_column + num)
                        if self.get_checker_details(current_square) in white:
                            if self.get_checker_details(current_square) == "White_king":   # capture a king
                                # reduce king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "White":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_king_count(-1)
                            elif self.get_checker_details(current_square) == "White_Triple_King":  # capture a triple king
                                # reduce triple king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "White":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_triple_king_count(-1)
                            self._board[start_row - num][start_column + num] = "__"  # clear the captured piece space
                            player_object.set_captured_pieces_count("increment")
                            player_object.set_total_captured_pieces()
                        num += 1
            else:  # moved left
                if start_row - end_row < 0:  # moved down
                    num = 1
                    while num < start_column - end_column:
                        current_square = (start_row + num, start_column - num)
                        if self.get_checker_details(current_square) in white:
                            if self.get_checker_details(current_square) == "White_king":   # capture a king
                                # reduce king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "White":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_king_count(-1)
                            elif self.get_checker_details(current_square) == "White_Triple_King":  # capture a triple king
                                # reduce triple king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "White":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_triple_king_count(-1)
                            self._board[start_row + num][start_column - num] = "__"  # clear the captured piece space
                            player_object.set_captured_pieces_count("increment")
                            player_object.set_total_captured_pieces()
                        num += 1
                else:  # moved up
                    num = 1
                    while num < start_column - end_column:
                        current_square = (start_row - num, start_column - num)
                        if self.get_checker_details(current_square) in white:
                            if self.get_checker_details(current_square) == "White_king":   # capture a king
                                # reduce king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "White":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_king_count(-1)
                            elif self.get_checker_details(current_square) == "White_Triple_King":  # capture a triple king
                                # reduce triple king count of opponent
                                for player_obj in self._players:
                                    if self._players[player_obj][1] == "White":
                                        opposing_player_object = player_obj
                                opposing_player_object.set_triple_king_count(-1)
                            self._board[start_row - num][start_column - num] = "__"  # clear the captured piece space
                            player_object.set_captured_pieces_count("increment")
                            player_object.set_total_captured_pieces()
                        num += 1

    def is_player_valid(self, player_name):
        """Returns True or False for if a player is in the game"""

        player_values = self._players.values()
        for list_of_values in player_values:
            if player_name in list_of_values:
                return True
        return False

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """
        starting_square_location and destination_square_locations are tuples in form (row, column)
        Checks is player_name matches any current players in self._player dictionary, raises InvalidPlayer if no match is found
        Checks if correct player is attempting a move but will override if jump just occurred and player is attempting subsequent jump
        Checks if starting_square_location contains a piece belonging to player
        Moves piece and updates board. If piece was king-ed or triple king-ed this is reflected in the updated board
        """

        if not self.is_player_valid(player_name):       # name does not exist as a player name
            print("You are not a player in this game.")
            raise InvalidPlayer

        for player_obj in self._players:
            if self._players[player_obj][0] == player_name:
                player_object = player_obj

        start_row, start_column = starting_square_location
        end_row, end_column = destination_square_location

        checker_color = player_object.get_checker_color()

        if checker_color != self.get_which_players_turn():  # If the wrong person is trying to take a turn
            if self.get_jump_just_occurred() is True and abs(start_row - end_row) > 1:  # jump just occurred and player is attempting a subsequent jump
                self.set_which_players_turn()
            else:
                print("It is not your turn.")
                raise OutofTurn

        current_checker = self.get_checker_details(starting_square_location)

        if checker_color == "Black":   # if the player with black checkers is playing
            options = ["Black", "Black_king", "Black_Triple_King"]
            if current_checker not in options:  # This square is either empty or does not have a checker belonging to this player
                print("You don't have a checker in this square.")
                raise InvalidSquare
        else:       # if the player with white checkers is playing
            options = ["White", "White_king", "White_Triple_King"]
            if current_checker not in options:   # This square is either empty or does  not hav ea checker belonging to this player
                print("You don't have a checker in this square.")
                raise InvalidSquare

        regular_checker = ["White", "Black"]
        king_checker = ["White_king", "Black_king"]
        triple_king_checker = ["White_Triple_King", "Black_Triple_King"]

        # Movement for basic checker piece, not king or triple king
        if current_checker in regular_checker:
            # no jump taking place
            if end_column == start_column + 1 or end_column == start_column - 1:
                if end_row == 0 or end_row == 7:    # King the piece!
                    player_object.set_king_count(1)
                    if current_checker == regular_checker[0]:       # white checker
                        current_checker = "White_king"
                        self.non_jump_procedure(starting_square_location, destination_square_location, current_checker)
                    else:       # black checker
                        current_checker = "Black_king"
                        self.non_jump_procedure(starting_square_location, destination_square_location, current_checker)
                else:       # piece was not king-ed
                    self.non_jump_procedure(starting_square_location, destination_square_location, current_checker)
            # jump takes place
            else:
                if end_row == 0 or end_row == 7:    # King the piece!
                    player_object.set_king_count(1)
                    if current_checker == regular_checker[0]:       # white checker
                        current_checker = "White_king"
                        self.jump_procedure(starting_square_location, destination_square_location, current_checker,
                                            player_object)
                    else:       # black checker
                        current_checker = "Black_king"
                        self.jump_procedure(starting_square_location, destination_square_location, current_checker,
                                            player_object)
                else:       # piece was not king-ed
                    self.jump_procedure(starting_square_location, destination_square_location, current_checker,
                                        player_object)

        elif current_checker in king_checker:    # if piece is king checker
            # no jump taking place
            if end_column == start_column + 1 or end_column == start_column - 1:
                if current_checker == king_checker[0]:  # White king
                    if end_row == 0:    # Triple king the piece!
                        player_object.set_triple_king_count(1)
                        current_checker = "White_Triple_King"
                        self.non_jump_procedure(starting_square_location, destination_square_location, current_checker)
                    else:   # no promotion to triple king
                        self.non_jump_procedure(starting_square_location, destination_square_location, current_checker)
                else:   # Black king
                    if end_row == 7:    # Triple king the piece!
                        player_object.set_triple_king_count(1)
                        current_checker = "Black_Triple_King"
                        self.non_jump_procedure(starting_square_location, destination_square_location, current_checker)
                    else:   # no promotion to triple king
                        self.non_jump_procedure(starting_square_location, destination_square_location, current_checker)
            # jump takes place
            else:
                if current_checker == king_checker[0]:  # White king
                    if end_row == 0:    # Triple king the piece!
                        player_object.set_triple_king_count(1)
                        current_checker = "White_Triple_King"
                        self.jump_procedure(starting_square_location, destination_square_location, current_checker,
                                            player_object)
                    else:   # no promotion to triple king
                        self.jump_procedure(starting_square_location, destination_square_location, current_checker,
                                            player_object)
                else:   # Black king
                    if end_row == 7:    # Triple king the piece!
                        player_object.set_triple_king_count(1)
                        current_checker = "Black_Triple_King"
                        self.jump_procedure(starting_square_location, destination_square_location, current_checker,
                                            player_object)
                    else:   # no promotion to triple king
                        self.jump_procedure(starting_square_location, destination_square_location, current_checker,
                                            player_object)

        elif current_checker in triple_king_checker:     # if piece is triple king checker
            # no jump taking place
            if end_column == start_column + 1 or end_column == start_column - 1:
                self.non_jump_procedure(starting_square_location, destination_square_location, current_checker)
            # jump takes place
            else:
                if current_checker == triple_king_checker[0]:  # White king
                    self.jump_procedure(starting_square_location, destination_square_location, current_checker,
                                        player_object)
                else:  # Black king
                    self.jump_procedure(starting_square_location, destination_square_location, current_checker,
                                        player_object)

        pieces_captured = player_object.get_captured_pieces_count()
        player_object.set_captured_pieces_count("reset")
        return pieces_captured

    def game_winner(self):
        """Returns the name of the game winner if there is one. If there is no winner returns 'Game has not ended'"""

        for player in self._players:
            if player.get_total_captured_pieces_count() == 12:
                return player.get_name()

        return "Game has not ended"


game = Checkers()
game.pretty_print_board()
# game.create_player("Sam", "White")
# game.create_player("Faris", "Black")
# print(game.play_game("Faris", (5, 2), (4, 1)))
# game.pretty_print_board()
# print(game.play_game("Sam", (2, 3), (3, 2)))
# game.pretty_print_board()
# print(game.play_game("Faris", (4, 1), (2, 3)))
# game.pretty_print_board()
# print(game.play_game("Sam", (1, 2), (3, 4)))
# game.pretty_print_board()
# print(game.play_game("Faris", (5, 4), (4, 5)))
# game.pretty_print_board()
# print(game.play_game("Sam", (0, 1), (1, 2)))
# game.pretty_print_board()
# print(game.play_game("Faris", (4, 5), (2, 3)))
# game.pretty_print_board()
# print(game.play_game("Faris", (2, 3), (0, 1)))
# game.pretty_print_board()
# print(game.play_game("Sam", (2,7),(3,6)))
# game.pretty_print_board()
# print(game.play_game("Faris", (6, 3), (5, 2)))
# game.pretty_print_board()
# print(game.play_game("Sam", (2,5),(3,4)))
# game.pretty_print_board()
# print(game.play_game("Faris", (0, 1), (4, 5)))
# game.pretty_print_board()
# print(game.play_game("Sam", (3,6),(5,4)))
# game.pretty_print_board()
# print(game.play_game("Faris", (6, 5), (4, 3)))
# game.pretty_print_board()
# print(game.play_game("Sam", (1,6),(2,7)))
# game.pretty_print_board()
# print(game.play_game("Faris", (5, 6), (4, 5)))
# game.pretty_print_board()
# print(game.play_game("Sam", (1,4),(2,5)))
# game.pretty_print_board()
# print(game.play_game("Faris", (4, 5), (3, 6)))
# game.pretty_print_board()
# print(game.play_game("Sam", (2,7),(4,5)))
# game.pretty_print_board()
# print(game.play_game("Faris", (7, 6), (6, 5)))
# game.pretty_print_board()
# print(game.play_game("Sam", (4,5),(5,4)))
# game.pretty_print_board()
# print(game.play_game("Faris", (5, 2), (4, 1)))
# game.pretty_print_board()
# print(game.play_game("Sam", (5,4),(7,6)))
# game.pretty_print_board()
# print(game.play_game("Sam",(7,6),(3,2)))
# game.pretty_print_board()
# print(game.play_game("Faris", (4,1),(2,3)))
# game.pretty_print_board()
# print(game.play_game("Sam",(0,3),(1,2)))
# game.pretty_print_board()
# print(game.play_game("Faris", (2,3),(0,1)))
# game.pretty_print_board()
# print(game.play_game("Sam",(2,1),(3,2)))
# game.pretty_print_board()
# print(game.play_game("Faris", (0,1),(1,2)))
# game.pretty_print_board()
# print(game.play_game("Sam",(2,5),(3,4)))
# game.pretty_print_board()
# print(game.play_game("Faris", (1,2),(2,1)))
# game.pretty_print_board()
# print(game.play_game("Sam",(0,5),(1,4)))
# game.pretty_print_board()
# print(game.play_game("Faris", (2,1),(4,3)))
# game.pretty_print_board()
# print(game.play_game("Faris", (4,3),(2,5)))
# game.pretty_print_board()
# print(game.play_game("Faris", (2,5),(0,3)))
# game.pretty_print_board()
# print(game.play_game("Sam",(0,7),(1,6)))
# game.pretty_print_board()
# print(game.play_game("Faris", (5,0),(4,1)))
# game.pretty_print_board()
# print(game.play_game("Sam",(1,6),(2,5)))
# game.pretty_print_board()
# print(game.play_game("Faris", (0,3),(3,6)))
# game.pretty_print_board()
# print(game.play_game("Sam",(1,0),(2,1)))
# game.pretty_print_board()
# print(game.play_game("Faris", (4,1),(3,2)))
# game.pretty_print_board()
# print(game.play_game("Sam",(2,1),(4,3)))
# game.pretty_print_board()
# print(game.play_game("Faris", (3,6),(4,5)))
# game.pretty_print_board()
# print(game.play_game("Sam",(4,3),(5,4)))
# game.pretty_print_board()
# print(game.play_game("Faris", (4,5),(6,3)))
# game.pretty_print_board()
# print(game.game_winner())


# game.pretty_print_board()
#
# # try:
# #     print(game.get_checker_details((7, 9)))
# # except InvalidSquare:
# #     print("That square is invalid! Try again.")
#
# # print(game.game_winner())   # "Game has not ended"
