# Tic-Tac-Toe MCP Server

A Model Context Protocol (MCP) server for playing tic-tac-toe games. This server provides tools for creating games, making moves, displaying boards, and managing game state through AI assistants like Cursor.

* [Link to ~2 hour screen capture](https://drive.google.com/file/d/1gnKyjaTpD5BpKEnMT8pk5fAgfZZbWpCI/view?usp=sharing)

## Features

- 🎮 Create and manage tic-tac-toe games
- 🤖 Strategic AI opponent (configurable)
- 📊 Game state tracking and history
- 🎯 Win/draw detection
- 🔄 In-memory game storage (extensible to persistent storage)

## Installation

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd /path/to/tic-tac-toe
   ```

2. **Create a virtual environment:**
   ```bash
   uv venv
   # or
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate  # On Windows
   ```

4. **Install dependencies:**
   ```bash
   uv pip install fastmcp
   # or
   pip install fastmcp
   ```

5. **Optional: Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env to customize AI_TYPE and ENVIRONMENT
   ```

## Adding to Cursor

### Step 1: Locate Cursor's MCP Configuration

The MCP configuration file is located at:
- **macOS/Linux:** `~/.cursor/mcp.json`
- **Windows:** `%APPDATA%\Cursor\mcp.json`

### Step 2: Edit the Configuration File

Open `mcp.json` in your editor. If it doesn't exist, create it with the following structure:

```json
{
  "mcpServers": {
    "tic-tac-toe": {
      "command": "/absolute/path/to/tic-tac-toe/.venv/bin/python",
      "args": ["/absolute/path/to/tic-tac-toe/server.py"]
    }
  }
}
```

**Important:** Replace `/absolute/path/to/tic-tac-toe` with the actual absolute path to your project directory.

**Example for macOS/Linux:**
```json
{
  "mcpServers": {
    "tic-tac-toe": {
      "command": "/Users/leechow/Projects/tic-tac-toe/.venv/bin/python",
      "args": ["/Users/leechow/Projects/tic-tac-toe/server.py"]
    }
  }
}
```

**Example for Windows:**
```json
{
  "mcpServers": {
    "tic-tac-toe": {
      "command": "C:\\Users\\YourName\\Projects\\tic-tac-toe\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourName\\Projects\\tic-tac-toe\\server.py"]
    }
  }
}
```

### Step 3: Restart Cursor

After saving the configuration file, restart Cursor completely for the changes to take effect.

### Step 4: Verify Installation

Once Cursor restarts, you should be able to use the tic-tac-toe tools. Try asking Cursor:
- "Create a new tic-tac-toe game"
- "Show me the available tic-tac-toe tools"

## Available Tools

The MCP server provides the following tools:

### `create_game`
Create a new tic-tac-toe game.

**Parameters:**
- `player1_type` (optional): "human" or "computer" (default: "human")
- `player2_type` (optional): "human" or "computer" (default: "computer")
- `player1_piece` (optional): "X" or "O" (default: "X")
- `player2_piece` (optional): "X" or "O" (default: "O")

**Returns:** Game UUID, player UUIDs, and success message

### `display_board`
Display the current board state for a game.

**Parameters:**
- `game_uuid`: The UUID of the game

**Returns:** Formatted string representation of the board

### `get_next_move`
Get the next move suggestion from the AI.

**Parameters:**
- `game_uuid`: The UUID of the game
- `player_uuid`: The UUID of the player making the move

**Returns:** Suggested position (e.g., "A1", "B2", "C3")

### `add_move`
Add a move to the game.

**Parameters:**
- `game_uuid`: The UUID of the game
- `player_uuid`: The UUID of the player making the move
- `position`: Board position (e.g., "A1", "B2", "C3")

**Returns:** Move result with updated status and winner

### `get_game_state`
Get the full game state.

**Parameters:**
- `game_uuid`: The UUID of the game

**Returns:** Complete game information (players, moves, status, winner)

### `check_game_status`
Check if the game is win/draw/ongoing.

**Parameters:**
- `game_uuid`: The UUID of the game

**Returns:** Status and winner if applicable

### `list_moves`
List all moves in the game history.

**Parameters:**
- `game_uuid`: The UUID of the game

**Returns:** Chronologically ordered list of moves

## Usage Examples

### Example 1: Create and Play a Game

```
You: Create a new tic-tac-toe game
Cursor: [Creates game and returns game_uuid and player UUIDs]

You: Display the board
Cursor: [Shows empty board]

You: Add move A1 for player [player1_uuid]
Cursor: [Adds move and shows updated board]

You: Get next move for player [player2_uuid]
Cursor: [Suggests a move, e.g., "B2"]
```

### Example 2: Check Game Status

```
You: Check the status of game [game_uuid]
Cursor: [Returns current status: Ongoing/Win/Draw]
```

### Example 3: View Game History

```
You: List all moves for game [game_uuid]
Cursor: [Returns chronological list of all moves]
```

## Board Positions

The board uses a coordinate system:
- **Rows:** A (top), B (middle), C (bottom)
- **Columns:** 1 (left), 2 (middle), 3 (right)

**Valid positions:** A1, A2, A3, B1, B2, B3, C1, C2, C3

## Configuration

### Environment Variables

Create a `.env` file (or set environment variables) to configure the server:

```env
# Environment: development, staging, production, or testing
ENVIRONMENT=development

# AI Type: strategic or random
# - strategic: Uses StrategicAI (prioritizes winning, blocking, center, corners, sides)
# - random: Uses RandomSelection (picks random valid moves)
AI_TYPE=strategic
```

## Development

### Project Structure

```
tic-tac-toe/
├── config/          # Configuration service
├── game_ai/         # AI implementations
├── game_engine/     # Game logic engine
├── models/          # Data models (Game, Player, Move)
├── storage/         # Storage implementations
├── tests/           # Unit tests
├── server.py        # MCP server entry point
└── README.md        # This file
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_game_engine.py
```

### Running the Server Directly

You can also run the server directly (useful for testing):

```bash
python server.py
```

## Troubleshooting

### Server Not Appearing in Cursor

1. **Check the path:** Ensure the absolute paths in `mcp.json` are correct
2. **Check Python:** Verify the virtual environment Python path is correct
3. **Check permissions:** Ensure the Python executable has execute permissions
4. **Restart Cursor:** Always restart Cursor after changing `mcp.json`
5. **Check logs:** Look for errors in Cursor's developer console

### Common Issues

**Issue:** "Command not found" or "No such file or directory"
- **Solution:** Use absolute paths, not relative paths
- **Solution:** Verify the virtual environment exists and Python is installed

**Issue:** "Module not found" errors
- **Solution:** Ensure dependencies are installed: `uv pip install fastmcp`
- **Solution:** Verify you're using the correct virtual environment Python

**Issue:** Tools not appearing in Cursor
- **Solution:** Restart Cursor completely
- **Solution:** Check that the MCP server is enabled in Cursor settings

## License

This project is open source and available for use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

