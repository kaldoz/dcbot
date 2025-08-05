# Discord Game Bot

A Discord bot for hosting and managing Team Fortress 2 games with class-based signups.

## Features

- **Host Games**: Create games with date, time, server, and division information
- **Class-based Signups**: Support for 6 classes with proper slot limits:
  - 2 Scouts
  - 2 Soldiers  
  - 1 Demo
  - 1 Medic
- **Signup Management**: Players can signup and signout with proper validation
- **Default Settings**: All games default to 9:00 PM SGT
- **Error Handling**: Proper error messages for full slots and invalid inputs

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Bot Token**:
   - Copy `.env.example` to `.env`
   - Add your Discord bot token to the `.env` file:
     ```
     DISCORD_TOKEN=your_actual_bot_token_here
     ```

3. **Run the Bot**:
   ```bash
   python bot.py
   ```

## Discord Commands

### `!host_game <date> [server] [division]`
Host a new game. 
- `date`: Date of the game (required)
- `server`: Server name (optional, defaults to "TBD")
- `division`: Division number 1-3 (optional, defaults to 1)

**Example**: `!host_game 2024-01-15 "EU Server" 2`

### `!signup <game_id> <class>`
Sign up for a specific class in a game.
- `game_id`: The ID of the game to join
- `class`: The class to play (scout, soldier, demo, medic)

**Example**: `!signup 1 scout`

### `!signout <game_id>`
Sign out from a game.
- `game_id`: The ID of the game to leave

**Example**: `!signout 1`

### `!game_status <game_id>`
Check the current signup status of a game.

### `!list_games`
List all currently active games.

## Class Limits

- **Scout**: 2 slots
- **Soldier**: 2 slots
- **Demo**: 1 slot
- **Medic**: 1 slot

## Error Messages

- "No [class] slots available" - When trying to signup for a full class
- "You are already signed up for [class] in this game" - When already signed up
- "Game #[id] not found" - When referencing a non-existent game
- "Invalid class" - When using an unsupported class name

## Testing

Run the test suite to verify bot functionality:
```bash
python test_bot.py
```

## Development

The bot uses discord.py 2.3+ and stores game data in memory. For production use, consider implementing persistent storage with a database.
