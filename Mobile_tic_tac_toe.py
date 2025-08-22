from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.switch import Switch
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.utils import platform
import random

# Mobile-specific imports
if platform == 'android':
    try:
        from jnius import autoclass, PythonJavaClass
        from android.permissions import request_permissions, Permission
        
        # Request vibration permission
        request_permissions([Permission.VIBRATE])
        
        # Get vibrator service
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Context = autoclass('android.content.Context')
        activity = PythonActivity.mActivity
        vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
    except ImportError:
        vibrator = None
        print("Android vibration not available")
else:
    vibrator = None

def vibrate(duration=50):
    """Add haptic feedback"""
    try:
        if platform == 'android' and vibrator:
            vibrator.vibrate(duration)
    except Exception as e:
        print(f"Vibration failed: {e}")

class MainMenuScreen(Screen):
    def __init__(self, game_logic, **kwargs):
        super().__init__(**kwargs)
        self.game_logic = game_logic
        self.name = 'main_menu'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(text='[color=ffffff][size=36][b]Ultimate Tic-Tac-Toe[/b][/size][/color]',
                     markup=True, size_hint_y=0.15)
        layout.add_widget(title)
        
        # Subtitle
        subtitle = Label(text='[color=bdc3c7][size=16]Choose your battle![/size][/color]',
                        markup=True, size_hint_y=0.08)
        layout.add_widget(subtitle)
        
        # Buttons container
        buttons_layout = BoxLayout(orientation='vertical', spacing=10, 
                                 size_hint_y=0.6, pos_hint={'center_x': 0.5})
        
        # Play vs Computer button
        vs_computer_btn = Button(text='🤖 Play vs Computer', 
                               background_color=(0.2, 0.6, 0.86, 1),
                               font_size=18, size_hint_y=0.2)
        vs_computer_btn.bind(on_press=self.show_difficulty)
        buttons_layout.add_widget(vs_computer_btn)
        
        # Play vs Friend button
        vs_friend_btn = Button(text='👥 Play vs Friend',
                             background_color=(0.18, 0.8, 0.44, 1),
                             font_size=18, size_hint_y=0.2)
        vs_friend_btn.bind(on_press=self.start_friend_game)
        buttons_layout.add_widget(vs_friend_btn)
        
        # Settings button
        settings_btn = Button(text='⚙️ Settings',
                            background_color=(0.58, 0.65, 0.65, 1),
                            font_size=18, size_hint_y=0.2)
        settings_btn.bind(on_press=self.show_settings)
        buttons_layout.add_widget(settings_btn)
        
        # Help button
        help_btn = Button(text='❓ How to Play',
                        background_color=(0.61, 0.35, 0.71, 1),
                        font_size=18, size_hint_y=0.2)
        help_btn.bind(on_press=self.show_help)
        buttons_layout.add_widget(help_btn)
        
        layout.add_widget(buttons_layout)
        
        # Score display
        self.score_label = Label(text=self.get_score_text(),
                               markup=True, size_hint_y=0.1,
                               font_size=14)
        layout.add_widget(self.score_label)
        
        self.add_widget(layout)
        
    def get_score_text(self):
        return f'[color=bdc3c7]Score - You: {self.game_logic.player_score} | Computer: {self.game_logic.computer_score}[/color]'
        
    def update_score_display(self):
        self.score_label.text = self.get_score_text()
        
    def show_difficulty(self, instance):
        self.manager.current = 'difficulty'
        
    def start_friend_game(self, instance):
        self.game_logic.game_mode = 'friend'
        self.game_logic.reset_board()
        self.manager.current = 'game'
        
    def show_settings(self, instance):
        self.manager.current = 'settings'
        
    def show_help(self, instance):
        self.manager.current = 'help'

