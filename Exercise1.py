import tkinter as tk
from tkinter import messagebox
import random

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Master")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        
        # Background color for the layout of the screen 
        self.bg_gradient_top = "#1e3a8a"      
        self.bg_gradient_bottom = "#3b82f6"   
        self.bg_color = "#2563eb"             
        self.card_bg = "#eff6ff"             
        self.primary_color = "#1e40af"        
        self.secondary_color = "#0ea5e9"      
        self.accent_color = "#60a5fa"        
        self.success_color = "#10b981"        
        self.error_color = "#ef4444"          
        self.warning_color = "#f59e0b"        
        self.text_dark = "#1e293b"            
        
        self.root.configure(bg=self.bg_color)
        
        # Quiz variables
        self.difficulty = 0
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.attempt = 1
        self.current_answer = 0
        self.num1 = 0
        self.num2 = 0
        self.operation = ''
        
        # Display the menu 
        self.displayMenu()
    
    def displayMenu(self):
        """Shows the main menu where users select their preferred difficulty level"""
        
        # Remove all existing widgets from the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Blue gradient background
        canvas = tk.Canvas(self.root, width=650, height=550, 
                          bg=self.bg_color, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Create gradient effect
        for i in range(550):
            ratio = i / 550
            color = self.interpolate_color(self.bg_gradient_top, 
                                          self.bg_gradient_bottom, ratio)
            canvas.create_line(0, i, 650, i, fill=color)
        
        # Main content frame
        main_frame = tk.Frame(canvas, bg=self.card_bg, relief='flat')
        main_frame.place(relx=0.5, rely=0.5, anchor='center', 
                        width=550, height=450)
        
        # Styling for the top bar and frame
        top_bar = tk.Frame(main_frame, bg=self.primary_color, height=6)
        top_bar.pack(fill='x')
        
        # Title of the page
        title_label = tk.Label(main_frame, text="Math Master Quiz", 
                              font=("Helvetica", 34, "bold"), 
                              bg=self.card_bg, fg=self.primary_color,
                              pady=20)
        title_label.pack()
        
        # 
        divider = tk.Frame(main_frame, bg=self.accent_color, height=2)
        divider.pack(fill='x', padx=50, pady=10)
        
        # Allows the user to select the difficulty level using labels
        difficulty_label = tk.Label(main_frame, 
                                   text="DIFFICULTY LEVEL", 
                                   font=("Helvetica", 18, "bold"), 
                                   bg=self.card_bg, fg=self.primary_color,
                                   pady=15)
        difficulty_label.pack()
        
        # Instructions frame
        inst_frame = tk.Frame(main_frame, bg=self.card_bg)
        inst_frame.pack(pady=10)
        
        options = [
            "1. Easy",
            "2. Moderate",
            "3. Advanced"
        ]
        
        for option in options:
            label = tk.Label(inst_frame, text=option, 
                           font=("Arial", 16), 
                           bg=self.card_bg, fg=self.text_dark)
            label.pack(anchor='w', pady=8, padx=80)
        
        # Buttons for difficulty selection
        button_frame = tk.Frame(main_frame, bg=self.card_bg)
        button_frame.pack(pady=30)
        
        easy_btn = tk.Button(button_frame, text="Easy", width=12, height=2,
                            font=("Helvetica", 12, "bold"), 
                            bg=self.success_color, fg="white",
                            relief='flat', cursor="hand2",
                            command=lambda: self.startQuiz(1))
        easy_btn.grid(row=0, column=0, padx=10)
        
        moderate_btn = tk.Button(button_frame, text="Moderate", width=12, height=2,
                                font=("Helvetica", 12, "bold"), 
                                bg=self.warning_color, fg="white",
                                relief='flat', cursor="hand2",
                                command=lambda: self.startQuiz(2))
        moderate_btn.grid(row=0, column=1, padx=10)
        
        advanced_btn = tk.Button(button_frame, text="Advanced", width=12, height=2,
                                font=("Helvetica", 12, "bold"), 
                                bg=self.error_color, fg="white",
                                relief='flat', cursor="hand2",
                                command=lambda: self.startQuiz(3))
        advanced_btn.grid(row=0, column=2, padx=10)
        
        # Hover effects
        easy_btn.bind("<Enter>", lambda e: easy_btn.configure(bg="#059669"))
        easy_btn.bind("<Leave>", lambda e: easy_btn.configure(bg=self.success_color))
        
        moderate_btn.bind("<Enter>", lambda e: moderate_btn.configure(bg="#d97706"))
        moderate_btn.bind("<Leave>", lambda e: moderate_btn.configure(bg=self.warning_color))
        
        advanced_btn.bind("<Enter>", lambda e: advanced_btn.configure(bg="#dc2626"))
        advanced_btn.bind("<Leave>", lambda e: advanced_btn.configure(bg=self.error_color))
    
    def interpolate_color(self, color1, color2, ratio):
        """Creates a smooth color transition between two colors for gradient backgrounds"""
        c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def startQuiz(self, difficulty):
        """Begins the quiz by setting the difficulty and resetting all counters"""
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        self.displayProblem()
    
    def randomInt(self):
        """Generates two random numbers appropriate for the selected difficulty level.
        Easy: single digit numbers (0-9)
        Moderate: double digit numbers (10-99)
        Advanced: four-digit numbers (1000-9999)"""
        if self.difficulty == 1:  # Easy questions 
            return random.randint(0, 9), random.randint(0, 9)
        elif self.difficulty == 2:  # Moderate questions 
            return random.randint(10, 99), random.randint(10, 99)
        else:  # Advanced questions 
            return random.randint(1000, 9999), random.randint(1000, 9999)
    
    def decideOperation(self):
        """Randomly selects either addition or subtraction for the problem.
        Returns either '+' or '-' as a character"""
        return random.choice(['+', '-'])
    
    def displayProblem(self):
        """Presents a math problem to the user and collects their answer through an Entry widget"""
        
        # Clear all widgets before loading the new question screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create a new problem when starting a new question
        if self.attempt == 1:
            self.num1, self.num2 = self.randomInt()
            self.operation = self.decideOperation()
            
            # Calculate the correct answer for this problem
            if self.operation == '+':
                self.current_answer = self.num1 + self.num2
            else:
                self.current_answer = self.num1 - self.num2
            
            self.current_question += 1
        
        # Blue background
        canvas = tk.Canvas(self.root, width=650, height=550, 
                          bg=self.bg_color, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Create gradient
        for i in range(550):
            ratio = i / 550
            color = self.interpolate_color(self.bg_gradient_top, 
                                          self.bg_gradient_bottom, ratio)
            canvas.create_line(0, i, 650, i, fill=color)
        
        # Main card
        main_card = tk.Frame(canvas, bg=self.card_bg, relief='flat')
        main_card.place(relx=0.5, rely=0.5, anchor='center', 
                       width=550, height=450)
        
        # Styled header bar
        top_bar = tk.Frame(main_card, bg=self.primary_color, height=6)
        top_bar.pack(fill='x')
        
        # Display question number and score
        info_label = tk.Label(main_card, 
                             text=f"Question {self.current_question}/{self.total_questions}     Score: {self.score}/100",
                             font=("Helvetica", 13, "bold"), 
                             bg=self.card_bg, fg=self.primary_color,
                             pady=20)
        info_label.pack()
        
        # Question View
        problem_frame = tk.Frame(main_card, bg=self.card_bg)
        problem_frame.pack(pady=40)
        
        problem_text = f"{self.num1} {self.operation} {self.num2} ="
        problem_label = tk.Label(problem_frame, text=problem_text, 
                                font=("Helvetica", 40, "bold"),
                                bg=self.card_bg, fg=self.primary_color)
        problem_label.pack()
        
        # Entry for answer
        self.answer_entry = tk.Entry(problem_frame, font=("Helvetica", 24), 
                                     width=12, justify='center',
                                     relief='solid', bd=2,
                                     bg="white",
                                     fg=self.text_dark,
                                     highlightbackground=self.secondary_color,
                                     highlightthickness=2)
        self.answer_entry.pack(pady=25, ipady=8)
        self.answer_entry.focus()
        
        # Enter key to submit answers
        self.answer_entry.bind('<Return>', lambda e: self.checkAnswer())
        
        # Submit button
        submit_btn = tk.Button(problem_frame, text="Submit Answer", 
                              font=("Helvetica", 13, "bold"), 
                              bg=self.primary_color, fg="white",
                              width=18, height=2, 
                              relief='flat', cursor="hand2",
                              command=self.checkAnswer)
        submit_btn.pack(pady=10)
        
        # Hover effect
        submit_btn.bind("<Enter>", lambda e: submit_btn.configure(bg="#1e3a8a"))
        submit_btn.bind("<Leave>", lambda e: submit_btn.configure(bg=self.primary_color))
        
        # Feedback label after the user selects
        self.feedback_label = tk.Label(main_card, text="", 
                                       font=("Helvetica", 12, "bold"),
                                       bg=self.card_bg)
        self.feedback_label.pack(pady=15)
    
    def checkAnswer(self):
        """Validates the user's input and manages the scoring and attempt logic"""
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
            return
        
        if self.isCorrect(user_answer):
            # Give points depending on which attempt was successful
            if self.attempt == 1:
                self.score += 10
            else:
                self.score += 5
            
            # Reset for the next question
            self.attempt = 1
            
            # Move to the next question after a short pause
            self.root.after(800, self.nextQuestion)
        else:
            if self.attempt == 1:
                # Allow one more try at this problem
                self.attempt = 2
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
                
                # Refresh display with error feedback
                self.displayProblem()
                self.feedback_label.config(text="Incorrect. Try again!", 
                                          fg=self.error_color)
            else:
                # No attempts remaining, prompt or direct user to the next question
                self.attempt = 1
                self.root.after(1500, self.nextQuestion)
    
    def isCorrect(self, user_answer):
        """Compares the user's answer with the correct solution and displays feedback messages"""
        if user_answer == self.current_answer:
            if self.attempt == 1:
                messagebox.showinfo("Correct!", "Well done! (+10 points)")
            else:
                messagebox.showinfo("Correct!", "Good job on second attempt! (+5 points)")
            return True
        else:
            if self.attempt == 1:
                # The messagebox must not appear yet, give the users a second chance
                return False
            else:
                messagebox.showinfo("Incorrect", 
                                  f"The correct answer was {self.current_answer}")
                return False
    
    def nextQuestion(self):
        """Determines whether to show another question or display final results"""
        if self.current_question < self.total_questions:
            self.displayProblem()
        else:
            self.displayResults()
    
    def displayResults(self):
        """Shows the user's final score out of 100 and assigns a letter grade based on performance"""
        # Clear all widgets to show results screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Determine grade based on score
        if self.score >= 90:
            grade = "A+"
        elif self.score >= 80:
            grade = "A"
        elif self.score >= 70:
            grade = "B"
        elif self.score >= 60:
            grade = "C"
        elif self.score >= 50:
            grade = "D"
        else:
            grade = "F"
        
        # Blue background for the layout 
        canvas = tk.Canvas(self.root, width=650, height=550, 
                          bg=self.bg_color, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Create gradient
        for i in range(550):
            ratio = i / 550
            color = self.interpolate_color(self.bg_gradient_top, 
                                          self.bg_gradient_bottom, ratio)
            canvas.create_line(0, i, 650, i, fill=color)
        
        # Results card once the game is over
        result_card = tk.Frame(canvas, bg=self.card_bg, relief='flat')
        result_card.place(relx=0.5, rely=0.5, anchor='center', 
                         width=550, height=450)
        
        # Decorative top bar
        top_bar = tk.Frame(result_card, bg=self.primary_color, height=6)
        top_bar.pack(fill='x')
        
        result_frame = tk.Frame(result_card, bg=self.card_bg)
        result_frame.pack(expand=True, pady=30)
        
        # Title after the completion of the quiz
        title = tk.Label(result_frame, text="QUIZ COMPLETED!", 
                        font=("Helvetica", 32, "bold"), 
                        bg=self.card_bg, fg=self.primary_color)
        title.pack(pady=(20, 30))
        
        # Display the user's score after the game
        score_label = tk.Label(result_frame, 
                              text=f"Final Score: {self.score} / 100",
                              font=("Helvetica", 24, "bold"),
                              bg=self.card_bg, fg=self.text_dark)
        score_label.pack(pady=15)
        
        # Grade display
        grade_label = tk.Label(result_frame, text=f"Grade: {grade}",
                              font=("Helvetica", 28, "bold"), 
                              bg=self.card_bg, fg=self.primary_color)
        grade_label.pack(pady=15)
        
        # Prompt to play again
        prompt_label = tk.Label(result_frame, 
                               text="Would you like to play again?",
                               font=("Helvetica", 14),
                               bg=self.card_bg, fg=self.text_dark)
        prompt_label.pack(pady=20)
        
        # Button frame so that users can select it by clicking
        button_frame = tk.Frame(result_frame, bg=self.card_bg)
        button_frame.pack(pady=20)
        
        play_again_btn = tk.Button(button_frame, text="Play Again", 
                                   font=("Helvetica", 13, "bold"), 
                                   bg=self.primary_color, 
                                   fg="white", width=14, height=2,
                                   relief='flat', cursor="hand2",
                                   command=self.displayMenu)
        play_again_btn.grid(row=0, column=0, padx=10)
        
        quit_btn = tk.Button(button_frame, text="Quit", 
                            font=("Helvetica", 13, "bold"), 
                            bg=self.error_color, 
                            fg="white", width=14, height=2,
                            relief='flat', cursor="hand2",
                            command=self.root.quit)
        quit_btn.grid(row=0, column=1, padx=10)
        
        # Interactive hover styles to appeal the users
        play_again_btn.bind("<Enter>", lambda e: 
                           play_again_btn.configure(bg="#1e3a8a"))
        play_again_btn.bind("<Leave>", lambda e: 
                           play_again_btn.configure(bg=self.primary_color))
        
        quit_btn.bind("<Enter>", lambda e: 
                     quit_btn.configure(bg="#dc2626"))
        quit_btn.bind("<Leave>", lambda e: 
                     quit_btn.configure(bg=self.error_color))


# Main program for the whole quiz
if __name__ == "__main__":
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()