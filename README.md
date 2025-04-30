# MCP Servers (Crawl4AI and PokerNow)

This repository contains two Model-Controller-Processor (MCP) servers:
- **Crawl4AI Scraping Server** – Provides web crawling and AI-based content analysis using LLMs (e.g., Claude).  
- **PokerNow Server** – Enables AI agents to interact with PokerNow.club online poker games (Texas Hold'em), retrieving game state and performing actions.

## Credits
- Craw4ai: https://github.com/unclecode/crawl4ai by unclecode
- Pokernow client: https://github.com/Zehmosu/PokerNow by Zehmosu
- Scraping Server forked from : https://github.com/MaitreyaM/WEB-SCRAPING-MCP by Maitreya Mishra

## Table of Contents
- [Crawl4AI Scraping Server](#crawl4ai-scraping-server)  
  - [Features (Crawl4AI)](#features-crawl4ai)  
  - [Exposed MCP Tools (Crawl4AI)](#exposed-mcp-tools-crawl4ai)  
  - [Setup and Running (Crawl4AI)](#setup-and-running-crawl4ai)  
  - [Environment Variables](#environment-variables)  
  - [Example Agent Interaction](#example-agent-interaction)  
- [PokerNow Server](#pokernow-server)  
  - [Features (PokerNow)](#features-pokernow)  
  - [Exposed MCP Tools (PokerNow)](#exposed-mcp-tools-pokernow)  
  - [Setup and Running (PokerNow)](#setup-and-running-pokernow)  
- [Files](#files)  

## Crawl4AI Scraping Server
Crawl4AI MCP Server is an AI-powered web crawling and content analysis service. It provides a REST API that allows AI agents to crawl specific websites and process the retrieved content using LLMs (e.g., Claude) for summarization, extraction, and analysis.

### Features (Crawl4AI)
- Configurable web crawling (adjust depth, follow link rules, and specify content selectors).  
- Respects `robots.txt` and polite crawling delays.  
- Extracts and processes web page content (main text, links, metadata).  
- AI-powered content analysis (summaries, fact extraction, deep insights, or Q&A) using Claude models.  
- Simple REST API interface for integration with agents or applications.  
- Configurable via command-line options and environment variables.  
- Detailed logging for monitoring and debugging.

### Exposed MCP Tools (Crawl4AI)
#### `scrape_url`
Scrape a webpage and return its content in Markdown format.

**Arguments:**  
- `url` (str, required): The URL of the webpage to scrape.

**Returns:**  
- (str): The webpage content in Markdown format, or an error message.

#### `extract_text_by_query`
Search a webpage for specific text and return matching snippets.

**Arguments:**  
- `url` (str, required): The URL of the webpage to search.  
- `query` (str, required): The text query to find (case-insensitive).  
- `context_size` (int, optional): Number of characters to include before/after each match (default: 300).

**Returns:**  
- (str): A formatted string of up to the first 5 matching snippets containing the query, or a message if no matches are found (or an error).

#### `smart_extract`
Use an LLM to intelligently extract specific information from a webpage based on a natural language instruction.

**Arguments:**  
- `url` (str, required): The URL of the webpage to analyze.  
- `instruction` (str, required): A description of what to extract (e.g., "List all contact emails on this page").

**Returns:**  
- (str): The extracted information (often in structured text or JSON), or a message if nothing relevant is found (or an error).

### Setup and Running (Crawl4AI)
You can run the Crawl4AI server either with Docker or locally.

#### Option 1: Running with Docker (Recommended)
1. **Install Docker:** Download and install [Docker Desktop](https://www.docker.com) for your OS and start it.  
2. **Clone this repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
3. **Create a `.env` file:** In the project root, add your Anthropic (Claude) API key:
    ```bash
    ANTHROPIC_API_KEY=your_anthropic_key_here
    ```
4. **Build the Docker image:**
    ```bash
    docker build -t crawl4ai-mcp-server .
    ```
5. **Run the Docker container:**  
    ```bash
    docker run -it --rm -p 8002:8002 --env-file .env crawl4ai-mcp-server
    ```
   The server will start and listen on `http://0.0.0.0:8002` (SSE endpoint at `/sse`).  
6. **Connect your MCP client:** Configure your agent or client to connect to `http://127.0.0.1:8002/sse` (Server-Sent Events transport).

#### Option 2: Running Locally
1. **Install Python:** Ensure Python 3.9 or higher is installed.  
2. **Clone this repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
3. **(Optional) Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # (On Windows: venv\Scripts\activate)
    ```
4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5. **Create a `.env` file:** Add your Claude API key (same as above).  
6. **Run the server:**
    ```bash
    python crawl_server.py
    ```
   The server will start and listen on `http://127.0.0.1:8002/sse`.

### Environment Variables
The Crawl4AI server can be configured via environment variables (in `.env` or your shell):  
- `ANTHROPIC_API_KEY`: Your Anthropic (Claude) API key.  
- `PORT` (optional): Server port (default: 8002).  
- `DEBUG` (optional): Set to `true` to enable debug logging.

### Example Agent Interaction
```
You: scrape_url https://example.com
Agent: Thinking...
[Tool: scrape_url("https://example.com")]
Agent: [Markdown content of example.com]

You: extract_text_by_query https://example.com query="MCP"
Agent: Thinking...
[Tool: extract_text_by_query("https://example.com", "MCP")]
Agent: Found 2 matches for 'MCP':
- ... [snippet 1] ...
- ... [snippet 2] ...

You: smart_extract https://openai.com instruction="List the key features of OpenAI's mission."
Agent: Thinking...
[Tool: smart_extract("https://openai.com", "List the key features of OpenAI's mission.")]
Agent: Successfully extracted information:
{
  "features": [
    "Ensure artificial general intelligence benefits all of humanity",
    "Collaborate with other institutions",
    "Conduct research to make AGI safe and beneficial"
  ]
}
```

## PokerNow Server
The PokerNow Server is an MCP server that allows AI agents to interact with PokerNow.club (online Texas Hold'em) games through browser automation. It exposes tools for creating games, joining games, retrieving real-time game state (players, cards, pot, blinds, etc.), and taking poker actions (fold, call, raise) on behalf of the agent.

### Features (PokerNow)
- Integrates with PokerNow.club to manage private Texas Hold'em games.  
- Automates game creation and joining for multiplayer tables.  
- Retrieves live game state: players’ names, stacks, statuses, hole cards, community cards, dealer position, and blinds.  
- Allows the agent to perform game actions (fold, call, raise) through exposed tools.  
- No external API keys or environment variables required (uses built-in browser automation).

### Exposed MCP Tools (PokerNow)
#### `create_game`
Create a new PokerNow game table and return its invite link or code.

**Arguments:**  
- None

**Returns:**  
- (str): The URL or code for the newly created PokerNow game.

#### `join_game`
Join an existing PokerNow game.

**Arguments:**  
- `game_url` (str, required): The invite URL or code of the game to join.  
- `player_name` (str, optional): The name to use in the game (if required).

**Returns:**  
- (str): Confirmation message or error.

#### `start_game`
Start the PokerNow game (begin play after all players have joined).

**Arguments:**  
- None

**Returns:**  
- (str): Confirmation that the game has started.

#### `get_game_state`
Retrieve the current state of the game.

**Arguments:**  
- None

**Returns:**  
- (dict): An object containing:  
  - `community_cards` (list of str): The community cards on the table (up to 5 cards).  
  - `pot` (float): The current total pot size.  
  - `players` (list of dict): Each player’s `name`, `stack` (remaining chips), and `status` ("active", "folded", or "all-in"). (Own hole cards may be included.)  
  - `dealer_position` (int): The index (or name) of the dealer.  
  - `current_turn` (str): The name of the player whose turn it is.  
  - `small_blind` (float): Small blind amount.  
  - `big_blind` (float): Big blind amount.

#### `get_community_cards`
Get the current community cards on the table.

**Arguments:**  
- None

**Returns:**  
- (list of str): The community cards (e.g., `["Ah", "Kd", "2c", "7s", "Jh"]`).

#### `get_player_cards`
Get the hole cards dealt to the agent's player.

**Arguments:**  
- None

**Returns:**  
- (list of str): The two hole cards of your player (e.g., `["Qc", "5h"]`), or an empty list if not dealt yet.

#### `get_players_info`
Get information for all players in the game.

**Arguments:**  
- None

**Returns:**  
- (list of dict): For each player, a dictionary with `name`, `stack`, and `status` ("active", "folded", etc.).

#### `get_current_player`
Get the name of the player whose turn it is.

**Arguments:**  
- None

**Returns:**  
- (str): The name of the active player.

#### `get_blinds`
Get the current small and big blind amounts.

**Arguments:**  
- None

**Returns:**  
- (dict): Contains `small_blind` and `big_blind` values.

#### `perform_action`
Perform a poker action for your player.

**Arguments:**  
- `action` (str, required): The action to take (`"fold"`, `"call"`, or `"raise"`).  
- `amount` (float, optional): The bet amount (required if `action` is `"raise"`, ignored for fold/call).

**Returns:**  
- (str): Result of the action (e.g., confirmation or error message).

### Setup and Running (PokerNow)
You can run the PokerNow server either with Docker or locally. No special environment setup is needed.

#### Option 1: Running with Docker
1. **Install Docker:** Ensure Docker is installed and running on your machine.  
2. **Clone this repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
3. **Build the Docker image:**
    ```bash
    docker build -t pokernow-mcp-server .
    ```
4. **Run the Docker container:**  
    ```bash
    docker run -it --rm -p 8002:8002 pokernow-mcp-server
    ```
   The server will start and listen on `http://0.0.0.0:8002` (SSE endpoint at `/sse`).  
5. **Connect your MCP client:** Configure your agent to connect to `http://127.0.0.1:8002/sse`.

#### Option 2: Running Locally
1. **Install Python:** Ensure Python 3.9 or higher is installed.  
2. **Clone this repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
3. **(Optional) Create and activate a virtual environment.**  
4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5. **Run the server:**
    ```bash
    python poker_server.py
    ```
   The server will start and listen on `http://127.0.0.1:8002/sse`.

## Files
- `crawl_server.py`: Main Python script for the Crawl4AI scraping MCP server.  
- `poker_server.py`: Main Python script for the PokerNow MCP server.  
- `Dockerfile`: Builds a Docker container image for deploying the servers.  
- `requirements.txt`: Python dependencies for both servers.  
- `.env.example`: Sample environment file for the Crawl4AI server (contains placeholder for Claude API key).  
- `.gitignore`: Git ignore file (including `.env`).  
- `README.md`: This documentation file.
