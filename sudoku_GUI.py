import pygame

pygame.font.init()
screen = pygame.display.set_mode((500, 600)) # initialize window
pygame.display.set_caption("sudoku") # caption for window
image = pygame.image.load('icon.png') # icon for window
pygame.display.set_icon(image)
font = pygame.font.SysFont("Ariel", 50) # load fonts

x = 0
y = 0
off = 500 / 9
sol = 0

sudokuBoard =[[7, 6, 0, 0, 0, 9, 0, 1, 0],
              [8, 0, 0, 0, 0, 0, 7, 2, 4],
              [0, 0, 0, 7, 1, 4, 0, 0, 9],
              [4, 0, 6, 0, 0, 0, 3, 0, 2],
              [0, 7, 0, 4, 5, 6, 0, 0, 0],
              [0, 5, 1, 0, 0, 0, 0, 7, 6],
              [1, 0, 0, 2, 9, 0, 0, 4, 0],
              [2, 0, 7, 6, 3, 0, 1, 0, 0],
              [0, 9, 8, 0, 0, 5, 2, 0, 7]
              ]

##############

# get coordinates
def get_coordinates(position):
    global x
    global y
    x = position[0] / off
    y = position[1] / off


# draw board
def draw():
    # add some color
    for i in range(9):
        for j in range(9):
            if sudokuBoard[i][j] != 0:  # number is given
                pygame.draw.rect(screen, (51, 153, 255), (i * off, j * off, off + 1, off + 1))
    # draw vertical and horizontal lines
    for i in range(10):
        if i % 3 == 0:
            thickness = 8
        else:
            thickness = 2
        pygame.draw.line(screen, (0, 0, 0), (0, i * off), (500, i * off), thickness)  # horizontal
        pygame.draw.line(screen, (0, 0, 0), (i * off, 0), (i * off, 500), thickness)  # vertical
    # add given numbers
    for i in range(9):
        for j in range(9):
            if sudokuBoard[i][j] != 0:  # number is given
                text1 = font.render(str(sudokuBoard[i][j]), True, (0, 0, 0))
                screen.blit(text1, (i * off + 15, j * off + 15))


# check if number is valid
def is_valid(board, num, position):
    valid = True
    # check row
    for i in range(len(board[0])):
        if board[position[0]][i] == num:
            valid = False
    # check col
    for j in range(len(board[0])):
        if board[j][position[1]] == num:
            valid = False
    # check box
    row = position[0] // 3
    col = position[1] // 3
    for i in range(row * 3, row * 3 + 3):
        for j in range(col * 3, col * 3 + 3):
            if board[i][j] == num and (i, j) != num:
                valid = False
    return valid


def draw_num(val):
    text = font.render(str(val), True, (0, 0, 0))
    screen.blit(text, (x * off + 10, y * off + 15))


def find_empty_cell(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i,j
    return False


# solver
def solver(board):
    empty_cell = find_empty_cell(board)   
    if not empty_cell: # if no cell is free we are done
        return True
    row = empty_cell[0]
    col = empty_cell[1]
    for num in range(1, 10):  # try to assign value (1-9) to (row,col) and if valid, move to the next cell.
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            screen.fill((255, 255, 255))
            draw()
            pygame.display.update()
            pygame.time.delay(30)
            if solver(board):
                return True
            # if we reached here we fail to insert number to cell, then undo and send 'fail'(AKA False)
            board[row][col] = 0
            screen.fill((255, 255, 255))
            draw()
            pygame.display.update()
            pygame.time.delay(45)
    return False


# main function :
run = True
while run:
    # white background
    screen.fill((255, 255, 255))
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.K_ESCAPE:
            run = False
        # mouse or keyboard input:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sol = 1
            if event.key == pygame.K_ESCAPE:
                run = False
    if sol == 1:
        solver(sudokuBoard)
        draw()
        sol = 0
    pygame.display.update()
pygame.quit()
