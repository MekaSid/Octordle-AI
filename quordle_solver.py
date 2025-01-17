from Quordle_Website_Game import Quordle_Website_Game
from general_solver import General_Solver
import numpy as np, json, string

if __name__ == "__main__":
	dict_path = "/Users/yashwant/Library/Mobile Documents/com~apple~CloudDocs/yash_icloud/CSC 480/Wordle/five_letter_words.json"
	game = Quordle_Website_Game(ultra_instinct = True, daily = True)
	trisha = General_Solver(dict_path, game, num_game_boards=4)
	trisha.live_play_ultra()

