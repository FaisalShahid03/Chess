import pygame
from collections import deque
import argparse

pygame.init()

# Screen dimensions and grid size
WIDTH, HEIGHT = 1000, 750  # Increased window size
CHESSBOARD_SIZE = 540
ROWS, COLS = 8, 8
SQUARE_SIZE = CHESSBOARD_SIZE // COLS
WHITE, BEIGE, BROWN, GREEN, BLACK = (255, 255, 255), (240, 255, 230), (196, 164, 132), (0, 255, 0), (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
BUTTON_TEXT_COLOR = BLACK

# Load piece images (ensure these paths are correct)
PIECE_IMAGES = {
    "Pawn_white": pygame.image.load("white-pawn.png"),
    "Rook_white": pygame.image.load("white-rook.png"),
    "Knight_white": pygame.image.load("white-knight.png"),
    "Bishop_white": pygame.image.load("white-bishop.png"),
    "Queen_white": pygame.image.load("white-queen.png"),
    "King_white": pygame.image.load("white-king.png"),
    "Pawn_black": pygame.image.load("black-pawn.png"),
    "Rook_black": pygame.image.load("black-rook.png"),
    "Knight_black": pygame.image.load("black-knight.png"),
    "Bishop_black": pygame.image.load("black-bishop.png"),
    "Queen_black": pygame.image.load("black-queen.png"),
    "King_black": pygame.image.load("black-king.png"),
}


class LinkListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        if self.head == None:
            return True

    def getLastValue(self):
        currentNode = self.head
        while currentNode.next != None:
            currentNode = currentNode.next
        return currentNode.value

    def getFirstValue(self):
        currentNode = self.head
        return currentNode.value

    def displayList(self):
        currentNode = self.head
        while currentNode != None:
            print(str(currentNode.value) + "-->", end=" ")
            currentNode = currentNode.next

    def insertNode(self,index,value):
        nextNode = Node(value)
        if index == 0:
            nextNode.next = self.head
            self.head = nextNode
        else:
            current = self.head
            for i in range(index - 1):
                current = current.next
            nextNode.next = current.next

            current.next = nextNode
        return nextNode

    def insertAtHead(self,value):
        nextNode = Node(value)

        nextNode.next = self.head
        self.head = nextNode

        return nextNode

    def insertAtEnd(self,value):
        nextNode = LinkListNode(value)

        if self.head == None:
            self.head = nextNode
        else:

            currentNode = self.head
            while currentNode.next!=None:
                currentNode = currentNode.next
            currentNode.next = nextNode

        return nextNode

    def peekAtNode(self,index):

        current = self.head
        for i in range(index):
            current = current.next
        return  current.value

    def findNode(self,value):
        currentNode = self.head
        while currentNode != None:
            if currentNode.value == value:
                return True
            currentNode = currentNode.next
        return False

    def deleteNode(self,value):
        currentNode = self.head
        check = False
        while currentNode.next != None:
            if currentNode.next.value == value:
                check = True
                nextNode = currentNode.next.next
                currentNode.next = nextNode
            else:
                currentNode = currentNode.next
        return check

    def deleteFromStart(self):
        currentNode = self.head
        self.head = currentNode.next

    def deleteFromEnd(self):
        currentNode = self.head
        if currentNode == None:
            return None
        if currentNode.next == None:
            self.head = None
            return None
        while currentNode.next.next!= None:
            currentNode = currentNode.next
        currentNode.next = None

    def length(self):
        currentNode = self.head
        size = 0
        while currentNode!=None:
            size = size+1
            currentNode= currentNode.next
        return size
    

class myStack:
    def __init__(self):
        self.list = LinkList()
    def isEmpty(self):
        if self.list.isEmpty():
            return True
        return False

    def displayStack(self):
        print("[",end='-')
        for i in range(self.list.length()):
            print("(" + str(self.list.peekAtNode(i)) + ")",end='-')

    def PUSH(self, value):

            self.list.insertAtEnd(value)

    def POP(self):

        if self.isEmpty():
            print("Stack UnderFlow: Stack is Empty")
            return None
        else:
            popy = self.list.getLastValue()
            self.list.deleteFromEnd()

            return popy
        
    def length(self):

        return self.list.length()

    def Peek(self):

        if not self.isEmpty():
            return self.list.getLastValue()

class Player:
    def __init__(self, color):
        self.color = color  # 'white' or 'black'
        self.turn = False   # Whether it's this player's turn

    def toggle_turn(self):
        self.turn = not self.turn

class Node:
    def __init__(self, position, rect):
        self.position = position  # (row, col)
        self.piece = None         # Stores the piece on the square
        self.rect = rect          # Pygame rectangle for rendering
        self.image = None         # Image for the piece
        self.color = None
        
    def set_piece(self, piece, image,color):
        self.piece = piece
        self.image = pygame.transform.scale(image, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
        self.color = color

    def remove_piece(self):
        self.piece = None
        self.image = None
        self.color = None

class ChessGraph:
    def __init__(self):
        self.nodes = {}  # Dictionary to hold nodes by position
        self.create_chessboard()
        self.setup_pieces()
        self.king_positions = {'white': (7, 4), 'black': (0, 4)}
        self.players = {'white': Player('white'), 'black': Player('black')} 
        self.players['white'].turn = True # White starts the game
        self.move_history = myStack()
        self.font = pygame.font.SysFont("Arial", 24)  # Specify a font explicitly
        self.white_timer = 300  # White player starts with 5 minutes (300 seconds)
        self.black_timer = 300  # Black player starts with 5 minutes (300 seconds)
        self.last_time = pygame.time.get_ticks()  # Track the last frame's time


        
        self.captured_white_pieces = [] 
        self.captured_black_pieces = []
        
    def create_chessboard(self):
        for row in range(ROWS):
            for col in range(COLS):
                position = (row, col)
                rect = pygame.Rect(col * SQUARE_SIZE + 80, row * SQUARE_SIZE + 80, SQUARE_SIZE, SQUARE_SIZE)  # Offset for border
                self.nodes[position] = Node(position, rect)

    def setup_pieces(self):
        # Set up pawns
        for col in range(COLS):
            self.nodes[(1, col)].set_piece("Pawn_black", PIECE_IMAGES["Pawn_black"],"black")
            self.nodes[(6, col)].set_piece("Pawn_white", PIECE_IMAGES["Pawn_white"],"white")

        # Set up rooks
        self.nodes[(0, 0)].set_piece("Rook_black", PIECE_IMAGES["Rook_black"],"black")
        self.nodes[(0, 7)].set_piece("Rook_black", PIECE_IMAGES["Rook_black"],"black")
        self.nodes[(7, 0)].set_piece("Rook_white", PIECE_IMAGES["Rook_white"],"white")
        self.nodes[(7, 7)].set_piece("Rook_white", PIECE_IMAGES["Rook_white"],"white")

        # Set up knights
        self.nodes[(0, 1)].set_piece("Knight_black", PIECE_IMAGES["Knight_black"],"black")
        self.nodes[(0, 6)].set_piece("Knight_black", PIECE_IMAGES["Knight_black"],"black")
        self.nodes[(7, 1)].set_piece("Knight_white", PIECE_IMAGES["Knight_white"],"white")
        self.nodes[(7, 6)].set_piece("Knight_white", PIECE_IMAGES["Knight_white"],"white")

        # Set up bishops
        self.nodes[(0, 2)].set_piece("Bishop_black", PIECE_IMAGES["Bishop_black"],"black")
        self.nodes[(0, 5)].set_piece("Bishop_black", PIECE_IMAGES["Bishop_black"],"black")
        self.nodes[(7, 2)].set_piece("Bishop_white", PIECE_IMAGES["Bishop_white"],"white")
        self.nodes[(7, 5)].set_piece("Bishop_white", PIECE_IMAGES["Bishop_white"],"white")

        # Set up queens
        self.nodes[(0, 3)].set_piece("Queen_black", PIECE_IMAGES["Queen_black"],"black")
        self.nodes[(7, 3)].set_piece("Queen_white", PIECE_IMAGES["Queen_white"],"white")

        # Set up kings
        self.nodes[(0, 4)].set_piece("King_black", PIECE_IMAGES["King_black"],"black")
        self.nodes[(7, 4)].set_piece("King_white", PIECE_IMAGES["King_white"],"white")


    def is_in_check(self, player_color):
        """Check if the player's king is in check."""
        opponent_color = 'black' if player_color == 'white' else 'white'
        king_pos = self.king_positions[player_color]
        
        # Check if any of the opponent's moves can capture the king
        for pos, node in self.nodes.items():
            if node.color == opponent_color:
                if "Pawn" in node.piece:
                    opponent_moves = self.get_valid_pawn_moves_bfs(pos)
                elif "Knight" in node.piece:
                    opponent_moves = self.get_valid_knight_moves_bfs(pos)
                elif "Rook" in node.piece:
                    opponent_moves = self.get_valid_rook_moves_bfs(pos)
                elif "Bishop" in node.piece:
                    opponent_moves = self.get_valid_bishop_moves_bfs(pos)
                elif "Queen" in node.piece:
                    opponent_moves = self.get_valid_queen_moves_bfs(pos)
                elif "King" in node.piece:
                    opponent_moves = self.get_valid_king_moves_bfs(pos)
                
                if king_pos in opponent_moves:
                    return True
        return False
    
    def update_valid_moves(self):
        """Recalculate valid moves for all pieces after a move."""
        for pos, node in self.nodes.items():
            if node.piece:
                piece = node.piece
                valid_moves = []
                if "Pawn" in piece:
                    valid_moves = self.get_valid_pawn_moves_bfs(pos)
                elif "Knight" in piece:
                    valid_moves = self.get_valid_knight_moves_bfs(pos)
                elif "Rook" in piece:
                    valid_moves = self.get_valid_rook_moves_bfs(pos)
                elif "Bishop" in piece:
                    valid_moves = self.get_valid_bishop_moves_bfs(pos)
                elif "Queen" in piece:
                    valid_moves = self.get_valid_queen_moves_bfs(pos)
                elif "King" in piece:
                    valid_moves = self.get_valid_king_moves_bfs(pos)
                node.valid_moves = valid_moves  # Store the valid moves for the piece


    def move_piece(self, source, destination):
        if source in self.nodes and destination in self.nodes:
            src_node = self.nodes[source]
            dest_node = self.nodes[destination]

            if src_node.piece:
                player = 'white' if src_node.color == 'white' else 'black'
                if self.players[player].turn:
                    print(f"Moving piece: {src_node.piece} from {source} to {destination}")
                    print(f"Player: {player}")

                    # Temporarily store the original state
                    original_state = (
                        (source, src_node.piece, src_node.image, src_node.color),
                        (destination, dest_node.piece, dest_node.image, dest_node.color),
                        self.king_positions.copy(),
                        player,
                        self.captured_white_pieces.copy(),
                        self.captured_black_pieces.copy(),
                    )
                    self.move_history.PUSH(original_state)  # Push the state onto the stack

                    # Move the piece and update the king's position if needed
                    if src_node.piece and "King" in src_node.piece:
                        self.king_positions[src_node.color] = destination

                    # Simulate the move
                    captured_piece = None
                    if dest_node.piece:
                        captured_piece = dest_node.piece
                        if dest_node.color == 'white':
                            self.captured_white_pieces.append(dest_node.piece)
                        else:
                            self.captured_black_pieces.append(dest_node.piece)

                    # Handle en passant capture
                    if "Pawn" in src_node.piece and abs(source[0] - destination[0]) == 1 and abs(source[1] - destination[1]) == 1:
                        if not dest_node.piece:  # The destination is empty, indicating an en passant capture
                            captured_pos = (source[0], destination[1])
                            captured_node = self.nodes[captured_pos]
                            captured_piece = captured_node.piece
                            captured_node.remove_piece()
                            if captured_node.color == 'white':
                                self.captured_white_pieces.append(captured_piece)
                            else:
                                self.captured_black_pieces.append(captured_piece)

                    dest_node.set_piece(src_node.piece, src_node.image, src_node.color)
                    src_node.remove_piece()

                    # Check for pawn promotion 
                    if dest_node.piece and "Pawn" in dest_node.piece and (destination[0] == 0 or destination[0] == 7):
                        self.promote_pawn(destination, player)
                    # Recalculate valid moves after the move is made
                    self.update_valid_moves()

                    # Check if the current player's king is in check
                    if self.is_in_check(player):
                        print(f"Check! {player}'s king is in check.")
                    # Check if the move left the player in check
                    if self.is_in_check(player):
                        print(f"Invalid move, {player} is in check!")
                        # Restore the original state
                        src_node.set_piece(original_state[0][1], original_state[0][2], original_state[0][3])
                        if original_state[1][1]:
                            dest_node.set_piece(original_state[1][1], original_state[1][2], original_state[1][3])
                        else:
                            dest_node.remove_piece()

                        if captured_piece:
                            if dest_node.color == 'white':
                                self.captured_white_pieces.remove(captured_piece)
                            else:
                                self.captured_black_pieces.remove(captured_piece)

                        if src_node.piece and "King" in src_node.piece:
                            self.king_positions[src_node.color] = source

                        self.move_history.POP()  # Remove the invalid move state from the stack
                        return

                        
                    # Toggle turn
                    self.players[player].toggle_turn()
                    self.players['white' if player == 'black' else 'black'].toggle_turn()

                    # # Check for check or checkmate
                    # opponent = 'white' if player == 'black' else 'black'
                    # if self.is_checkmate(opponent):
                    #     print(f"Checkmate! {player} wins!")
                    # elif self.is_in_check(opponent):
                    #     print(f"Check! {player} has the opponent in check.")
                else:
                    print(f"It's not {player}'s turn.")
            else:
                print(f"No piece at {source} to move.")

    def promote_pawn(self, position, player_color):
        """Promotes a pawn to a queen, rook, bishop, or knight based on player's choice."""
        promotion_choices = ['Queen', 'Rook', 'Bishop', 'Knight']
        print("Choose promotion piece: ")
        for i, piece in enumerate(promotion_choices):
            print(f"{i + 1}: {piece}")

        # Simulating player input; in a real game, you would get actual input from the player
        choice = int(input("Enter the number corresponding to your choice: ")) - 1
        if choice < 0 or choice >= len(promotion_choices):
            print("Invalid choice. Defaulting to Queen.")
            choice = 0  # Default to Queen

        promotion_piece = promotion_choices[choice]
        piece_image = self.get_piece_image(promotion_piece, player_color)

        # Promote the pawn
        self.nodes[position].set_piece(f'{promotion_piece}_{player_color}', piece_image, player_color)
        print(f"Pawn promoted to {promotion_piece} at {position} for {player_color} player")

    def get_piece_image(self, piece, color):
        """Helper function to get the image for a piece."""
        return pygame.image.load(f'{color}-{piece}.png')  # Adjust the path as needed



    def undo_move(self):
        if self.move_history.isEmpty():
            print("No moves to undo.")
            return

        # Pop the last move from the stack
        last_state = self.move_history.POP()
        src_state, dest_state, last_king_positions, last_player, last_captured_white, last_captured_black = last_state

        # Restore the source and destination nodes
        src_pos, src_piece, src_image, src_color = src_state
        dest_pos, dest_piece, dest_image, dest_color = dest_state

        self.nodes[src_pos].set_piece(src_piece, src_image, src_color)
        if dest_piece:
            self.nodes[dest_pos].set_piece(dest_piece, dest_image, dest_color)
        else:
            self.nodes[dest_pos].remove_piece()

        # Restore the king positions
        self.king_positions = last_king_positions

        # Restore the captured pieces
        self.captured_white_pieces = last_captured_white
        self.captured_black_pieces = last_captured_black

        # Toggle turn back
        self.players[last_player].toggle_turn()
        self.players['white' if last_player == 'black' else 'black'].toggle_turn()


    
    def draw_board(self, screen, valid_moves=None):
    # Draw border
        pygame.draw.rect(screen, BLACK, (80, 80, CHESSBOARD_SIZE, CHESSBOARD_SIZE), 5)

        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BROWN
                pygame.draw.rect(screen, color, self.nodes[(row, col)].rect)

                # Draw piece image if it exists
                if self.nodes[(row, col)].image:
                    piece_color = self.nodes[(row, col)].color
                    piece_name = self.nodes[(row, col)].piece

                    if "King" in piece_name:
                        king_position = self.nodes[(row, col)].position
                        if (piece_color == 'white' and self.is_in_check('white')) or (piece_color == 'black' and self.is_in_check('black')):
                            pygame.draw.rect(screen, (255, 0, 0), self.nodes[(row, col)].rect)  # Red background for king in check
                            screen.blit(self.nodes[(row, col)].image, (col * SQUARE_SIZE + 85, row * SQUARE_SIZE + 85))
                            continue

                    screen.blit(self.nodes[(row, col)].image, (col * SQUARE_SIZE + 85, row * SQUARE_SIZE + 85))

                # Highlight valid moves
                if valid_moves and (row, col) in valid_moves:
                    pygame.draw.rect(screen, GREEN, self.nodes[(row, col)].rect, 5)

        # Draw ranks and files outside the board
        font = pygame.font.SysFont(None, 32)
        for row in range(ROWS):
            rank_text = font.render(str(8 - row), True, BLACK)
            screen.blit(rank_text, (50, row * SQUARE_SIZE + 100))

        for col in range(COLS):
            file_text = font.render(chr(ord('a') + col), True, BLACK)
            screen.blit(file_text, (col * SQUARE_SIZE + 100, CHESSBOARD_SIZE + 90))
            
    def draw_player_names(self, screen, player1_name, player2_name):
        """Draw player names above and below the chessboard."""
        # Render names
        player1_text = self.font.render(player1_name, True, BLACK)
        player2_text = self.font.render(player2_name, True, BLACK)

        # Draw names on the screen
        screen.blit(player1_text, (CHESSBOARD_SIZE // 2 - player1_text.get_width() // 2 + 80, 70))
        screen.blit(player2_text, (CHESSBOARD_SIZE // 2 - player2_text.get_width() // 2 + 80, CHESSBOARD_SIZE + 110))

    def load_icons(self):
        """Load icons for buttons."""
        self.undo_icon = pygame.image.load("undo-icon.png")  # Replace with your undo icon file
        self.home_icon = pygame.image.load("Images/home-icon.png")  # Replace with your home icon file
        self.undo_icon = pygame.transform.scale(self.undo_icon, (50, 50))
        self.home_icon = pygame.transform.scale(self.home_icon, (50, 50))

    
        
    def handle_buttons(self, event):
        """Handle button clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for button, action in self.buttons:
                if button.collidepoint(mouse_pos):
                    if action == "undo":
                        self.undo_move()


    def get_valid_knight_moves_bfs(self, position):
        """Calculate valid moves for a Knight from the given position using BFS."""
        moves = []
        row, col = position
        potential_moves = [
            (row - 2, col - 1), (row - 2, col + 1), (row + 2, col - 1), (row + 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2), (row + 1, col - 2), (row + 1, col + 2)
        ]

        current_piece_color = self.nodes[position].color  # Color of the Knight at the current position

        for r, c in potential_moves:
            if 0 <= r < ROWS and 0 <= c < COLS:
                target_node = self.nodes[(r, c)]
                target_piece_color = target_node.color

                # Check if the square is empty or occupied by an enemy piece
                if not target_node.piece or target_piece_color != current_piece_color:
                    moves.append((r, c))

        return moves
    
    

    def get_valid_rook_moves_bfs(self, position):
        """Calculate valid moves for a Rook using BFS."""
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        row, col = position
        current_piece_color = self.nodes[position].color  # Color of the Rook at the current position

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < ROWS and 0 <= c < COLS:
                target_node = self.nodes[(r, c)]
                target_piece = target_node.piece
                target_piece_color = target_node.color  # Color of the piece at the target square

                # If there's a piece on the target square
                if target_piece:
                    if target_piece_color != current_piece_color:
                        moves.append((r, c))  # Valid move if the piece is of a different color (enemy piece)
                    break  # Stop if a piece blocks further movement
                moves.append((r, c))  # Add the square if it's empty
                r, c = r + dr, c + dc

        return moves


    def get_valid_bishop_moves_bfs(self, position):
        """Calculate valid moves for a Bishop using BFS."""
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        row, col = position
        current_piece_color = self.nodes[position].color  # Color of the Bishop at the current position

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < ROWS and 0 <= c < COLS:
                target_node = self.nodes[(r, c)]
                target_piece = target_node.piece
                target_piece_color = target_node.color  # Color of the piece at the target square

                # If there's a piece on the target square
                if target_piece:
                    if target_piece_color != current_piece_color:
                        moves.append((r, c))  # Valid capture if it's an enemy piece
                    break  # Stop if a piece blocks further movement
                moves.append((r, c))  # Add the square if it's empty
                r, c = r + dr, c + dc

        return moves


    def get_valid_queen_moves_bfs(self, position):
        """Calculate valid moves for a Queen by combining Rook and Bishop moves."""
        return self.get_valid_rook_moves_bfs(position) + self.get_valid_bishop_moves_bfs(position)


    def get_valid_king_moves_bfs(self, position):
        """Calculate valid moves for a King using BFS."""
        moves = []
        row, col = position
        current_piece_color = self.nodes[position].color  # Color of the King at the current position
        potential_moves = [
            (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1),
            (row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)
        ]

        for r, c in potential_moves:
            if 0 <= r < ROWS and 0 <= c < COLS:
                target_node = self.nodes[(r, c)]
                target_piece = target_node.piece
                target_piece_color = target_node.color  # Color of the piece at the target square

                # Check if it's an empty square or an enemy piece
                if not target_piece or target_piece_color != current_piece_color:
                    moves.append((r, c))

        return moves


    def get_valid_pawn_moves_bfs(self, position):
        """Calculate valid moves for a Pawn using BFS."""
        moves = []
        row, col = position
        current_piece_color = self.nodes[position].color  # Color of the Pawn at the current position
        direction = -1 if current_piece_color == "white" else 1
        start_row = 6 if current_piece_color == "white" else 1
        en_passant_row = 3 if current_piece_color == "white" else 4

        # Move forward one square
        if 0 <= row + direction < ROWS and not self.nodes[(row + direction, col)].piece:
            moves.append((row + direction, col))

            # Move forward two squares from the starting position
            if row == start_row and not self.nodes[(row + 2 * direction, col)].piece:
                moves.append((row + 2 * direction, col))

        # Capture diagonally
        for dc in [-1, 1]:
            if 0 <= col + dc < COLS and 0 <= row + direction < ROWS:
                target_piece = self.nodes[(row + direction, col + dc)].piece
                target_piece_color = self.nodes[(row + direction, col + dc)].color  # Color of the target piece
                if target_piece and target_piece_color != current_piece_color:
                    moves.append((row + direction, col + dc))  # Valid capture

        # En passant capture
        if row == en_passant_row:
            for dc in [-1, 1]:
                if 0 <= col + dc < COLS:
                    target_position = (row, col + dc)
                    target_node = self.nodes[target_position]
                    if target_node.piece and target_node.color != current_piece_color and "Pawn" in target_node.piece:
                        # Check the last move to see if it was a pawn moving two squares forward
                        last_move = self.move_history.Peek() if not self.move_history.isEmpty() else None
                        if last_move:
                            src_last_move, dest_last_move, _, _, _, _ = last_move  # Adjusting to match the stored state
                            src_pos, src_piece, src_image, src_color = src_last_move
                            dest_pos, dest_piece, dest_image, dest_color = dest_last_move
                            src_row, src_col = src_pos
                            dest_row, dest_col = dest_pos
                            if abs(src_row - dest_row) == 2 and (dest_row, dest_col) == target_position:
                                moves.append((row + direction, col + dc))  # En passant capture

        return moves
    def draw_timers(self, screen):
        """Draw the timers and time bars for each player."""
        # Timer dimensions
        
        timer_width, timer_height = 200, 30
        margin = 20
        bar_length = 200
        bar_height = 20

        # Black Timer (at the top)
        pygame.draw.rect(screen, WHITE, (WIDTH - timer_width - margin -100, margin + 5, timer_width - 10, timer_height - 10))
        black_time_text = self.font.render(f"Black Time Left: {int(self.black_timer)}s", True, BLACK)
        screen.blit(black_time_text, (WIDTH - timer_width - margin -100, margin + 50))

        # Black Time Bar (below the black timer)
        pygame.draw.rect(screen, BEIGE, (WIDTH - bar_length - margin-100, margin + timer_height + 55, bar_length, bar_height))
        pygame.draw.rect(screen, GREEN, (WIDTH - bar_length - margin-100, margin + timer_height + 55,
                                        int((self.black_timer / 300) * bar_length), bar_height))

        # White Timer (at the bottom)
        pygame.draw.rect(screen, WHITE, (WIDTH - timer_width - margin -100, HEIGHT - timer_height - margin + 5, timer_width - 10, timer_height - 10))
        white_time_text = self.font.render(f"White Time Left: {int(self.white_timer)}s", True, BLACK)
        screen.blit(white_time_text, (WIDTH - timer_width - margin -100, HEIGHT - timer_height - margin -90))

        # White Time Bar (above the white timer)
        pygame.draw.rect(screen, BEIGE, (WIDTH - bar_length - margin-100, HEIGHT - timer_height - margin - bar_height - 10, bar_length, bar_height))
        pygame.draw.rect(screen, GREEN, (WIDTH - bar_length - margin-100, HEIGHT - timer_height - margin - bar_height - 100,
                                        int((self.white_timer / 300) * bar_length), bar_height))

        
    def update_timers(self):
        """Update the timer for the current player."""
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_time) / 1000  # Convert milliseconds to seconds
        self.last_time = current_time

        if self.players['white'].turn:
            self.white_timer = max(0, self.white_timer - elapsed)
        elif self.players['black'].turn:
            self.black_timer = max(0, self.black_timer - elapsed)

        # Check if time runs out
        if self.white_timer == 0:
            print("Time's up! Black wins!")
            return "black_wins"
        elif self.black_timer == 0:
            print("Time's up! White wins!")
            return "white_wins"

        return None





def draw_captured_pieces(screen, captured_white_pieces, captured_black_pieces):
    # Display captured white pieces at the bottom right
    for index, piece in enumerate(captured_white_pieces):
        image = PIECE_IMAGES[piece]
        scaled_image = pygame.transform.scale(image, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
        screen.blit(scaled_image, (CHESSBOARD_SIZE + 100 + (index % 8) * 30, HEIGHT - 180 - (index // 8) * 30))

    # Display captured black pieces at the top right
    for index, piece in enumerate(captured_black_pieces):
        image = PIECE_IMAGES[piece]
        scaled_image = pygame.transform.scale(image, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
        screen.blit(scaled_image, (CHESSBOARD_SIZE + 100 + (index % 8) * 30, 30 + (index // 8) * 30))

def draw_buttons(screen):
        """Draw Undo and Home buttons with icons on the given screen."""
        # Load and scale the icons
        font = pygame.font.Font(None, 36)

        # Home button
        home_rect = pygame.Rect(750, 100, 150, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, home_rect)
        home_text = font.render("Home", True, BUTTON_TEXT_COLOR)
        screen.blit(home_text, (home_rect.x + 50, home_rect.y + 10))

        # Undo button
        undo_rect = pygame.Rect(750, 200, 150, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, undo_rect)
        undo_text = font.render("Undo", True, BUTTON_TEXT_COLOR)
        screen.blit(undo_text, (undo_rect.x + 50, undo_rect.y + 10))

        return home_rect, undo_rect
        


def main(player1="Player 1", player2="Player 2", mode=0):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")

    chess_graph = ChessGraph()

    selected_piece = None
    valid_moves = []

    print(f"Game started with {player1} and {player2}. Mode: {'Human vs Human' if mode == 0 else 'Human vs AI'}")

    running = True
    while running:
        # Update timers
        result = chess_graph.update_timers()
        if result == "white_wins" or result == "black_wins":
            running = False  # End the game
            print(f"Game Over: {result.replace('_', ' ').capitalize()}")
            return result

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = (x - 80) // SQUARE_SIZE, (y - 80) // SQUARE_SIZE

                # Handle button clicks
                home_rect, undo_rect = draw_buttons(screen)
                if home_rect.collidepoint(x, y):
                    print("Home button clicked")
                    running = False  # Exit to return to the main menu
                    return "home"  # Return "home" as a signal to go back to main menu
                elif undo_rect.collidepoint(x, y):
                    print("Undo button clicked")
                    chess_graph.undo_move()

                # Handle chessboard interactions
                if 0 <= col < COLS and 0 <= row < ROWS:
                    clicked_position = (row, col)
                    piece = chess_graph.nodes[clicked_position].piece
                    piece_color = chess_graph.nodes[clicked_position].color
                    player = 'white' if piece_color == 'white' else 'black'

                    if selected_piece is None:
                        if piece:
                            if chess_graph.players[player].turn:
                                selected_piece = clicked_position
                                if "Pawn" in piece:
                                    valid_moves = chess_graph.get_valid_pawn_moves_bfs(clicked_position)
                                elif "Knight" in piece:
                                    valid_moves = chess_graph.get_valid_knight_moves_bfs(clicked_position)
                                elif "Rook" in piece:
                                    valid_moves = chess_graph.get_valid_rook_moves_bfs(clicked_position)
                                elif "Bishop" in piece:
                                    valid_moves = chess_graph.get_valid_bishop_moves_bfs(clicked_position)
                                elif "Queen" in piece:
                                    valid_moves = chess_graph.get_valid_queen_moves_bfs(clicked_position)
                                elif "King" in piece:
                                    valid_moves = chess_graph.get_valid_king_moves_bfs(clicked_position)
                            else:
                                print(f"It's not {player}'s turn.")
                    elif selected_piece == clicked_position:
                        selected_piece = None
                        valid_moves = []
                    else:
                        if clicked_position in valid_moves:
                            chess_graph.move_piece(selected_piece, clicked_position)

                            # Check for pawn promotion
                            if chess_graph.nodes[clicked_position].piece and "Pawn" in chess_graph.nodes[clicked_position].piece:
                                if clicked_position[0] == 0 or clicked_position[0] == 7:
                                    chess_graph.promote_pawn(clicked_position)

                            selected_piece = None
                            valid_moves = []

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:  # Press 'u' to undo the last move
                    chess_graph.undo_move()

        # Draw everything
        screen.fill(WHITE)

        # Draw border around the chessboard
        border_thickness = 5
        pygame.draw.rect(
            screen, BLACK, 
            (80 - border_thickness, 80 - border_thickness, CHESSBOARD_SIZE + 2 * border_thickness, CHESSBOARD_SIZE + 2 * border_thickness)
        )
        pygame.draw.rect(
            screen, WHITE, 
            (80, 80, CHESSBOARD_SIZE, CHESSBOARD_SIZE)
        )

        chess_graph.draw_board(screen, valid_moves)
        draw_captured_pieces(screen, chess_graph.captured_white_pieces, chess_graph.captured_black_pieces)
        chess_graph.draw_player_names(screen, player1, player2)
        chess_graph.draw_timers(screen)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess Game")
    parser.add_argument("--player1", type=str, default="Player 1", help="Name of Player 1")
    parser.add_argument("--player2", type=str, default="Player 2", help="Name of Player 2")
    parser.add_argument("--mode", type=int, choices=[0, 1], default=0, help="Game mode: 0 for Human vs Human, 1 for Human vs AI")
    args = parser.parse_args()

    main(player1=args.player1, player2=args.player2, mode=args.mode)