class DifficultyScreen(Screen):
    def __init__(self, game_logic, **kwargs):
        super().__init__(**kwargs)
        self.game_logic = game_logic
        self.name = 'difficulty'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = Label(text='[color=ffffff][size=28][b]Choose Difficulty[/b][/size][/color]',
                      markup=True, size_hint_y=0.2)
        layout.add_widget(header)
        
        # Difficulty buttons
        buttons_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.6)
        
        difficulties = [
            ('😊 Easy', 'easy', (0.18, 0.8, 0.44, 1), "I'm learning too!"),
            ('🤔 Medium', 'medium', (0.95, 0.61, 0.07, 1), "Let's have fun!"),
            ('😈 Hard', 'hard', (0.91, 0.3, 0.24, 1), "Prepare to lose!")
        ]
        
        for text, difficulty, color, desc in difficulties:
            btn_container = BoxLayout(orientation='vertical', spacing=5, size_hint_y=0.3)
            
            btn = Button(text=text, background_color=color,
                        font_size=20, size_hint_y=0.7)
            btn.bind(on_press=lambda x, d=difficulty: self.set_difficulty(d))
            btn_container.add_widget(btn)
            
            desc_label = Label(text=f'[color=bdc3c7]{desc}[/color]',
                             markup=True, size_hint_y=0.3, font_size=12)
            btn_container.add_widget(desc_label)
            
            buttons_layout.add_widget(btn_container)
            
        layout.add_widget(buttons_layout)
        
        # Back button
        back_btn = Button(text='← Back to Menu',
                         background_color=(0.58, 0.65, 0.65, 1),
                         size_hint_y=0.15, font_size=16)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def set_difficulty(self, difficulty):
        self.game_logic.difficulty = difficulty
        self.game_logic.game_mode = 'computer'
        self.game_logic.reset_board()
        self.manager.current = 'game'
        
    def go_back(self, instance):
        self.manager.current = 'main_menu'

