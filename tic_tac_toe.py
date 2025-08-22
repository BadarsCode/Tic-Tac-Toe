import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class TicTacToeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ultimate Tic-Tac-Toe")
        self.root.geometry("500x600")
        self.root.configure(bg='#2C3E50')
        self.root.resizable(False, False)
        
        # Game state
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_mode = None  # "computer" or "friend"
        self.difficulty = "medium"  # "easy", "medium", "hard"
        self.player_score = 0
        self.computer_score = 0
        self.friend_score = 0
        self.game_active = False
        
        # Sound effects (placeholder - would need pygame or similar for actual sounds)
        self.sounds_enabled = True
        
        self.setup_main_menu()
        
    def setup_main_menu(self):
        """Create the main menu interface"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, text="Ultimate Tic-Tac-Toe", 
                        font=("Arial", 24, "bold"), 
                        fg='#ECF0F1', bg='#2C3E50')
        title.pack(pady=30)
        
        # Subtitle with animation effect
        subtitle = tk.Label(self.root, text="Choose your battle!", 
                           font=("Arial", 12), 
                           fg='#BDC3C7', bg='#2C3E50')
        subtitle.pack(pady=10)
        
        # Menu buttons
        button_style = {
            'font': ('Arial', 14, 'bold'),
            'width': 20,
            'height': 2,
            'relief': 'flat',
            'cursor': 'hand2'
        }
        
        # Play vs Computer button
        vs_computer_btn = tk.Button(self.root, text="🤖 Play vs Computer", 
                                   bg='#3498DB', fg='white',
                                   command=self.show_difficulty_selection,
                                   **button_style)
        vs_computer_btn.pack(pady=10)
        
        # Play vs Friend button  
        vs_friend_btn = tk.Button(self.root, text="👥 Play vs Friend", 
                                 bg='#2ECC71', fg='white',
                                 command=self.start_friend_game,
                                 **button_style)
        vs_friend_btn.pack(pady=10)
        
        # Settings button
        settings_btn = tk.Button(self.root, text="⚙️ Settings", 
                               bg='#95A5A6', fg='white',
                               command=self.show_settings,
                               **button_style)
        settings_btn.pack(pady=10)
        
        # How to Play button
        help_btn = tk.Button(self.root, text="❓ How to Play", 
                           bg='#9B59B6', fg='white',
                           command=self.show_help,
                           **button_style)
        help_btn.pack(pady=10)
        
        # Score display
        if self.friend_score > 0:
            score_text = f"Score - Player 1: {self.player_score} | Player 2: {self.friend_score}"
        else:
            score_text = f"Score - You: {self.player_score} | Computer: {self.computer_score}"
        
        score_label = tk.Label(self.root, text=score_text,
                              font=("Arial", 10),
                              fg='#BDC3C7', bg='#2C3E50')
        score_label.pack(side=tk.BOTTOM, pady=20)
        
    def show_difficulty_selection(self):
        """Show difficulty selection screen"""
        self.clear_window()
        self.game_mode = "computer"
        
        # Header
        header = tk.Label(self.root, text="Choose Difficulty", 
                         font=("Arial", 20, "bold"), 
                         fg='#ECF0F1', bg='#2C3E50')
        header.pack(pady=30)
        
        # Difficulty buttons
        difficulties = [
            ("😊 Easy", "easy", "#2ECC71", "I'm learning too!"),
            ("🤔 Medium", "medium", "#F39C12", "Let's have fun!"),
            ("😈 Hard", "hard", "#E74C3C", "Prepare to lose!")
        ]
        
        for text, diff, color, desc in difficulties:
            frame = tk.Frame(self.root, bg='#2C3E50')
            frame.pack(pady=10)
            
            btn = tk.Button(frame, text=text,
                           font=("Arial", 16, "bold"),
                           bg=color, fg='white',
                           width=15, height=2,
                           relief='flat', cursor='hand2',
                           command=lambda d=diff: self.set_difficulty(d))
            btn.pack()
            
            desc_label = tk.Label(frame, text=desc,
                                 font=("Arial", 10),
                                 fg='#BDC3C7', bg='#2C3E50')
            desc_label.pack(pady=5)
        
        # Back button
        back_btn = tk.Button(self.root, text="← Back to Menu",
                            font=("Arial", 12),
                            bg='#95A5A6', fg='white',
                            command=self.setup_main_menu,
                            relief='flat', cursor='hand2')
        back_btn.pack(side=tk.BOTTOM, pady=20)
        
    def set_difficulty(self, difficulty):
        """Set difficulty and start computer game"""
        self.difficulty = difficulty
        self.start_computer_game()
        
    def start_computer_game(self):
        """Start game against computer"""
        self.game_mode = "computer"
        self.reset_board()
        self.setup_game_board()
        
    def start_friend_game(self):
        """Start game against friend"""
        self.game_mode = "friend"
        self.reset_board()
        self.setup_game_board()
        
    def setup_game_board(self):
        """Create the game board interface"""
        self.clear_window()
        self.game_active = True
        
        # Header frame
        header_frame = tk.Frame(self.root, bg='#2C3E50')
        header_frame.pack(pady=10, fill='x')
        
        # Turn indicator
        turn_text = self.get_turn_text()
        self.turn_label = tk.Label(header_frame, text=turn_text,
                                  font=("Arial", 16, "bold"),
                                  fg='#ECF0F1', bg='#2C3E50')
        self.turn_label.pack()
        
        # Score display
        score_text = self.get_score_text()
        self.score_label = tk.Label(header_frame, text=score_text,
                                   font=("Arial", 12),
                                   fg='#BDC3C7', bg='#2C3E50')
        self.score_label.pack()
        
        # Game board frame
        board_frame = tk.Frame(self.root, bg='#2C3E50')
        board_frame.pack(pady=20)
        
        # Create 3x3 grid of buttons
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(board_frame, text="", 
                               font=("Arial", 20, "bold"),
                               width=4, height=2,
                               bg='#34495E', fg='white',
                               relief='raised', bd=2,
                               cursor='hand2',
                               command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
            
        # Control buttons
        control_frame = tk.Frame(self.root, bg='#2C3E50')
        control_frame.pack(pady=20)
        
        new_game_btn = tk.Button(control_frame, text="New Game",
                                font=("Arial", 12),
                                bg='#3498DB', fg='white',
                                command=self.new_game,
                                relief='flat', cursor='hand2')
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        menu_btn = tk.Button(control_frame, text="Main Menu",
                            font=("Arial", 12),
                            bg='#95A5A6', fg='white',
                            command=self.setup_main_menu,
                            relief='flat', cursor='hand2')
        menu_btn.pack(side=tk.LEFT, padx=10)
        
    def make_move(self, row, col):
        """Handle player move"""
        if not self.game_active or self.board[row][col] != "":
            return
            
        # Make the move
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player,
                                     fg='#E74C3C' if self.current_player == 'X' else '#3498DB')
        
        # Play sound effect (placeholder)
        if self.sounds_enabled:
            # Sound effect would be played here
            pass
            
        # Check for game end
        if self.check_winner():
            self.end_game(self.current_player)
            return
        elif self.is_board_full():
            self.end_game("draw")
            return
            
        # Switch turns
        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_turn_display()
        
        # Computer move if needed
        if self.game_mode == "computer" and self.current_player == "O" and self.game_active:
            self.root.after(500, self.computer_move)  # Delay for better UX
            
    def computer_move(self):
        """Handle computer move based on difficulty"""
        if not self.game_active:
            return
            
        move = None
        
        if self.difficulty == "easy":
            # Easy: Random moves with occasional good moves
            if random.random() < 0.3:
                move = self.get_best_move()
            if move is None:
                move = self.get_random_move()
                
        elif self.difficulty == "medium":
            # Medium: Block player wins, try to win, otherwise random
            move = self.get_winning_move("O")  # Try to win
            if move is None:
                move = self.get_winning_move("X")  # Block player
            if move is None:
                move = self.get_random_move()
                
        else:  # hard
            # Hard: Use minimax algorithm for optimal play
            move = self.get_best_move()
            
        if move:
            row, col = move
            self.make_move(row, col)
            
    def get_random_move(self):
        """Get a random available move"""
        available = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        return random.choice(available) if available else None
        
    def get_winning_move(self, player):
        """Check if player can win in next move"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = player
                    if self.check_winner():
                        self.board[i][j] = ""
                        return (i, j)
                    self.board[i][j] = ""
        return None
        
    def get_best_move(self):
        """Get the best move using minimax algorithm"""
        best_score = float('-inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(0, False)
                    self.board[i][j] = ""
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
                        
        return best_move
        
    def minimax(self, depth, is_maximizing):
        """Minimax algorithm for optimal play"""
        winner = self.check_winner()
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif self.is_board_full():
            return 0
            
        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score
            
    def check_winner(self):
        """Check if there's a winner"""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                return row[0]
                
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return self.board[0][col]
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]
            
        return None
        
    def is_board_full(self):
        """Check if board is full"""
        return all(cell != "" for row in self.board for cell in row)
        
    def end_game(self, winner):
        """Handle game end"""
        self.game_active = False
        
        if winner == "draw":
            message = "It's a Draw! 🤝"
            if self.sounds_enabled:
                # Draw sound would be played here
                pass
        else:
            if self.game_mode == "computer":
                if winner == "X":
                    message = "🎉 You Win! Congratulations!"
                    self.player_score += 1
                    if self.sounds_enabled:
                        # Victory sound would be played here
                        pass
                else:
                    message = "🤖 Computer Wins! Better luck next time!"
                    self.computer_score += 1
                    if self.sounds_enabled:
                        # Defeat sound would be played here
                        pass
            else:  # friend mode
                message = f"🎉 Player {winner} Wins!"
                if winner == "X":
                    self.player_score += 1
                else:
                    self.friend_score += 1
                if self.sounds_enabled:
                    # Victory sound would be played here
                    pass
        
        # Show result dialog
        result = messagebox.askquestion("Game Over", 
                                       message + "\n\nPlay again?",
                                       icon='question')
        
        if result == 'yes':
            self.new_game()
        else:
            self.setup_main_menu()
            
    def new_game(self):
        """Start a new game with same settings"""
        self.reset_board()
        self.setup_game_board()
        
    def reset_board(self):
        """Reset the game board"""
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_active = True
        
    def get_turn_text(self):
        """Get current turn display text"""
        if self.game_mode == "computer":
            return "Your Turn" if self.current_player == "X" else "Computer's Turn"
        else:
            return f"Player {self.current_player}'s Turn"
            
    def get_score_text(self):
        """Get score display text"""
        if self.game_mode == "computer":
            return f"You: {self.player_score} | Computer: {self.computer_score}"
        else:
            return f"Player X: {self.player_score} | Player O: {self.friend_score}"
            
    def update_turn_display(self):
        """Update the turn indicator"""
        if hasattr(self, 'turn_label'):
            self.turn_label.config(text=self.get_turn_text())
            
    def show_settings(self):
        """Show settings screen"""
        self.clear_window()
        
        # Header
        header = tk.Label(self.root, text="Settings", 
                         font=("Arial", 20, "bold"), 
                         fg='#ECF0F1', bg='#2C3E50')
        header.pack(pady=30)
        
        # Settings frame
        settings_frame = tk.Frame(self.root, bg='#2C3E50')
        settings_frame.pack(pady=20)
        
        # Sound effects toggle
        sound_frame = tk.Frame(settings_frame, bg='#2C3E50')
        sound_frame.pack(pady=10, fill='x')
        
        tk.Label(sound_frame, text="Sound Effects:", 
                font=("Arial", 12), fg='#ECF0F1', bg='#2C3E50').pack(side='left')
        
        sound_btn = tk.Button(sound_frame, 
                             text="ON" if self.sounds_enabled else "OFF",
                             font=("Arial", 10),
                             bg='#2ECC71' if self.sounds_enabled else '#E74C3C',
                             fg='white', width=8,
                             command=self.toggle_sound,
                             relief='flat', cursor='hand2')
        sound_btn.pack(side='right')
        
        # Reset scores button
        reset_frame = tk.Frame(settings_frame, bg='#2C3E50')
        reset_frame.pack(pady=20, fill='x')
        
        reset_btn = tk.Button(reset_frame, text="Reset All Scores",
                             font=("Arial", 12),
                             bg='#E74C3C', fg='white',
                             command=self.reset_scores,
                             relief='flat', cursor='hand2')
        reset_btn.pack()
        
        # Back button
        back_btn = tk.Button(self.root, text="← Back to Menu",
                            font=("Arial", 12),
                            bg='#95A5A6', fg='white',
                            command=self.setup_main_menu,
                            relief='flat', cursor='hand2')
        back_btn.pack(side=tk.BOTTOM, pady=20)
        
    def toggle_sound(self):
        """Toggle sound effects"""
        self.sounds_enabled = not self.sounds_enabled
        self.show_settings()  # Refresh to update button
        
    def reset_scores(self):
        """Reset all scores"""
        result = messagebox.askquestion("Reset Scores",
                                       "Are you sure you want to reset all scores?",
                                       icon='warning')
        if result == 'yes':
            self.player_score = 0
            self.computer_score = 0
            self.friend_score = 0
            messagebox.showinfo("Scores Reset", "All scores have been reset!")
            
    def show_help(self):
        """Show how to play screen"""
        self.clear_window()
        
        # Header
        header = tk.Label(self.root, text="How to Play", 
                         font=("Arial", 20, "bold"), 
                         fg='#ECF0F1', bg='#2C3E50')
        header.pack(pady=20)
        
        # Instructions
        instructions = [
            "🎯 Get 3 in a row to win!",
            "",
            "📝 Rules:",
            "• Players take turns placing X's and O's",
            "• First to get 3 in a row wins",
            "• 3 in a row can be horizontal, vertical, or diagonal",
            "• If the board fills up with no winner, it's a draw",
            "",
            "🎮 Game Modes:",
            "• Play vs Computer: Choose from 3 difficulty levels",
            "• Play vs Friend: Take turns on the same device",
            "",
            "🎵 Tip: Enable sound effects in settings for more fun!"
        ]
        
        for instruction in instructions:
            label = tk.Label(self.root, text=instruction,
                           font=("Arial", 12),
                           fg='#ECF0F1', bg='#2C3E50',
                           justify='left')
            label.pack(pady=2)
            
        # Back button
        back_btn = tk.Button(self.root, text="← Back to Menu",
                            font=("Arial", 12),
                            bg='#95A5A6', fg='white',
                            command=self.setup_main_menu,
                            relief='flat', cursor='hand2')
        back_btn.pack(side=tk.BOTTOM, pady=20)
        
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def run(self):
        """Start the game"""
        self.root.mainloop()

# Run the game
if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()

