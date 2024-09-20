import chess
import random

class ChessAI:
    def __init__(self, depth=3):
        self.depth = depth
        self.move_scores = {}
        self.move_history = []
        self.exploration_rate = 0.1

        # Piece-Square Tables (Positional score based on the location of each piece)
        self.piece_square_tables = {
            chess.PAWN: [
                0, 0, 0, 0, 0, 0, 0, 0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5, 5, 10, 25, 25, 10, 5, 5,
                0, 0, 0, 20, 20, 0, 0, 0,
                5, -5, -10, 0, 0, -10, -5, 5,
                5, 10, 10, -20, -20, 10, 10, 5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            chess.KNIGHT: [
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50
            ],
            chess.BISHOP: [
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -20, -10, -10, -10, -10, -10, -10, -20
            ],
            chess.ROOK: [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, 10, 10, 10, 10, 5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                0, 0, 0, 5, 5, 0, 0, 0
            ],
            chess.QUEEN: [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -5, 0, 5, 5, 5, 5, 0, -5,
                0, 0, 5, 5, 5, 5, 0, -5,
                -10, 5, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 0, 0, 0, 0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],
            chess.KING: [
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                20, 20, 0, 0, 0, 0, 20, 20,
                20, 30, 10, 0, 0, 10, 30, 20
            ]
        }

    def choose_move(self, board):
        legal_moves = list(board.legal_moves)
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        legal_moves = self.order_moves(board, legal_moves)

        for move in legal_moves:
            board.push(move)
            score = -self.quiescence_search(board, self.depth - 1, -beta, -alpha, not board.turn)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        self.update_move_scores(board, best_move, best_score)
        self.update_move_history(best_move)

        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def quiescence_search(self, board, depth, alpha, beta, maximizing_player):
        stand_pat = self.evaluate_board(board)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):  # Only search further for captures
                board.push(move)
                score = -self.quiescence_search(board, depth - 1, -beta, -alpha, not board.turn)
                board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha

    def evaluate_board(self, board):
        if board.is_checkmate():
            return -10000 if board.turn == chess.WHITE else 10000
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 300,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 0
        }

        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    score += value
                    score += self.piece_square_tables.get(piece.piece_type, [0]*64)[square]
                else:
                    score -= value
                    score -= self.piece_square_tables.get(piece.piece_type, [0]*64)[chess.square_mirror(square)]

        return score

    def order_moves(self, board, moves):
        def move_score(move):
            score = self.move_scores.get(move.uci(), 0)
            if random.random() < self.exploration_rate:
                score += random.uniform(-200, 200)
            return score
        return sorted(moves, key=lambda move: move_score(move), reverse=True)

    def update_move_scores(self, board, move, score):
        move_uci = move.uci()
        if move_uci not in self.move_scores:
            self.move_scores[move_uci] = score
        else:
            self.move_scores[move_uci] = (self.move_scores[move_uci] + score) / 2

    def update_move_history(self, move):
        self.move_history.append(move.uci())
        if len(self.move_history) > 5:
            self.move_history.pop(0)

def play_game():
    board = chess.Board()
    ai = ChessAI(depth=3)

    human_score = 0
    ai_score = 0

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print(board)
            move = input("Enter your move (e.g., e2e4) or 'quit' to exit: ")

            if move.lower() == "quit":
                print("You quit the game.")
                break

            try:
                board.push_san(move)
            except ValueError:
                print("Invalid move. Try again.")
                continue
        else:
            move = ai.choose_move(board)
            board.push(move)
            print(f"AI moved: {move}")

        current_score = ai.evaluate_board(board)
        if board.turn == chess.WHITE:
            human_score = current_score
        else:
            ai_score = current_score

        print(f"Current Score -> Human: {human_score} | AI: {ai_score}")

    if board.is_game_over():
        print(board)
        print("Game Over")
        print(f"Result: {board.result()}")

if __name__ == "__main__":
    play_game()
