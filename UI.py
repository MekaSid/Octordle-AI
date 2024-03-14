import tkinter as tk
import json
import random
from general_solver import General_Solver
from Octordle_Website_Game import Octordle_Website_Game
import copy

class OctordleUI:
    def __init__(self, master):
        self.master = master
        master.title('Octordle Game')

        file_path = 'five_letter_words.json'

        with open(file_path, 'r') as file:
            self.target_words = json.load(file)

        self.target_words = random.sample(self.target_words, 8)

        # Define target words for testing
        # self.target_words = ["APPLE", "BERRY", "CHERR", "DATES", "ELDER", "FIGGY", "GRAPE", "HONEY"]
        # Ensure all target words are uppercase
        self.target_words = [word.upper() for word in self.target_words]
        # Track the current guess index and which boards are solved
        self.current_guess_index = 0
        self.solved_boards = [False] * len(self.target_words)

        # Set the size of the window
        master.geometry('1280x800')

        # Define colors
        self.colors = {"correct": "#538d4e", "present": "#b59f3b", "absent": "#3a3a3c"}

        # Create frames for each word's guesses and separators
        self.frames = [tk.Frame(master, width=100, height=600) for _ in range(8)]
        for index, frame in enumerate(self.frames):
            frame.grid(row=1, column=index * 2)
            if index < 7:  # Add separators between sections but not after the last one
                separator = tk.Frame(master, width=2, height=600, bg="black")
                separator.grid(row=1, column=index * 2 + 1, sticky="ns")

        # Create labels for guesses in each frame
        self.guess_labels = [[[tk.Label(frame, text=' ', bg="#3a3a3c", fg="white", font=('Helvetica', 16), width=2,
                                        height=1) for _ in range(5)] for _ in range(13)] for frame in self.frames]
        for frame_index, frame_labels in enumerate(self.guess_labels):
            for guess_index, row in enumerate(frame_labels):
                for letter_index, label in enumerate(row):
                    label.grid(row=guess_index, column=letter_index, padx=2, pady=2)

        # Add input field and submit button
        self.input_field = tk.Entry(master, width=10, font=('Helvetica', 16))
        self.input_field.grid(row=0, column=0, columnspan=8)

        self.submit_button = tk.Button(master, text="Submit Guess", command=self.submit_guess, font=('Helvetica', 14))
        self.submit_button.grid(row=0, column=8, columnspan=2)

        ## Use General_Solver to come up with appropriate words
        
        #3D feedback array
        self.feedback_array_all_guess = [None for _ in range(13)]
        self.feedback_array_current_guess = [[None for _ in range(5)] for _ in range(8)]

        # Get the guess
        #self.octordle = Octordle_Website_Game()
        self.solver = General_Solver(game = self)
        self.solver.live_play_ultra()



    def submit_guess(self):
        guess = self.input_field.get().upper()
        # Clear input field after submission
        self.input_field.delete(0, tk.END)

        if len(guess) == 5 and self.current_guess_index < 13:
            for word_index, target_word in enumerate(self.target_words):
                if not self.solved_boards[word_index]:  # Only update if not already solved
                    self.update_guess(word_index, self.current_guess_index, guess, target_word)
            self.current_guess_index += 1
        #print(self.feedback_array_current_guess)
        print(self.feedback_array_all_guess)
        # feedback, done = self.octordle.advance_state(feedback = self.feedback_array_all_guess[0])
        #self.solver.live_play_ultra()
        feedback = self.feedback_array_all_guess[self.current_guess_index - 1]
        self.solver.hi()
        self.solver.add_to_encoded_guesses(feedback)
        self.solver.live_play_ultra()




    def update_guess(self, word_index, guess_index, guess, target_word):
        target_word = target_word.lower()
        guess = guess.lower()
        correct_guess = True
        for i, char in enumerate(guess):
            if char == target_word[i]:
                correct_color = self.colors["correct"]
                feedback = [char, 3]
            elif char in target_word:
                correct_color = self.colors["present"]
                correct_guess = False  # Part of the word, but wrong position
                feedback = [char,2]
            else:
                correct_color = self.colors["absent"]
                correct_guess = False  # Not in the word at all
                feedback = [char, 1]
            self.guess_labels[word_index][guess_index][i].config(text=char, bg=correct_color, fg="white")
            #encoded guesses changing here
            self.feedback_array_current_guess[word_index][i] = feedback
            print(self.feedback_array_current_guess[word_index])
        self.feedback_array_all_guess[guess_index] = copy.deepcopy(self.feedback_array_current_guess)
        return correct_guess and guess == target_word


# Create the Tkinter application
root = tk.Tk()
app = OctordleUI(root)

# Run the application
root.mainloop()