class GameScreen(Screen):
    def __init__(self, game_logic, **kwargs):
        super().__init__(**kwargs)
        self.game_logic = game_logic
        self.name = 'game'
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header_layout = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        
        self.turn_label = Label(text='[color=ffffff][size=20][b]Your Turn[/b][/size][/color]',
                               markup=True, size_hint_y=0.6)
        header_layout.add_widget(self.turn_label)
        
        self.score_label = Label(text='[color=bdc3c7]You: 0 | Computer: 0[/color]',
                               markup=True, size_hint_y=0.4, font_size=14)
        header_layout.add_widget(self.score_label)
        
        layout.add_widget(header_layout)
        
        # Game board
        self.board_layout = GridLayout(cols=3, rows=3, spacing=5, 
                                      size_hint_y=0.6, pos_hint={'center_x': 0.5})
        
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = Button(text='', font_size=40, background_color=(0.2, 0.29, 0.37, 1),
                           color=(1, 1, 1, 1))
                btn.bind(on_press=lambda x, r=i, c=j: self.make_move(r, c))
                self.board_layout.add_widget(btn)
                row.append(btn)
            self.buttons.append(row)
            
        layout.add_widget(self.board_layout)
        
        # Control buttons
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        
        new_game_btn = Button(text='New Game', background_color=(0.2, 0.6, 0.86, 1),
                             font_size=16)
        new_game_btn.bind(on_press=self.new_game)
        control_layout.add_widget(new_game_btn)
        
        menu_btn = Button(text='Main Menu', background_color=(0.58, 0.65, 0.65, 1),
                         font_size=16)
        menu_btn.bind(on_press=self.go_to_menu)
        control_layout.add_widget(menu_btn)
        
        layout.add_widget(control_layout)
        
        self.add_widget(layout)
        
    def on_enter(self):
        """Called when screen is displayed"""
        self.update_display()
        
    def make_move(self, row, col):
        result = self.game_logic.make_move(row, col)
        if result:
            # Add haptic feedback for successful move
            vibrate(30)
            self.update_display()
            
            if self.game_logic.game_active and self.game_logic.game_mode == 'computer' and self.game_logic.current_player == 'O':
                # Schedule computer move after a brief delay
                Clock.schedule_once(lambda dt: self.computer_move(), 0.8)
                
    def computer_move(self):
        result = self.game_logic.computer_move()
        if result:
            # Add slight vibration for computer move
            vibrate(20)
            self.update_display()
            
    def update_display(self):
        # Update board buttons
        for i in range(3):
            for j in range(3):
                cell = self.game_logic.board[i][j]
                self.buttons[i][j].text = cell
                if cell == 'X':
                    self.buttons[i][j].color = (0.91, 0.3, 0.24, 1)  # Red
                elif cell == 'O':
                    self.buttons[i][j].color = (0.2, 0.6, 0.86, 1)   # Blue
                else:
                    self.buttons[i][j].color = (1, 1, 1, 1)          # White
                    
        # Update turn label
        if self.game_logic.game_active:
            turn_text = self.game_logic.get_turn_text()
            self.turn_label.text = f'[color=ffffff][size=20][b]{turn_text}[/b][/size][/color]'
        
        # Update score
        score_text = self.game_logic.get_score_text()
        self.score_label.text = f'[color=bdc3c7]{score_text}[/color]'
        
        # Check for game end
        winner = self.game_logic.check_winner()
        if winner or self.game_logic.is_board_full():
            self.show_game_result(winner)
            
    def show_game_result(self, winner):
        self.game_logic.game_active = False
        
        if winner == "draw" or (winner is None and self.game_logic.is_board_full()):
            title = "It's a Draw! 🤝"
            message = "Good game! Want to play again?"
            vibrate(100)  # Longer vibration for draw
        else:
            if self.game_logic.game_mode == "computer":
                if winner == "X":
                    title = "🎉 You Win!"
                    message = "Congratulations! You beat the computer!"
                    self.game_logic.player_score += 1
                    vibrate(200)  # Victory vibration
                else:
                    title = "🤖 Computer Wins!"
                    message = "Better luck next time!"
                    self.game_logic.computer_score += 1
                    vibrate(50)   # Defeat vibration
            else:  # friend mode
                title = f"🎉 Player {winner} Wins!"
                message = "Great game! Play another round?"
                if winner == "X":
                    self.game_logic.player_score += 1
                else:
                    self.game_logic.friend_score += 1
                vibrate(200)  # Victory vibration
        
        # Create popup
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        result_label = Label(text=f'[color=ffffff][size=18]{message}[/size][/color]',
                           markup=True, size_hint_y=0.7)
        content.add_widget(result_label)
        
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.3)
        
        play_again_btn = Button(text='Play Again', background_color=(0.18, 0.8, 0.44, 1))
        play_again_btn.bind(on_press=lambda x: self.close_popup_and_new_game())
        button_layout.add_widget(play_again_btn)
        
        menu_btn = Button(text='Main Menu', background_color=(0.58, 0.65, 0.65, 1))
        menu_btn.bind(on_press=lambda x: self.close_popup_and_menu())
        button_layout.add_widget(menu_btn)
        
        content.add_widget(button_layout)
        
        self.result_popup = Popup(title=title, content=content, size_hint=(0.8, 0.4),
                                 auto_dismiss=False)
        self.result_popup.open()
        
    def close_popup_and_new_game(self):
        self.result_popup.dismiss()
        self.new_game(None)
        
    def close_popup_and_menu(self):
        self.result_popup.dismiss()
        self.go_to_menu(None)
        
    def new_game(self, instance):
        self.game_logic.reset_board()
        self.update_display()
        
    def go_to_menu(self, instance):
        # Update main menu score display
        main_menu = self.manager.get_screen('main_menu')
        main_menu.update_score_display()
        self.manager.current = 'main_menu'

