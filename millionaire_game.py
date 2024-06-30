import tkinter as tk
from PIL import Image, ImageTk
import random
from question import questions  # Import questions from question.py


class MillionaireGame:
    """A class to represent the 'Who Wants to Be a Millionaire' game."""

    def __init__(self, root):
        """Initialize the game with the root window."""
        self.root = root
        self.root.title("Who Wants to Be a Millionaire")
        self.root.geometry("800x550")

        try:
            self.image_02 = ImageTk.PhotoImage(Image.open("skizb.png"))
        except FileNotFoundError:
            print("Error: 'skizb.png' not found.")
            exit(1)

        self.label = tk.Label(root, image=self.image_02)
        self.label.pack(expand=True)

        self.enter_button = tk.Button(root, text="Enter", command=self.ask_name)
        self.enter_button.pack(pady=20)

        self.score = 0
        self.fifty_fifty_used = False
        self.audience_help_used = False

    def ask_name(self):
        """Ask for the player's name."""
        self.label.pack_forget()
        self.enter_button.pack_forget()
        self.root.configure(bg='black')

        self.name_label = tk.Label(self.root, text="Please enter your name!", font=("Helvetica", 16), bg='black', fg='white')
        self.name_label.pack(pady=20)

        self.name_entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.name_entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.get_name)
        self.submit_button.pack(pady=10)

    def get_name(self):
        """Get the player's name and start the game."""
        self.player_name = self.name_entry.get()
        print(f"Player's name: {self.player_name}")

        num_questions = min(10, len(questions))
        if num_questions < 10:
            print("Not enough questions available. Selecting all available questions.")

        self.selected_questions = random.sample(questions, num_questions)
        self.current_question_index = 0

        try:
            self.image_harcer = ImageTk.PhotoImage(Image.open("harcer.png"))
        except FileNotFoundError:
            print("Error: 'harcer.png' not found.")
            exit(1)

        self.score = 0
        self.display_question()

    def display_question(self):
        """Display the current question and options."""
        for widget in self.root.winfo_children():
            widget.pack_forget()
            widget.place_forget()

        self.label = tk.Label(self.root, image=self.image_harcer)
        self.label.pack(expand=True)

        question = self.selected_questions[self.current_question_index]
        self.question_label = tk.Label(self.root, text=question["question"], font=("Helvetica", 14), bg='black', fg='white')
        self.question_label.place(relx=0.5, rely=0.35, anchor='center')

        self.answers_frame = tk.Frame(self.root, bg='black')
        self.answers_frame.place(relx=0.5, rely=0.55, anchor='center')

        self.answer_buttons = []
        for i, option in enumerate(question["options"]):
            button = tk.Button(self.answers_frame, text=option, command=lambda opt=option: self.check_answer(opt), font=("Helvetica", 12))
            button.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            self.answer_buttons.append(button)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 14), bg='black', fg='white')
        self.score_label.place(relx=0.5, rely=0.1, anchor='center')

        self.lifelines_frame = tk.Frame(self.root, bg='black')
        self.lifelines_frame.place(relx=0.5, rely=0.9, anchor='center')

        self.fifty_fifty_button = tk.Button(self.lifelines_frame, text="50/50", command=self.use_fifty_fifty, font=("Helvetica", 12))
        self.fifty_fifty_button.grid(row=0, column=0, padx=10, pady=10)

        self.audience_help_button = tk.Button(self.lifelines_frame, text="Audience Help", command=self.use_audience_help, font=("Helvetica", 12))
        self.audience_help_button.grid(row=0, column=1, padx=10, pady=10)

    def check_answer(self, selected_option):
        """Check if the selected answer is correct."""
        question = self.selected_questions[self.current_question_index]
        if selected_option.startswith(question["answer"]):
            print("Correct!")
            self.score += question["value"]
        else:
            print("Incorrect!")

        self.current_question_index += 1
        if self.current_question_index < len(self.selected_questions):
            self.display_question()
        else:
            self.end_game()

    def use_fifty_fifty(self):
        """Use the 50/50 lifeline to disable two incorrect options."""
        if self.fifty_fifty_used:
            return

        question = self.selected_questions[self.current_question_index]
        correct_answer = question["answer"]
        options = question["options"]

        incorrect_options = [opt for opt in options if not opt.startswith(correct_answer)]
        options_to_disable = random.sample(incorrect_options, 2)

        for button in self.answer_buttons:
            if button.cget("text") in options_to_disable:
                button.config(state=tk.DISABLED)

        self.fifty_fifty_used = True

    def use_audience_help(self):
        """Use the audience help lifeline to display the likelihood of each option being correct."""
        if self.audience_help_used:
            return

        question = self.selected_questions[self.current_question_index]
        correct_answer = question["answer"]
        options = question["options"]

        percentages = [random.randint(5, 20) for _ in options]
        correct_index = next(i for i, opt in enumerate(options) if opt.startswith(correct_answer))
        percentages[correct_index] = max(percentages) + random.randint(20, 40)

        total = sum(percentages)
        percentages = [int(p * 100 / total) for p in percentages]

        for i, button in enumerate(self.answer_buttons):
            button.config(text=f"{options[i]} ({percentages[i]}%)")

        self.audience_help_used = True

    def end_game(self):
        """End the game and display the final score."""
        for widget in self.root.winfo_children():
            widget.pack_forget()
            widget.place_forget()

        congrats_label = tk.Label(self.root, text=f"Congratulations {self.player_name}! Your final score is {self.score}.", font=("Helvetica", 16), bg='black', fg='white')
        congrats_label.pack(pady=20)

        try:
            self.image_avart = ImageTk.PhotoImage(Image.open("avart.png"))
        except FileNotFoundError:
            print("Error: 'avart.png' not found.")
            exit(1)

        self.avart_label = tk.Label(self.root, image=self.image_avart)
        self.avart_label.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    game = MillionaireGame(root)
    root.mainloop()

