# ChessRush ♟️

A fully-featured chess game built with Python and Pygame, offering multiple time controls, elegant UI themes, and complete chess rules implementation.

## Features

### Game Modes
- **Bullet Chess**: 1 min, 1|1, 2|1
- **Blitz Chess**: 3 min, 3|2, 5 min
- **Rapid Chess**: 10 min, 15|10, 30 min

### Complete Chess Rules
- All standard piece movements (Pawns, Knights, Bishops, Rooks, Queens, Kings)
- Special moves: Castling (kingside and queenside), En Passant
- Pawn promotion (automatically promotes to Queen)
- Check, checkmate, and stalemate detection
- Move validation to prevent illegal moves
- Visual indicators for possible moves and captures

### Customization
- 4 different piece sets to choose from
- 5 board color themes:
  - Classical (tan/brown)
  - Sky Blue
  - Green
  - Gray
  - Pink

### UI Features
- Elegant main menu with logo
- Time control selection interface
- Appearance customization screen
- Live game timer with turn indicator
- End game banner showing results
- Move highlighting and possible move indicators
- Check visualization with arrows
- Sound effects for moves, captures, checks, and game end

### Game Recording
- Automatic PGN (Portable Game Notation) file generation
- Records all moves in standard chess notation
- Saves game results

## Installation

### Requirements
- Python 3.7+

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/chessrush.git
cd chessrush

# Install dependencies
pip install pygame

# Run the game
python main.py
```

## Project Structure

```
chessrush/
│
├── main.py                 # Entry point
├── game_save.txt          # PGN game recording file
│
├── classes/
│   ├── game.py            # Main game logic and state management
│   ├── pieces.py          # Chess piece classes (Pawn, Knight, Bishop, etc.)
│   ├── interface.py       # UI components (menus, timers, banners)
│   └── bord.py            # Board class (currently unused)
│
├── utils/
│   ├── constante.py       # Constants (colors, board layouts, time controls)
│   └── functions.py       # Helper functions (move validation, notation, etc.)
│
└── assets/
    ├── pieces/            # Default piece set images
    ├── pieces_2/          # Alternative piece sets
    ├── pieces_3/
    ├── pieces_4/
    ├── sounds/            # Sound effects
    │   ├── game-start.mp3
    │   ├── game-end.mp3
    │   ├── move-self.mp3
    │   ├── move-check.mp3
    │   ├── capture.mp3
    │   ├── castle.mp3
    │   └── illegal.mp3
    ├── ChessRush.png      # Game logo
    ├── white-avatar.png   # Player avatars
    ├── black-avatar.png
    └── icon-*.png         # UI icons
```

## How to Play

1. **Launch the game** - Run `python main.py`
2. **Select time control** - Choose from Bullet, Blitz, or Rapid modes
3. **Customize appearance** - Select your preferred pieces and board colors
4. **Play chess** - Click to select a piece, then click the destination square
5. **View results** - After the game ends, see the winner and choose to rematch or quit

### Controls
- **Mouse Click**: Select and move pieces
- **ESC**: Return to previous menu / Exit game
- **Visual Indicators**:
  - Yellow highlight: Selected piece
  - Small dots: Valid move destinations
  - Red circles: Capture opportunities
  - Red square: King in check

## Game Rules Implementation

### Move Validation
- Legal move checking for all piece types
- Path obstruction detection for sliding pieces
- Turn-based move enforcement
- King safety validation (no moves that leave king in check)

### Special Moves
- **Castling**: Available when king and rook haven't moved, path is clear, and king isn't in/through check
- **En Passant**: Captures opposing pawn that just moved two squares forward
- **Pawn Promotion**: Pawns reaching the opposite end automatically promote to Queens

### Game End Conditions
- **Checkmate**: King is in check with no legal moves
- **Stalemate**: No legal moves available but king not in check
- **Time Out**: Player's clock reaches zero
- **Insufficient Material**: Kings only, King+Bishop, King+Knight, or King+Bishop vs King+Bishop (same color)

## PGN Output

Games are automatically saved in `game_save.txt` using standard PGN format:

```
[Event ""]
[Site ""]
[Date ""]
[Round ""]
[White "Player_1"]
[Black "Player_2"]
[Result "1-0"]
[FEN "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 ...
```

## Technical Details

### Key Classes
- **Game**: Main game state manager, handles turn logic, timers, and game flow
- **Pieces**: Base class with specialized subclasses for each piece type
- **Interface Functions**: Menu systems, timers, and visual feedback

### Notable Functions
- `is_legal_move()`: Validates moves according to chess rules
- `is_safe_move()`: Ensures moves don't leave king in check
- `algebraic_notation()`: Converts moves to standard notation
- `is_checkmate()` / `is_stalemate()`: Game end condition detection

## Future Enhancements

- [x] AI opponent with difficulty levels
- [ ] Move history viewer
- [ ] Undo/redo functionality
- [ ] Custom piece promotion choice



## License

This project is open source and available under the MIT License.

## Acknowledgments

- Chess piece graphics from various open-source chess sets
- Sound effects for enhanced gameplay experience
- Pygame community for excellent documentation and support

---

**Enjoy playing ChessRush!** ♟️✨