class SettingsScreen(Screen):
    def __init__(self, game_logic, **kwargs):
        super().__init__(**kwargs)
        self.game_logic = game_logic
        self.name = 'settings'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = Label(text='[color=ffffff][size=28][b]Settings[/b][/size][/color]',
                      markup=True, size_hint_y=0.2)
        layout.add_widget(header)
        
        # Settings content
        settings_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.6)
        
        # Sound effects toggle
        sound_layout = BoxLayout(orientation='horizontal', size_hint_y=0.3)
        sound_label = Label(text='[color=ffffff][size=16]Sound Effects[/size][/color]',
                           markup=True, size_hint_x=0.7)
        sound_layout.add_widget(sound_label)
        
        self.sound_switch = Switch(active=self.game_logic.sounds_enabled, size_hint_x=0.3)
        self.sound_switch.bind(active=self.toggle_sound)
        sound_layout.add_widget(self.sound_switch)
        
        settings_layout.add_widget(sound_layout)
        
        # Reset scores button
        reset_btn = Button(text='Reset All Scores',
                          background_color=(0.91, 0.3, 0.24, 1),
                          size_hint_y=0.4, font_size=16)
        reset_btn.bind(on_press=self.reset_scores)
        settings_layout.add_widget(reset_btn)
        
        layout.add_widget(settings_layout)
        
        # Back button
        back_btn = Button(text='← Back to Menu',
                         background_color=(0.58, 0.65, 0.65, 1),
                         size_hint_y=0.15, font_size=16)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def toggle_sound(self, instance, value):
        self.game_logic.sounds_enabled = value
        
    def reset_scores(self, instance):
        # Create confirmation popup
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        message = Label(text='[color=ffffff]Are you sure you want to reset all scores?[/color]',
                       markup=True, size_hint_y=0.7)
        content.add_widget(message)
        
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.3)
        
        yes_btn = Button(text='Yes', background_color=(0.91, 0.3, 0.24, 1))
        yes_btn.bind(on_press=lambda x: self.confirm_reset())
        button_layout.add_widget(yes_btn)
        
        no_btn = Button(text='No', background_color=(0.58, 0.65, 0.65, 1))
        no_btn.bind(on_press=lambda x: self.reset_popup.dismiss())
        button_layout.add_widget(no_btn)
        
        content.add_widget(button_layout)
        
        self.reset_popup = Popup(title='Reset Scores', content=content, 
                               size_hint=(0.8, 0.3), auto_dismiss=False)
        self.reset_popup.open()
        
    def confirm_reset(self):
        self.game_logic.reset_scores()
        self.reset_popup.dismiss()
        
        # Show confirmation
        content = Label(text='[color=ffffff]All scores have been reset![/color]',
                       markup=True)
        popup = Popup(title='Scores Reset', content=content, 
                     size_hint=(0.6, 0.2), auto_dismiss=True)
        popup.open()
        
    def go_back(self, instance):
        self.manager.current = 'main_menu'

class HelpScreen(Screen):
    def __init__(self, game_logic, **kwargs):
        super().__init__(**kwargs)
        self.game_logic = game_logic
        self.name = 'help'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = Label(text='[color=ffffff][size=28][b]How to Play[/b][/size][/color]',
                      markup=True, size_hint_y=0.15)
        layout.add_widget(header)
        
        # Instructions scroll view
        scroll = ScrollView(size_hint_y=0.7)
        
        instructions_text = """[color=ffffff][size=16]
🎯 [b]Get 3 in a row to win![/b]

📝 [b]Rules:[/b]
• Players take turns placing X's and O's
• First to get 3 in a row wins
• 3 in a row can be horizontal, vertical, or diagonal  
• If the board fills up with no winner, it's a draw

🎮 [b]Game Modes:[/b]
• [b]Play vs Computer:[/b] Choose from 3 difficulty levels
  - Easy: Makes some random moves
  - Medium: Blocks your wins and tries to win
  - Hard: Perfect play - very challenging!
• [b]Play vs Friend:[/b] Take turns on the same device

⚙️ [b]Settings:[/b]
• Toggle sound effects on/off
• Reset all game scores

🏆 [b]Scoring:[/b]
• Scores are tracked for each game mode
• Wins are counted separately for computer and friend games

📱 [b]Mobile Tips:[/b]
• Tap any empty square to place your mark
• Use the back button to return to previous screens
• Game automatically saves your progress

Good luck and have fun! 🎉
[/size][/color]"""
        
        instructions_label = Label(text=instructions_text, markup=True, 
                                 text_size=(None, None), valign='top')
        scroll.add_widget(instructions_label)
        layout.add_widget(scroll)
        
        # Back button
        back_btn = Button(text='← Back to Menu',
                         background_color=(0.58, 0.65, 0.65, 1),
                         size_hint_y=0.12, font_size=16)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def go_back(self, instance):
        self.manager.current = 'main_menu'

