import random
import re

from numpy import broadcast_arrays
class Board:
    def __init__(self,dim_size,num_bombs): 
        # user defined parameterized constructor 
        self.num_bombs = num_bombs
        self.dim_size = dim_size
        self.dug = set() # if dig it (0,0) then self.dug = {0,0}
        self.board = self.make_new_board() # helper function to create the board 
        self.assign_values_to_board()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)]for _ in range(self.dim_size)] # make board of given size

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0,self.dim_size**2-1) # return a random number between 0 and size^2 of board
            row = loc//self.dim_size # gives th row of bomb
            col = loc%self.dim_size # gives the column of the bomb

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            bombs_planted +=1
        return board

    def assign_values_to_board(self):
        # this is done to give the a cell the no of bombs surrounding it
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r,c)

    def get_num_neighbouring_bombs(self,row,col):
        # run loop from row+1 to col+1 to get the all neighbouring cells in current cell of the board
        num_neighbouring_bombs = 0
        for r in range(max(0,row-1),min(self.dim_size-1,row+1)+1):
            for c in range(max(0,col-1),min(self.dim_size-1,col+1)+1):
                if r == row and c == col:
                    # no need to check the original location
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs +=1
        return num_neighbouring_bombs

    def dig(self,row,col):
        # dig at the location
        # if dug a bomb game over
        # if dug at location with neighbouring bombs finish dig
        # if dug at location with no neighbouring bombs recursively dig neighbors
        self.dug.add((row,col)) # keep track where we dig

        if self.board[row][col] == '*': # if a bomb return false
            return False
        elif self.board[row][col] > 0 : # if dig has neighbouring bombs which means that the dig is successful
            return True

        # if dig has no neighbouring bombs then we need to dig recursively
        for r in range(max(0,row-1),min(self.dim_size-1,row+1)+1):
            for c in range(max(0,col-1),min(self.dim_size-1,col+1)+1):
                if (r,c) in self.dug:
                    continue # no need to dig where already dug
                self.dig(r,c)
        return True      

    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep
           

        
def play(dim_size = 10,num_bombs = 10):
    # Step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)
    # Step 2: show the user the board and ask for where they want to dig
    # Step 3a: if location is a bomb, show game over message
    # Step 3b: if location is not a bomb, dig recursively until each square is at least
    #next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!
    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("where would you like dig ? Input as row,col:"))
        row,col = int(user_input[0]),int(user_input[-1])
        if row < 0 or row>=dim_size or col < 0 or col>=dim_size :
            print("Invalid location. Try again.")
            continue
        safe = board.dig(row,col)
        if safe == False:
            break
    
    if safe == True:
        print("Congo you won the game")
    else :
        print("Sorry Game :(")
        board.dug = [(r,c) for r in range(board.dim_size)for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__' :
    play()