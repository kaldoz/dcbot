#!/usr/bin/env python3
"""
Simple test script for the Discord bot functionality.
This tests the core game logic without requiring Discord API.
"""

import sys
sys.path.append('/home/runner/work/dcbot/dcbot')
from bot import Game, CLASS_LIMITS

def test_game_creation():
    """Test game creation."""
    game = Game(1, "2024-01-15", "9:00 PM SGT", "Server 1", 2)
    assert game.game_id == 1
    assert game.date == "2024-01-15"
    assert game.time == "9:00 PM SGT"
    assert game.server == "Server 1"
    assert game.division == 2
    print("✅ Game creation test passed")

def test_player_signup():
    """Test player signup functionality."""
    game = Game(1, "2024-01-15")
    
    # Test successful signup
    assert game.add_player("player1", "scout") == True
    assert "player1" in game.signups["scout"]
    
    # Test duplicate signup for same player
    assert game.add_player("player1", "soldier") == False
    
    # Test filling up scout slots
    assert game.add_player("player2", "scout") == True
    assert game.add_player("player3", "scout") == False  # Should fail, scouts full
    
    print("✅ Player signup test passed")

def test_player_signout():
    """Test player signout functionality."""
    game = Game(1, "2024-01-15")
    
    # Add a player
    game.add_player("player1", "medic")
    assert "player1" in game.signups["medic"]
    
    # Remove the player
    assert game.remove_player("player1") == True
    assert "player1" not in game.signups["medic"]
    
    # Try to remove non-existent player
    assert game.remove_player("player999") == False
    
    print("✅ Player signout test passed")

def test_class_limits():
    """Test that class limits are enforced correctly."""
    game = Game(1, "2024-01-15")
    
    # Test scout limit (2)
    assert game.add_player("scout1", "scout") == True
    assert game.add_player("scout2", "scout") == True
    assert game.add_player("scout3", "scout") == False
    
    # Test demo limit (1)
    assert game.add_player("demo1", "demo") == True
    assert game.add_player("demo2", "demo") == False
    
    # Test medic limit (1)
    assert game.add_player("medic1", "medic") == True
    assert game.add_player("medic2", "medic") == False
    
    print("✅ Class limits test passed")

def test_invalid_class():
    """Test invalid class handling."""
    game = Game(1, "2024-01-15")
    
    # Test invalid class
    assert game.add_player("player1", "spy") == False
    assert game.add_player("player1", "heavy") == False
    
    print("✅ Invalid class test passed")

def test_game_status():
    """Test game status generation."""
    game = Game(1, "2024-01-15", "9:00 PM SGT", "Test Server", 2)
    
    # Add some players
    game.add_player("player1", "scout")
    game.add_player("player2", "medic")
    
    status = game.get_signup_status()
    assert "Game #1" in status
    assert "2024-01-15" in status
    assert "9:00 PM SGT" in status
    assert "Test Server" in status
    assert "Division: 2" in status
    assert "Scout: 1/2" in status
    assert "Medic: 1/1" in status
    
    print("✅ Game status test passed")

if __name__ == "__main__":
    print("Running Discord bot tests...")
    
    test_game_creation()
    test_player_signup()
    test_player_signout()
    test_class_limits()
    test_invalid_class()
    test_game_status()
    
    print("\n🎉 All tests passed! The bot logic is working correctly.")
    print("\nTo run the Discord bot:")
    print("1. Create a .env file with your DISCORD_TOKEN")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the bot: python bot.py")