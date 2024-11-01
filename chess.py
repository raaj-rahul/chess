import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (205, 133, 63)
LIGHT_BROWN = (222, 184, 135)
HIGHLIGHT_COLOR = (173, 216, 230)  # Light blue for selected piece

# Load images
PIECE_IMAGES = {}
PIECE_TYPES = ["pawn", "rook", "knight", "bishop", "queen", "king"]
PIECE_COLORS = ["white", "black"]

# Load the piece images from the images folder
for color in PIECE_COLORS:
    for piece in PIECE_TYPES:
        image_path = f"images/{color}_{piece}.png"
        if os.path.exists(image_path):  # Check if image exists
            PIECE_IMAGES[f"{color}_{piece}"] = pygame.transform.scale(pygame.image.load(image_path), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            print(f"Warning: Image file '{image_path}' not found.")

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Chessboard setup
def create_board():
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    for i in range(COLS):
        board[1][i] = "black_pawn"
        board[6][i] = "white_pawn"
    
    # Rooks
    board[0][0] = board[0][7] = "black_rook"
    board[7][0] = board[7][7] = "white_rook"
    # Knights
    board[0][1] = board[0][6] = "black_knight"
    board[7][1] = board[7][6] = "white_knight"
    # Bishops
    board[0][2] = board[0][5] = "black_bishop"
    board[7][2] = board[7][5] = "white_bishop"
    # Queens
    board[0][3] = "black_queen"
    board[7][3] = "white_queen"
    # Kings
    board[0][4] = "black_king"
    board[7][4] = "white_king"
    
    return board

# Draw board
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces on board
def draw_pieces(board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                screen.blit(PIECE_IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Highlight selected piece
def highlight_square(row, col):
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Check valid moves for a piece
def valid_moves(piece, row, col, board):
    moves = []
    color = piece.split("_")[0]
    piece_type = piece.split("_")[1]

    if piece_type == "pawn":
        direction = -1 if color == "white" else 1
        start_row = 6 if color == "white" else 1
        
        # Move forward
        if 0 <= row + direction < ROWS and board[row + direction][col] is None:
            moves.append((row + direction, col))
            # Double move from starting position
            if row == start_row and board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))
        
        # Captures
        if col - 1 >= 0 and 0 <= row + direction < ROWS and board[row + direction][col - 1] and board[row + direction][col - 1].split("_")[0] != color:
            moves.append((row + direction, col - 1))
        if col + 1 < COLS and 0 <= row + direction < ROWS and board[row + direction][col + 1] and board[row + direction][col + 1].split("_")[0] != color:
            moves.append((row + direction, col + 1))

    elif piece_type == "rook":
        for r in range(row + 1, ROWS):  # Down
            if board[r][col] is None:
                moves.append((r, col))
            else:
                if board[r][col].split("_")[0] != color:
                    moves.append((r, col))
                break
        for r in range(row - 1, -1, -1):  # Up
            if board[r][col] is None:
                moves.append((r, col))
            else:
                if board[r][col].split("_")[0] != color:
                    moves.append((r, col))
                break
        for c in range(col + 1, COLS):  # Right
            if board[row][c] is None:
                moves.append((row, c))
            else:
                if board[row][c].split("_")[0] != color:
                    moves.append((row, c))
                break
        for c in range(col - 1, -1, -1):  # Left
            if board[row][c] is None:
                moves.append((row, c))
            else:
                if board[row][c].split("_")[0] != color:
                    moves.append((row, c))
                break

    elif piece_type == "knight":
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if board[r][c] is None or board[r][c].split("_")[0] != color:
                    moves.append((r, c))

    elif piece_type == "bishop":
        for d in range(1, ROWS):  # Diagonal down-right
            r, c = row + d, col + d
            if r < ROWS and c < COLS:
                if board[r][c] is None:
                    moves.append((r, c))
                else:
                    if board[r][c].split("_")[0] != color:
                        moves.append((r, c))
                    break
            else:
                break
        for d in range(1, ROWS):  # Diagonal down-left
            r, c = row + d, col - d
            if r < ROWS and c >= 0:
                if board[r][c] is None:
                    moves.append((r, c))
                else:
                    if board[r][c].split("_")[0] != color:
                        moves.append((r, c))
                    break
            else:
                break
        for d in range(1, ROWS):  # Diagonal up-right
            r, c = row - d, col + d
            if r >= 0 and c < COLS:
                if board[r][c] is None:
                    moves.append((r, c))
                else:
                    if board[r][c].split("_")[0] != color:
                        moves.append((r, c))
                    break
            else:
                break
        for d in range(1, ROWS):  # Diagonal up-left
            r, c = row - d, col - d
            if r >= 0 and c >= 0:
                if board[r][c] is None:
                    moves.append((r, c))
                else:
                    if board[r][c].split("_")[0] != color:
                        moves.append((r, c))
                    break
            else:
                break

    elif piece_type == "queen":
        # Combine rook and bishop moves
        moves += valid_moves(f"{color}_rook", row, col, board)
        moves += valid_moves(f"{color}_bishop", row, col, board)

    elif piece_type == "king":
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if board[r][c] is None or board[r][c].split("_")[0] != color:
                    moves.append((r, c))

    return moves

# Main function
def main():
    clock = pygame.time.Clock()
    board = create_board()
    selected_piece = None
    selected_pos = None
    white_turn = True

    running = True
    while running:
        clock.tick(60)
        screen.fill(WHITE)
        draw_board()
        draw_pieces(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                piece = board[row][col]

                if selected_piece:
                    # Try to move the piece
                    if (row, col) in valid_moves(selected_piece, selected_pos[0], selected_pos[1], board):
                        board[row][col] = selected_piece
                        board[selected_pos[0]][selected_pos[1]] = None
                        white_turn = not white_turn  # Switch turns after a valid move
                        selected_piece = None
                    else:
                        selected_piece = None
                else:
                    # Select the piece
                    if piece and piece.split("_")[0] == ("white" if white_turn else "black"):
                        selected_piece = piece
                        selected_pos = (row, col)
                        highlight_square(row, col)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
