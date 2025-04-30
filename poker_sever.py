import logging
import asyncio
import json
import time
from mcp.server.fastmcp import FastMCP
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PokerNow import PokerClient  # Assuming this is the correct import
from models_local import GameState

# --- Configure logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("poker_mcp")

# --- Shared Selenium client setup ---
# Initialize the Selenium WebDriver
options = Options()
# options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
client = PokerClient(driver)

# Prompt user for manual login
logger.info("Prompting user for manual login...")
print("Please log in to PokerNow.club in the opened browser window.")
print("After completing the login process, return here and press Enter to continue...")
input()
logger.info("User completed login, starting MCP server...")

# Create FastMCP instance
mcp = FastMCP("PokerNow_mcp")
mcp.settings.port = 8000

# --- Define tool methods ---

@mcp.tool()
# This Function is successful
async def navigate(url: str) -> dict:
    """Navigate the browser to a specific URL."""
    logger.info("Called navigate with URL: %s", url)
    try:
        client.navigate(url)
        logger.info("Navigation successful to %s", url)
        return {"status": "ok", "navigated_to": url}
    except Exception as e:
        logger.error("Navigation failed: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
async def get_game_state() -> dict:
    """Retrieve the current game state."""
    logger.info("Called get_game_state")
    try:
        state = client.game_state_manager.get_game_state()
        result = state.dict()
        logger.info("Game state retrieved: %s", result)
        return result
    except Exception as e:
        logger.error("Error retrieving game state: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
# always returns false even when it is my turn, suspect is the client's fault no need to fix now
async def is_your_turn() -> dict:
    """Check if it's your turn."""
    logger.info("Called is_your_turn")
    try:
        turn = client.game_state_manager.is_your_turn()
        logger.info("is_your_turn: %s", turn)
        return {"is_your_turn": turn}
    except Exception as e:
        logger.error("Error checking turn: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
async def get_community_cards() -> dict:
    """Get the community cards on the table."""
    logger.info("Called get_community_cards")
    try:
        cards = client.game_state_manager.get_community_cards()
        data = {"community_cards": [card.dict() for card in cards]}
        logger.info("Community cards: %s", data)
        return data
    except Exception as e:
        logger.error("Error getting community cards: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
async def get_players_info() -> dict:
    """Retrieve all players' info at the table."""
    logger.info("Called get_players_info")
    try:
        players = client.game_state_manager.get_players_info()
        data = {"players": [p.dict() for p in players]}
        logger.info("Players info: %s", data)
        return data
    except Exception as e:
        logger.error("Error getting players info: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
# Currently works
async def get_winners() -> dict:
    """Retrieve the winners of the last hand."""
    logger.info("Called get_winners")
    try:
        winners = client.game_state_manager.get_winners()
        logger.info("Winners: %s", winners)
        return {"winners": winners}
    except Exception as e:
        logger.error("Error getting winners: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
# This function is successful
async def get_blinds() -> dict:
    """Retrieve the current blinds values."""
    logger.info("Called get_blinds")
    try:
        small, big = client.game_state_manager.get_blinds()
        logger.info("Blinds: small=%s, big=%s", small, big)
        return {"small_blind": small, "big_blind": big}
    except Exception as e:
        logger.error("Error getting blinds: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
# only returns the sit position, no player name or how far the paly is.
async def get_dealer_position() -> dict:
    """Get the dealer button position."""
    logger.info("Called get_dealer_position")
    try:
        pos = client.game_state_manager.get_dealer_position()
        logger.info("Dealer position: %s", pos)
        return {"dealer_position": pos}
    except Exception as e:
        logger.error("Error getting dealer position: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
# This function currently doesn't work
async def get_current_player() -> dict:
    """Get the name of the current player."""
    logger.info("Called get_current_player")
    try:
        name = client.game_state_manager.get_current_player()
        logger.info("Current player: %s", name)
        return {"current_player": name}
    except Exception as e:
        logger.error("Error getting current player: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
# Only retrieves check and fold even when call and raise is available
async def get_available_actions() -> dict:
    """List available actions for the current player."""
    logger.info("Called get_available_actions")
    try:
        actions = client.action_helper.get_available_actions()
        action_list = list(actions.keys())
        logger.info("Available actions: %s", action_list)
        return {"actions": action_list}
    except Exception as e:
        logger.error("Error getting available actions: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
# Can only successfully check
async def perform_action(action: str, amount: int = None) -> dict:
    """Perform an action in the game."""
    logger.info("Called perform_action with action=%s, amount=%s", action, amount)
    try:
        client.action_helper.perform_action(action, amount=amount)
        logger.info("Action performed: %s %s", action, amount)
        return {"status": "ok", "action": action, "amount": amount}
    except Exception as e:
        logger.error("Error performing action: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
# This function currently doesn't work
async def handle_raise(amount: int) -> dict:
    """Handle a raise action with specified amount."""
    logger.info("Called handle_raise with amount=%s", amount)
    if amount is None:
        logger.error("Raise called without amount")
        return {"status": "error", "detail": "Amount is required for a raise."}
    try:
        client.action_helper.handle_raise(amount)
        logger.info("Raised to %s", amount)
        return {"status": "ok", "raised_to": amount}
    except Exception as e:
        logger.error("Error handling raise: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
# Unsure
async def check_and_handle_fold_confirmation() -> dict:
    """Check and confirm a fold dialog if present."""
    logger.info("Called check_and_handle_fold_confirmation")
    try:
        client.action_helper.check_and_handle_fold_confirmation()
        logger.info("Fold confirmation handled")
        return {"status": "ok"}
    except Exception as e:
        logger.error("Error handling fold confirmation: %s", e)
        return {"status": "error", "detail": str(e)}

@mcp.tool()
# Buggy
async def events() -> dict:
    """Streams the latest game state whenever it changes."""
    logger.info("Called events")
    last_state = None
    try:
        while True:
            state = client.game_state_manager.get_game_state().dict()
            if state != last_state:
                payload = json.dumps(state)
                last_state = state
                logger.info("Game state updated: %s", payload)
                return {"event": "game_state", "data": payload}
            await asyncio.sleep(1)
    except Exception as e:
        logger.error("Error streaming events: %s", e)
        return {"status": "error", "detail": str(e)}

# --- Main entrypoint ---
if __name__ == "__main__":
    logger.info("Starting MCP server on 0.0.0.0:8000")
    mcp.run(transport="sse")
