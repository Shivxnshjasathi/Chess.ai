# Chess AI

A Python-based Chess AI that allows a human player to compete against a computer. The AI uses the minimax algorithm with alpha-beta pruning and quiescence search to determine the best move. The AI also incorporates piece-square tables to evaluate the board position for both sides.

## Features

- **Minimax Algorithm**: The AI uses a depth-limited minimax algorithm with alpha-beta pruning to efficiently search the game tree.
- **Quiescence Search**: Prevents "horizon effect" by continuing the search through only capture moves when the depth is zero.
- **Piece-Square Tables**: Assigns a score to each piece based on its position on the board, making the AI more positionally aware.
- **Exploration Rate**: Introduces a slight randomness to move ordering to prevent overly deterministic play and encourage exploration of different move sequences.
- **Human vs AI Mode**: Allows a human to play as White against the AI playing as Black.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/chess-ai.git
    cd chess-ai
    ```

2. Install the required dependencies:
    ```bash
    pip install python-chess
    ```

## How to Play

1. Run the game:
    ```bash
    python chess_ai.py
    ```

2. The game starts with an empty chessboard and asks you to input your move in standard chess notation (e.g., `e2e4`).

3. The AI will automatically respond after you make your move.

4. To quit the game, type `quit`.

5. The game will continue until checkmate, stalemate, or a draw is reached.

## Board Representation

The chessboard is represented in the console as an 8x8 grid, with the following notation:

- **Uppercase** letters represent White's pieces (e.g., `P` for pawn, `R` for rook).
- **Lowercase** letters represent Black's pieces (e.g., `p` for pawn, `r` for rook).
- **Dots (.)** represent empty squares.

Example:
```
8 r . b q k b n r
7 p p p p p p p p
6 . . . . . . . .
5 . . . . . . . .
4 . . . . . . . .
3 . . . . . . . .
2 P P P P P P P P
1 R N B Q K B N R
  a b c d e f g h
```

## AI Algorithm

The AI uses a combination of techniques to play effectively:

- **Minimax with Alpha-Beta Pruning**: The AI simulates moves ahead up to a certain depth and calculates the board evaluation score. It then chooses the move that minimizes the opponent's possible advantage.
  
- **Quiescence Search**: The AI continues evaluating beyond the usual depth in positions with potential captures, to avoid shortsighted moves.
  
- **Move Ordering**: Moves are evaluated and ordered based on previous game experience to improve search efficiency.

## Configuration

You can adjust the following AI settings:

- **Depth**: The search depth for the AI can be adjusted to control the difficulty level. By default, the depth is set to 3.
  
- **Exploration Rate**: This rate controls how often the AI explores different moves for variety. The default is 0.1, meaning 10% of moves may be chosen slightly at random.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [python-chess](https://python-chess.readthedocs.io/en/latest/) library for handling the chessboard and game rules.

## Documentation 

- https://shivxnshjasathi.github.io/Chess.ai/
