"""
The different player choices you have

random_move : get_random_move()
smart_ai : get_smart_move()
human_move : wait_for human_input()


env = PieceCapture()

action1 = get_smart_move()
obs, reward , done = player_one_move(action1)

action2

obs2, reward , done = player_two_move(action2)


"""


from env_classes.game import Game
from env_classes.player import Player, BotPlayer
import random as rd
import numpy as np


class PieceCaptureTwoStep:

    def __init__(self, x_size=10, y_size=10):
        self.p1 = Player()
        self.p2 = Player()
        self.curr_player = self.p1
        self.game = Game(self.p1, self.p2, x_size, y_size)
        self.game.start()

    def player_one_move(self, x, y):
        """
        Return
        :param x:
        :param y:
        :return: 0 if move was
        """
        move_valid, p1_reward, p2_reward, done = 0, 0, 0, False

        if self.curr_player == self.p1:
            move_valid, p1_reward, p2_reward = self.game.place_piece(self.p1, (x, y))
            if move_valid:
                self.curr_player = self.p2
                done = self.game.is_game_complete()
            return self.game.Board.Grid, [p1_reward, p2_reward], done,move_valid
        else:
            return self.game.Board.Grid, [p1_reward, p2_reward], done, move_valid

    def player_two_move(self, x, y):
        """
        Return
        :param x:
        :param y:
        :return: 0 if move was
        """
        move_valid, p1_reward, p2_reward, done = 0, 0, 0, False

        if self.curr_player == self.p2:
            move_valid, p1_reward, p2_reward = self.game.place_piece(self.p2, (x, y))
            if move_valid:
                self.curr_player = self.p1
                done = self.game.is_game_complete()
            return -1*self.game.Board.Grid, [p1_reward, p2_reward], done, move_valid
        else:
            return -1*self.game.Board.Grid, [p1_reward, p2_reward], done, move_valid

    def get_random_move(self):
        """
        This function returns a random spot to play from the Game.Board.empty_spaces property
        :empty_move_list: the cached list of available moves
        :return: [row,col]
        """

        if len(self.game.Board.empty_spots) > 0:
            choice = rd.randint(0, len(self.game.Board.empty_spots) - 1)
            return self.game.Board.empty_spots[choice]
        else:
            return -1, -1  # Signifies that there are no empty moves left

    def print(self):
        print(self.game.Board.Grid, end='\r')

    def make_player_smart(self, player_num):
        if player_num == 1:
            self.p1 = BotPlayer()
            self.game.assign_player_piece_color()
        if player_num == 2:
            self.p2 = BotPlayer()
            self.game.assign_player_piece_color()

    def reset(self):
        self.game.reset()
        return self.game.Board.Grid

    def action_space(self):
        return len(self.game.Board.Grid) * len(self.game.Board.Grid[0])
    

