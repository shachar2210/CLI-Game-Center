# 🎮 Python CLI Game Center

A feature-rich **command-line game collection** built with **Python** and the
[`rich`](https://github.com/Textualize/rich) library.  
The project features classic games, smart AI opponents, a persistent leaderboard,
and a polished terminal UI.

---

## ✨ Features

### 🎲 Games Included
- ⭕ **Tic Tac Toe**  
  Unbeatable AI using the **Minimax algorithm**.
- 🔴 **Connect Four**  
  Play against a smart heuristic AI or a second human player.
- 🃏 **Blackjack (21)**  
  Classic casino rules against a dealer.
- 🧠 **Memory Game**  
  Visual card-matching game in the terminal.

### 🤖 AI Opponents
- **Easy Mode:** Random moves.
- **Hard Mode:** Intelligent decision-making.
  - *Tic Tac Toe:* Full Minimax search (guaranteed optimal play).
  - *Connect Four:* Advanced heuristics with:
    - Immediate win detection  
    - Forced blocking  
    - Trap avoidance (global safety checks)  
    - Positional scoring (center control, potential lines)

### 🏆 Leaderboard
- Persistent leaderboard stored in a **JSON file**.
- Tracks wins and high scores across sessions.

### 🎨 Terminal UI
- Clean, colorful, and readable interface powered by **Rich**.

### 🐳 Docker Support
- Fully dockerized for easy setup and consistent execution.

---

## 🚀 Installation & Usage

### Option 1: Run with Docker (Recommended)

No Python installation required.

```bash
# Build the image
docker build -t game-center .

# Run the game
docker run -it --rm game-center
```

---

### Option 2: Run Locally with Python

#### Requirements
- Python 3.x

#### Steps

```bash
# Clone the repository
git clone https://github.com/shachar2210/CLI-Game-Center.git
cd CLI-Game-Center

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

---

## 🧠 AI Implementation Details

### Tic Tac Toe (Hard)
- Uses the **Minimax algorithm**.
- Explores all possible future game states.
- Guaranteed to never lose.

### Connect Four (Hard)
- Uses a **heuristic-based scoring system**.
- Features:
  - Immediate win detection
  - Global forced blocking
  - Trap detection (avoids giving the opponent a winning move)
  - Positional evaluation (center column preference, potential connections)
- Optimized using **do/undo backtracking** instead of deep copying where possible.

---

## 📂 Project Structure

```
.
├── main.py              # Entry point and menu system
├── ai_player.py         # AI logic for all games
├── score_manager.py     # Persistent JSON leaderboard
├── base_game.py         # Abstract base class for games
├── tic_tac_toe.py       # Tic Tac Toe implementation
├── connect_four.py      # Connect Four implementation
├── blackjack.py         # Blackjack (21)
├── memory_game.py       # Memory matching game
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🛠 Technologies Used
- Python 3
- Rich (terminal UI)
- Docker
- JSON (data persistence)

---

## 👤 Author

Created by **Shachar Shtienmetz**
