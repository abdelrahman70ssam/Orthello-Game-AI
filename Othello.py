import tkinter as tk
import customtkinter as ctk  # Importing custom tkinter module
import tkinter.messagebox

class ctkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Tkinter Layout")
        
        # Initialize the game board
        self.board = [['' for _ in range(8)] for _ in range(8)]
        
        # Set initial pieces
        self.board[3][3] = "white"
        self.board[4][4] = "white"
        self.board[3][4] = "black"
        self.board[4][3] = "black"
        
        # Set the initial player (black)
        self.current_player = "black"
        
        # Create a frame for the label and segmented button
        top_frame = tk.Frame(self.root, bg="#24BB70")
        top_frame.pack(padx=300, pady=5)
        
        # Label
        difficulty_label = ctk.CTkLabel(top_frame, text="Difficulty Level", font=("arial", 40, "bold"))
        difficulty_label.pack(side="left", padx=10, pady=5)
        
        # Segmented Button
        self.difficulty_var = tk.StringVar() 
        
        # Options for segmented button
        options = ["Easy", "Intermediate", "Hard"]
        
        segmented_button = ctk.CTkSegmentedButton(top_frame, 
                                                variable=self.difficulty_var, 
                                                command=self.on_difficulty_select,
                                                values=options,
                                                unselected_color="#41EEEE",
                                                fg_color="#019C5A",
                                                text_color="#000000", height=40,
                                                font=("arial", 20, "bold"))
        segmented_button.pack(side="left", padx=10, pady=5)
        self.segmented_button = segmented_button

        self.black_pieces_left = 30
        self.white_pieces_left = 30

        
        # Create a frame for the additional information labels
        info_frame = tk.Frame(self.root, bg="#24BB70")
        info_frame.pack(padx=10, side="right")

        # Human moves count label
        self.human_pieces_label = tk.Label(top_frame, text=f"Human player(Black):      {self.count_pieces('black', self.board)}", font=("arial", 12, "bold"), bg="#24BB70")
        self.human_pieces_label.pack(side="top", padx=5, pady=1)

        # Computer moves count label
        self.computer_pieces_label = tk.Label(top_frame, text=f"Computer player(White): {self.count_pieces('white', self.board)}", font=("arial", 12, "bold"), bg="#24BB70")
        self.computer_pieces_label.pack(side="top", padx=5, pady=1)

        # Human moves count label
        self.human_left_label = tk.Label(top_frame, text=f"Human left:{self.black_pieces_left}", font=("arial", 12, "bold"), bg="#24BB70")
        self.human_left_label.pack(side="right", padx=5, pady=1)

        # Computer moves count label
        self.computer_right_label = tk.Label(top_frame, text=f"Computer left: {self.white_pieces_left}", font=("arial", 12, "bold"), bg="#24BB70")
        self.computer_right_label.pack(side="right", padx=5, pady=1)
        
        # Grid of Buttons
        self.create_button_grid()
        

    
    # update labels above    
    def update_human_pieces_label(self):
        self.human_pieces_label.config(text=f"Human player(Black): {self.count_pieces('black', self.board)}")

    def update_computer_pieces_label(self):
        self.computer_pieces_label.config(text=f"Computer player(White): {self.count_pieces('white', self.board)}")
    
    def update_human_left_label(self):
        self.human_left_label.config(text=f"Human left:{self.black_pieces_left}")

    def update_computer_left_label(self):
        self.computer_right_label.config(text=f"Computer left:{self.white_pieces_left}")    
   
     
    
    def on_difficulty_select(self, value):
        self.disable_buttons()

    # Disable each button within the segmented button
    def disable_buttons(self):
        for child in self.segmented_button.winfo_children():
            child.configure(state="disabled")
        # Update the UI to process the state change without lag
        self.root.update_idletasks()
    
    
    # create buttons
    def create_button_grid(self):        
        self.buttons = []
        self.valid_moves = self.getAllValidMoves(self.current_player, self.board)  # Get all valid moves initially
        for i in range(8):
            button_row = tk.Frame(self.root)  # Create a frame for each row of buttons
            button_row.pack()  # Pack the frame to ensure buttons are in the same line
            button_row_list = []
            for j in range(8):
                button = ctk.CTkButton(button_row, text="", width=90, height=80, fg_color="#019A6A", command=lambda i=i, j=j: self.on_button_click(i, j))
                button.pack(side="left", padx=1, pady=1)  # Pack buttons to the left side of the frame
                button_row_list.append(button)
            self.buttons.append(button_row_list)

        # Set initial pieces
        self.buttons[3][3].configure(text="⚫", text_color="#FFFFFF", font=("arial", 50, "bold"))
        self.buttons[4][4].configure(text="⚫", text_color="#FFFFFF", font=("arial", 50, "bold"))
        self.buttons[3][4].configure(text="⚫", text_color="#000000", font=("arial", 50, "bold"))
        self.buttons[4][3].configure(text="⚫", text_color="#000000", font=("arial", 50, "bold"))
        
        
    # activated after clicking on button
    def on_button_click(self, row, col):
        if self.current_player == "black":
            if (row, col) in (self.getAllValidMoves(self.current_player, self.board)) :
                self.move(row, col, self.current_player, self.board, True)
                # Signal that the player has made a move
                self.player_move.set(1)


    def move(self, i, j, player, board, change_buttons):
        button1 = None 
        moves = self.getAllValidMoves(self.current_player, board)
        if (i, j) in moves:  
            board[i][j] = player
            opponent = 'white' if player == 'black' else 'black'
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
            
            for dr, dc in directions:
                r, c = i + dr, j + dc
                pieces_to_flip = []

                while 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] == '':
                        break
                    elif board[r][c] == player:
                        if pieces_to_flip:
                            for flip_row, flip_col in pieces_to_flip:
                                board[flip_row][flip_col] = player
                                
                                if(change_buttons):
                                    # change buttons
                                    button = self.buttons[flip_row][flip_col]
                                    self.chnge_button(button)
                        break
                    elif board[r][c] == opponent:
                        pieces_to_flip.append((r, c))
                    r += dr
                    c += dc
            
            if player == 'black' and board == self.board:
                self.black_pieces_left -= 1
            if player == 'white' and board == self.board:
                self.white_pieces_left -= 1
            
            # Set button1 to the clicked button
            button1 = self.buttons[i][j]
        
        # Toggle the circle if button1 is not None
        if button1 is not None and change_buttons:
            self.chnge_button(button1) 

                    
    # set button with specific color (white, black)
    def chnge_button(self, button):
        # goes to specified position and change it is color
        if self.current_player == "black":
            button.configure(text="⚫", text_color="#000000", font=("arial", 50, "bold"))
        else:
            button.configure(text="⚫", text_color="#FFFFFF", font=("arial", 50, "bold"))


    # Reset grey color of possible moves to original color
    def reset_button_colors(self):
        for i in range(8):
            for j in range(8):
                button = self.buttons[i][j]
                moves = self.getAllValidMoves(self.current_player, self.board)
                if (i, j) in moves:
                    button.configure(fg_color="#AAAAAA")  # Set valid move buttons to grey
                else:
                    button.configure(fg_color="#019A6A")  # Set other buttons to their original color

    # Highlight avilable moves with grey
    def highlight_valid_moves(self):
        moves = self.getAllValidMoves(self.current_player, self.board)
        for i, j in moves:
            self.buttons[i][j].configure(fg_color="#AAAAAA")  # Highlight valid move buttons with grey


    # if there is a filpping button bet two equal colors, it should be flipped
    def is_outFlank(self, row, col):
        target_color = self.current_player
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dr, dc in directions:
            r, c = row + dr, col + dc
            has_opponent_piece = False
            while 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == '':
                    break
                elif self.board[r][c] == target_color:
                    if has_opponent_piece:
                        return True
                    else:
                        break
                else:
                    has_opponent_piece = True
                r += dr
                c += dc

        return False

    # Get all valid moves for a player
    def getAllValidMoves(self, player, board):
        moves = []
        Target_pice = 'white' if player == 'black' else 'black'
        for i in range(8):
            for j in range(8):
                if board[i][j] == Target_pice:
                    if i-1 >= 0 and board[i-1][j] == "" and self.is_outFlank(i-1, j):
                        if (i-1, j) not in moves:
                            moves.append((i-1, j))
                    if i+1 < 8 and board[i+1][j] == "" and self.is_outFlank(i+1, j):
                        if (i+1, j) not in moves:
                            moves.append((i+1, j))
                    if j-1 >= 0 and board[i][j-1] == "" and self.is_outFlank(i, j-1):
                        if (i, j-1) not in moves:
                            moves.append((i, j-1))
                    if j+1 < 8 and board[i][j+1] == "" and self.is_outFlank(i, j+1):
                        if (i, j + 1) not in moves:
                            moves.append((i, j + 1))
        return moves

    def is_board_full(self, board):
        for row in board:
            if '' in row:
                return False
        return True
    
    def switch_player(self):
        self.current_player = 'white' if self.current_player == 'black' else 'black'

    def count_pieces(self, player,board):
        count = 0
        for row in board:
            for col in row:
                if col == player:
                    count += 1
        return count

    def check_move(self, player):
        opponent = 'white' if player == 'black' else 'black'
        player_pieces = self.count_pieces(player,self.board)
        opponent_pieces = self.count_pieces(opponent,self.board)

        if player_pieces > opponent_pieces:
            winner = f"Player {player} wins!"
        else:
            winner = f"Player {opponent} wins!"
        
        tkinter.messagebox.showinfo("Game Ends", winner) # show message
        return True

    def computerMove(self):
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            depth = 1
        elif difficulty == "Intermediate":
            depth = 3
        else:
            depth = 5    

        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for move in self.getAllValidMoves("white", self.board):
            new_board = [row[:] for row in self.board]
            self.move(move[0], move[1],self.current_player,new_board, False)
            score = self.minimax(new_board, depth=depth, alpha=alpha, beta=beta, maximizingPlayer='white')
            if score > best_score:
                best_score = score
                best_move = move

        
        self.move(best_move[0],best_move[1],self.current_player,self.board, True)        
        return best_move


    def minimax(self, cur_board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.is_game_over(maximizingPlayer, cur_board):
            return self.util(maximizingPlayer,cur_board)

        if maximizingPlayer == 'white':
            maxEval = float('-inf')
            for move in self.getAllValidMoves('white',cur_board):
                new_board = [row[:] for row in cur_board]
                self.move(move[0], move[1],'white', new_board, False)
                eval = self.minimax(new_board, depth - 1, alpha, beta, 'black')
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for move in self.getAllValidMoves("black", cur_board):
                new_board = [row[:] for row in cur_board]
                self.move(move[0], move[1],'black',new_board, False)
                eval = self.minimax(new_board, depth - 1, alpha, beta, 'white')
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
        
    def util(self, player, board):
        player_pieces = self.count_pieces(player,board)
        opponent = 'white' if player == 'black' else 'black'
        opponent_pieces = self.count_pieces(opponent,board)
        return player_pieces - opponent_pieces
        
    def is_game_over(self ,player,board):
        return self.is_board_full(board) or not self.getAllValidMoves(player,board)    
    
    def is_win(self, player):
        opponent = 'white' if player == 'black' else 'black'
        player_pieces = self.count_pieces(player)
        opponent_pieces = self.count_pieces(opponent)
        return player_pieces > opponent_pieces
    
    def is_draw(self):
        return self.is_board_full(self.board) and not self.is_win('black') and not self.is_win('white')


    # logic for application
    def play(self):
        while True:
            # message to remind user of Difficulty
            if self.difficulty_var.get() == "":
                tkinter.messagebox.showerror("Error", "Pls Enter Difficulty first")
            
            moves = self.getAllValidMoves(self.current_player, self.board)

            # reset previous grey colors
            self.reset_button_colors()
            
            # Highlight valid moves on the GUI
            self.highlight_valid_moves()
            
            
            # Check if the current player has valid moves
            if not moves and not self.is_board_full(self.board):
                self.switch_player()
                test = self.getAllValidMoves(self.current_player, self.board)
                if test == []:
                    self.check_move(self.current_player)
                    break
                continue

            # Check if a player has run out of pieces
            if (self.current_player == 'black' and self.black_pieces_left == 0) or \
                    (self.current_player == 'white' and self.white_pieces_left == 0):
                self.check_move(self.current_player)
                break

            # Computer's turn
            if self.current_player == 'white':
                self.computerMove()
            else:
                # Wait for the player to make a move through GUI interaction
                self.player_move = tk.IntVar()  
                self.player_move.set(0)  

                # Wait for the player to click on a button
                self.root.wait_variable(self.player_move)

                # Update valid moves after the move is made
                self.valid_moves = self.getAllValidMoves(self.current_player, self.board)

                # Check if the game is over
                if self.is_board_full(self.board):
                    if self.is_win(self.current_player):
                        tkinter.messagebox.showinfo("Game Ends", f"Player {self.current_player} wins!")
                        break
                # Check if the game is draw
                if self.is_draw():
                    tkinter.messagebox.showinfo("Draw", "It's a draw!")
                    break
                    
            # update dashboard after each move
            self.update_human_pieces_label()
            self.update_computer_pieces_label()             
            self.update_human_left_label()
            self.update_computer_left_label()
       
            
            # Switch to the next player
            self.switch_player()



def main():
    root = tk.Tk()
    root.configure(bg="#24CA70")
    app = ctkApp(root)
    app.play()  
    root.mainloop()  
    
if __name__ == "__main__":
    main()
