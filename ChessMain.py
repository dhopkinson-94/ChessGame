"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
from Chess import ChessEngine

width = height = 512
dimension = 8 #dimensions of a chess board are 8*8
sq_size = height // dimension
max_fps = 15 #for animation later on
images = {}
pieces = ['wp','wB','wK','wQ','wN','wR','bp','bB','bK','bQ','bN','bR']
"""
Initialise a global dictionary of images. Called exactly once in the main
"""
def load_images():
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'),(sq_size,sq_size))
    #Note: we can access an image by saying 'images['wp']'

"""
The main driver for code. This will handle user input and update the graphics
"""

def main():
    p.init()
    screen = p.display.set_mode((width,height + 100))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    moveMade = False #flag variable for when a move is made
    print(gs.board)
    load_images() #only do this once, before the while loop
    running = True
    sq_selected = () #no square selected, keep track of the last click of the user (tuple (x , y))
    player_clicks = [] #keeps track of player clicks. contains two tuples [(x1, y,1),(x2, y2)]


    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  #(x, y) location of the mouse
                col = location[0]//sq_size
                row = location[1]//sq_size
                if sq_selected == (row, col):
                    sq_selected = () #deselct
                    player_clicks = [] #clear player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected) #append for both first and second clicks
                #was that the users second click
                if len(player_clicks) == 2:
                    move  = ChessEngine.Move(player_clicks[0],player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                       gs.make_move(move)
                       moveMade = True
                       sq_selected = () #reset user clicks
                       player_clicks = []
                    else:
                        player_clicks = [sq_selected]
            #Key hanlders
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undo_move()
                    moveMade = True

        if moveMade:
            valid_moves = gs.get_valid_moves()
            moveMade = False
        clock.tick(max_fps)
        p.display.flip()
        draw_game_state(screen, gs)

"""
Responsible for all graphics in current game state
"""
def draw_game_state(screen, gs):
    draw_board(screen) #draw squares on the board
    draw_info_box(screen) #draw rectangle at the bottom of the board for info
    draw_pieces(screen, gs.board) #draw pieces on top of those squares
    get_text(screen, gs)
    draw_player_options(screen, gs)



"""
Draw the squares on the board. Top left square is always light.
"""
def draw_board(screen):
    colors = [p.Color('white'), p.Color('dark green')]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen,color,p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

"""
draw pieces on the board using the current GameState.board
"""
def draw_pieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != '--':
                screen.blit(images[piece], p.Rect(c*sq_size,r*sq_size, sq_size,sq_size))


def draw_info_box(screen):
    color = p.Color('black')
    height = 100
    width = 512
    rects = ( 0,512, width, height)
    p.draw.rect(screen,color, rects)

def get_text(screen, gs):
    x = 20
    y = 530
    piece_taken = gs.pieces_taken
    movelog = gs.movelog
    p.display.set_caption('Show Text')
    font = p.font.Font('freesansbold.ttf', 15)
    piece = []
    if len(piece_taken) > 0:
        for i in piece_taken:
            piece.append(i)
        text = font.render(str(piece), True, 'white')
        textRect = text.get_rect()
        textRect.center = (x, y)
        textRect.left = x
        screen.blit(text, textRect)

    w = 570
    p.display.set_caption('Show Text')
    font = p.font.Font('freesansbold.ttf', 15)
    text = font.render(str(movelog), True, 'white')
    textRect = text.get_rect()
    textRect.center = (x, w)
    textRect.left = x
    screen.blit(text, textRect)


def draw_player_options(screen,gs):
    if not gs.movelog:
        x = 256
        y = 306
        rects = ( 170,300, width, height)


if __name__ == '__main__':
   main()




