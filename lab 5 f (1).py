import random

class GameBoard:
    def __init__(self):
        self.grid = [['-' for _ in range(3)] for _ in range(3)]
        self.active_symbol = 'X'
    
    def display(self):
        print("\n  0   1   2")
        for idx, line in enumerate(self.grid):
            print(f"{idx} {line[0]} | {line[1]} | {line[2]}")
            if idx < 2:
                print("  ---+---+---")
        print()
    
    def place_symbol(self, r, c):
        if self.grid[r][c] == '-':
            self.grid[r][c] = self.active_symbol
            self.active_symbol = 'O' if self.active_symbol == 'X' else 'X'
            return True
        return False
    
    def find_winner(self):
        # Check rows and columns
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != '-':
                return self.grid[i][0]
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != '-':
                return self.grid[0][i]
        
        # Check diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != '-':
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != '-':
            return self.grid[0][2]
        
        return None
    
    def is_full(self):
        for line in self.grid:
            if '-' in line:
                return False
        return True
    
    def get_empty_cells(self):
        empty = []
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == '-':
                    empty.append((i, j))
        return empty

class GameAgent:
    def __init__(self, mark, agent_name):
        self.mark = mark
        self.enemy = 'X' if mark == 'O' else 'O'
        self.agent_name = agent_name
    
    def select_position(self, board):
        empty_cells = board.get_empty_cells()
        
        # Try to win
        for cell in empty_cells:
            r, c = cell
            board.grid[r][c] = self.mark
            if board.find_winner() == self.mark:
                board.grid[r][c] = '-'
                return cell
            board.grid[r][c] = '-'
        
        # Block enemy win
        for cell in empty_cells:
            r, c = cell
            board.grid[r][c] = self.enemy
            if board.find_winner() == self.enemy:
                board.grid[r][c] = '-'
                return cell
            board.grid[r][c] = '-'
        
        # Center preference
        if board.grid[1][1] == '-':
            return (1, 1)
        
        # Corner positions
        corner_spots = [(0, 0), (0, 2), (2, 0), (2, 2)]
        open_corners = [spot for spot in corner_spots if board.grid[spot[0]][spot[1]] == '-']
        if open_corners:
            return random.choice(open_corners)
        
        # Side positions
        side_spots = [(0, 1), (1, 0), (1, 2), (2, 1)]
        open_sides = [spot for spot in side_spots if board.grid[spot[0]][spot[1]] == '-']
        if open_sides:
            return random.choice(open_sides)
        
        # Random selection
        return random.choice(empty_cells) if empty_cells else None

def play_game(game_id):
    board = GameBoard()
    player1 = GameAgent('X', 'Agent_X')
    player2 = GameAgent('O', 'Agent_O')
    
    print(f"\nMatch {game_id}: Agent_X vs Agent_O")
    
    turn_counter = 0
    while True:
        turn_counter += 1
        
        current_agent = player1 if board.active_symbol == 'X' else player2
        r, c = current_agent.select_position(board)
        board.place_symbol(r, c)
        
        print(f"Turn {turn_counter}: {board.grid[r][c]} ({current_agent.agent_name}) at position ({r}, {c})")
        board.display()
        
        winner = board.find_winner()
        if winner:
            winner_label = "Agent_X" if winner == 'X' else "Agent_O"
            print(f"{winner} ({winner_label}) WINS! Turns taken: {turn_counter}")
            return winner, turn_counter
        
        if board.is_full():
            print(f"DRAW! Turns taken: {turn_counter}")
            return 'Draw', turn_counter

def execute_series():
    print("TIC-TAC-TOE: 20 GAME SERIES ANALYSIS")
    
    match_records = []
    x_victories = 0
    o_victories = 0
    tied_games = 0
    x_turns_total = 0
    o_turns_total = 0
    
    for match_id in range(1, 21):
        result, turns = play_game(match_id)
        match_records.append((match_id, result, turns))
        
        if result == 'X':
            x_victories += 1
            x_turns_total += turns
        elif result == 'O':
            o_victories += 1
            o_turns_total += turns
        else:
            tied_games += 1
    
    # Display results
    print("\nRESULTS")
    print("=" * 40)
    print(f"Agent_X Wins: {x_victories} ({x_victories/20*100:.1f}%)")
    print(f"Agent_O Wins: {o_victories} ({o_victories/20*100:.1f}%)")
    print(f"Draws: {tied_games} ({tied_games/20*100:.1f}%)")
    
    if x_victories > 0:
        print(f"Agent_X average moves to win: {x_turns_total/x_victories:.1f}")
    if o_victories > 0:
        print(f"Agent_O average moves to win: {o_turns_total/o_victories:.1f}")

if __name__ == "__main__":
    execute_series()