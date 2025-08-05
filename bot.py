import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Game data storage (in a real implementation, you'd use a database)
games: Dict[int, Dict] = {}
game_counter = 0

# Available classes and their limits
CLASS_LIMITS = {
    'scout': 2,
    'soldier': 2,
    'demo': 1,
    'medic': 1
}

# Singapore timezone
SGT = timezone(timedelta(hours=8))

class Game:
    def __init__(self, game_id: int, date: str, time: str = "9:00 PM SGT", 
                 server: str = "TBD", division: int = 1):
        self.game_id = game_id
        self.date = date
        self.time = time
        self.server = server
        self.division = division
        self.signups: Dict[str, List[str]] = {
            'scout': [],
            'soldier': [],
            'demo': [],
            'medic': []
        }
    
    def add_player(self, player_id: str, class_name: str) -> bool:
        """Add a player to a class. Returns True if successful, False if full."""
        class_name = class_name.lower()
        if class_name not in CLASS_LIMITS:
            return False
        
        # Check if player is already signed up for any class
        for cls, players in self.signups.items():
            if player_id in players:
                return False  # Player already signed up
        
        # Check if class has space
        if len(self.signups[class_name]) >= CLASS_LIMITS[class_name]:
            return False
        
        self.signups[class_name].append(player_id)
        return True
    
    def remove_player(self, player_id: str) -> bool:
        """Remove a player from all classes. Returns True if player was found and removed."""
        for class_name, players in self.signups.items():
            if player_id in players:
                players.remove(player_id)
                return True
        return False
    
    def get_signup_status(self) -> str:
        """Get a formatted string showing current signups."""
        status = f"**Game #{self.game_id}**\n"
        status += f"📅 Date: {self.date}\n"
        status += f"🕘 Time: {self.time}\n"
        status += f"🖥️ Server: {self.server}\n"
        status += f"🏆 Division: {self.division}\n\n"
        status += "**Current Signups:**\n"
        
        for class_name, limit in CLASS_LIMITS.items():
            players = self.signups[class_name]
            status += f"🔹 {class_name.capitalize()}: {len(players)}/{limit}\n"
            for player_id in players:
                status += f"  - <@{player_id}>\n"
            if len(players) == 0:
                status += "  - (No signups)\n"
        
        return status

@bot.event
async def on_ready():
    print(f'{bot.user} has logged in to Discord!')
    print(f'Bot is ready to host games!')

@bot.command(name="host_game")
async def host_game(ctx, date: str, server: str = "TBD", division: int = 1):
    """Host a new game with specified parameters."""
    global game_counter
    game_counter += 1
    
    # Validate division
    if division not in [1, 2, 3]:
        await ctx.send("❌ Division must be 1, 2, or 3.")
        return
    
    # Create new game with default 9pm SGT time
    game = Game(game_counter, date, "9:00 PM SGT", server, division)
    games[game_counter] = game
    
    embed = discord.Embed(
        title=f"🎮 New Game Hosted! (Game #{game_counter})",
        description=game.get_signup_status(),
        color=discord.Color.blue()
    )
    
    await ctx.send(embed=embed)

@bot.command(name="signup")
async def signup(ctx, game_id: int, class_name: str):
    """Sign up for a specific class in a game."""
    player_id = str(ctx.author.id)
    class_name = class_name.lower()
    
    # Validate class name
    if class_name not in CLASS_LIMITS:
        valid_classes = ", ".join(CLASS_LIMITS.keys())
        await ctx.send(f"❌ Invalid class. Available classes: {valid_classes}")
        return
    
    # Check if game exists
    if game_id not in games:
        await ctx.send(f"❌ Game #{game_id} not found.")
        return
    
    game = games[game_id]
    
    # Check if player is already signed up
    for cls, players in game.signups.items():
        if player_id in players:
            await ctx.send(f"❌ You are already signed up for {cls} in this game.")
            return
    
    # Try to add player
    if game.add_player(player_id, class_name):
        embed = discord.Embed(
            title=f"✅ Successfully signed up!",
            description=f"You have been signed up as **{class_name}** for Game #{game_id}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
        # Send updated game status
        status_embed = discord.Embed(
            title="Updated Game Status",
            description=game.get_signup_status(),
            color=discord.Color.blue()
        )
        await ctx.send(embed=status_embed)
    else:
        await ctx.send(f"❌ No {class_name} slots available")

@bot.command(name="signout")
async def signout(ctx, game_id: int):
    """Sign out from a game."""
    player_id = str(ctx.author.id)
    
    # Check if game exists
    if game_id not in games:
        await ctx.send(f"❌ Game #{game_id} not found.")
        return
    
    game = games[game_id]
    
    # Try to remove player
    if game.remove_player(player_id):
        embed = discord.Embed(
            title="✅ Successfully signed out!",
            description=f"You have been removed from Game #{game_id}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        
        # Send updated game status
        status_embed = discord.Embed(
            title="Updated Game Status",
            description=game.get_signup_status(),
            color=discord.Color.blue()
        )
        await ctx.send(embed=status_embed)
    else:
        await ctx.send(f"❌ You are not signed up for Game #{game_id}.")

@bot.command(name="game_status")
async def game_status(ctx, game_id: int):
    """Check the current status of a game."""
    if game_id not in games:
        await ctx.send(f"❌ Game #{game_id} not found.")
        return
    
    game = games[game_id]
    embed = discord.Embed(
        title="Game Status",
        description=game.get_signup_status(),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name="list_games")
async def list_games(ctx):
    """List all currently hosted games."""
    if not games:
        await ctx.send("No games currently hosted.")
        return
    
    description = ""
    for game_id, game in games.items():
        description += f"**Game #{game_id}**: {game.date} at {game.time}\n"
        description += f"Server: {game.server}, Division: {game.division}\n\n"
    
    embed = discord.Embed(
        title="🎮 Active Games",
        description=description,
        color=discord.Color.purple()
    )
    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: DISCORD_TOKEN not found in environment variables.")
        print("Please create a .env file with your Discord bot token.")
    else:
        bot.run(token)