class GameLogic:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_mode = None  # "computer" or "friend"
        self.difficulty = "medium"  # "easy", "medium", "hard"
        self.player_score = 0
        self.computer_score = 0
        self.friend_score = 0
        self.game_active = False
        self.sounds_enabled = True
        
    def reset_board(self):
        """Reset the game board"""
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_active = True
        
    def reset_scores(self):
        """Reset all scores"""
        self.player_score = 0
        self.computer_score = 0
        self.friend_score = 0
        
    def make_move(self, row, col):
        """Handle player move"""
        if not self.game_active or self.board[row][col] != "":
            return False
            
        self.board[row][col] = self.current_player
        
        # Check for game end
        if not (self.check_winner() or self.is_board_full()):
            # Switch turns only if game continues
            self.current_player = "O" if self.current_player == "X" else "X"
            
        return True
        
    def computer_move(self):
        """Handle computer move based on difficulty"""
        if not self.game_active or self.current_player != "O":
            return False
            
        move = None
        
        if self.difficulty == "easy":
            if random.random() < 0.3:
                move = self.get_best_move()
            if move is None:
                move = self.get_random_move()
                
        elif self.difficulty == "medium":
            move = self.get_winning_move("O")  # Try to win
            if move is None:
                move = self.get_winning_move("X")  # Block player
            if move is None:
                move = self.get_random_move()
                
        else:  # hard
            move = self.get_best_move()
            
        if move:
            row, col = move
            return self.make_move(row, col)
        return False
        
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
                    if self.check_winner() == player:
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

class TicTacToeApp(App):
    def build(self):
        # Set app properties
        self.title = 'Ultimate Tic-Tac-Toe'
        
        # Handle Android back button
        Window.bind(on_keyboard=self.on_keyboard)
        
        # Handle window resize for orientation changes
        Window.bind(on_resize=self.on_window_resize)
        
        # Initialize game logic
        self.game_logic = GameLogic()
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MainMenuScreen(self.game_logic))
        sm.add_widget(DifficultyScreen(self.game_logic))
        sm.add_widget(GameScreen(self.game_logic))
        sm.add_widget(SettingsScreen(self.game_logic))
        sm.add_widget(HelpScreen(self.game_logic))
        
        return sm
    
    def on_keyboard(self, instance, key, scancode, codepoint, modifier):
        """Handle Android back button"""
        if key == 27:  # Back button pressed
            if self.root.current == 'main_menu':
                # If on main menu, minimize app instead of closing
                if platform == 'android':
                    try:
                        from android import activity
                        activity.moveTaskToBack(True)
                        return True
                    except:
                        pass
                return False  # Let system handle (close app)
            else:
                # Navigate back to previous screen
                if self.root.current in ['difficulty', 'settings', 'help']:
                    self.root.current = 'main_menu'
                elif self.root.current == 'game':
                    if self.game_logic.game_mode == 'computer':
                        self.root.current = 'difficulty'
                    else:
                        self.root.current = 'main_menu'
                return True
        return False
    
    def on_window_resize(self, instance, width, height):
        """Handle screen orientation changes"""
        # Adjust UI based on orientation if needed
        if width > height:
            # Landscape mode - could adjust layouts here
            print("Landscape mode detected")
        else:
            # Portrait mode
            print("Portrait mode detected")
    
    def on_pause(self):
        """Handle app pause (Android lifecycle)"""
        return True  # Allow app to pause
    
    def on_resume(self):
        """Handle app resume (Android lifecycle)"""
        pass

# Run the app
if __name__ == '__main__':
    TicTacToeApp().run()