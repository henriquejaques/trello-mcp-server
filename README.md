# Trello MCP Server

A powerful Model Context Protocol (MCP) server that enables AI assistants to interact with Trello boards, lists, cards, and checklists through a standardized interface.

> **Note**: This project is forked from [m0xai/trello-mcp-server](https://github.com/m0xai/trello-mcp-server) with additional improvements and features. Credit to the original author for the foundational work.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Server Modes](#server-modes)
- [Configuration](#configuration)
- [Client Integration](#client-integration)
- [Capabilities](#capabilities)
- [Usage Examples](#usage-examples)
- [Architecture](#architecture)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- 🔄 **Full Trello API Coverage**: Complete CRUD operations for boards, lists, cards, and checklists
- 🤖 **AI Assistant Integration**: Seamless integration with Claude Desktop, Cursor, and other MCP-compatible clients
- 🚀 **Dual Mode Operation**: Support for both Claude Desktop integration and standalone SSE server
- 🐳 **Docker Support**: Containerized deployment with Docker Compose
- 📝 **Type Safety**: Built with Pydantic models and comprehensive type hints
- ⚡ **Async Architecture**: Fully asynchronous for optimal performance
- 🔧 **Easy Configuration**: Environment-based configuration with sensible defaults


## Prerequisites

1. **Python 3.12+** - Easily managed with [uv](https://github.com/astral-sh/uv)
2. **Trello Account** - With API credentials (API key and token)
3. **AI Client** (optional) - [Claude Desktop](https://claude.ai/download), Cursor, or other MCP-compatible client
4. **Docker** (optional) - For containerized deployment

## Installation

### 1. Get Trello API Credentials

1. Go to [Trello Apps Administration](https://trello.com/power-ups/admin)
2. Create a new integration at [New Power-Up or Integration](https://trello.com/power-ups/admin/new)
3. Fill in your information (Iframe connector URL can be left empty)
4. Click your app's icon → "API key" from the left sidebar
5. Copy your **API Key** and click "Token" to generate your **Trello Token**

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/trello-mcp-server.git
cd trello-mcp-server

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy environment template and configure
cp .env.example .env
# Edit .env with your credentials:
# TRELLO_API_KEY=your_api_key_here
# TRELLO_TOKEN=your_token_here
```

### 3. Choose Installation Method

#### Option A: Claude Desktop Integration
```bash
# Install and configure for Claude Desktop
uv run mcp install main.py

# Restart Claude Desktop app
```

#### Option B: Standalone SSE Server
```bash
# Set USE_CLAUDE_APP=false in .env, then run:
python main.py
```

#### Option C: Docker Deployment
```bash
# Ensure .env is configured, then:
docker-compose up -d
```

## Server Modes

This MCP server can run in two different modes:

### Claude App Mode

This mode integrates directly with the Claude Desktop application:

1. Set `USE_CLAUDE_APP=true` in your `.env` file (this is the default)
2. Run the server with:
```bash
uv run mcp install main.py
```
3. Restart the Claude Desktop application

### SSE Server Mode

This mode runs as a standalone SSE server that can be used with any MCP-compatible client, including Cursor:

1. Set `USE_CLAUDE_APP=false` in your `.env` file
2. Run the server with:
```bash
python main.py
```
3. The server will be available at `http://localhost:8000` by default (or your configured port)

### Docker Mode

You can also run the server using Docker Compose:

1. Make sure you have Docker and Docker Compose installed
2. Create your `.env` file with your configuration
3. Build and start the container:
```bash
docker-compose up -d
```
4. The server will run in SSE mode by default
5. To view logs:
```bash
docker-compose logs -f
```
6. To stop the server:
```bash
docker-compose down
```

## Configuration

The server can be configured using environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| TRELLO_API_KEY | Your Trello API key | Required |
| TRELLO_TOKEN | Your Trello API token | Required |
| MCP_SERVER_NAME | The name of the MCP server | Trello MCP Server |
| MCP_SERVER_HOST | Host address for SSE mode | 0.0.0.0 |
| MCP_SERVER_PORT | Port for SSE mode | 8000 |
| USE_CLAUDE_APP | Whether to use Claude app mode | true |

You can customize the server by editing these values in your `.env` file.

## Client Integration

### Using with Claude Desktop

1. Run the server in Claude app mode (`USE_CLAUDE_APP=true`)
2. Start or restart Claude Desktop
3. Claude will automatically detect and connect to your MCP server

### Using with Cursor

To connect your MCP server to Cursor:

1. Run the server in SSE mode (`USE_CLAUDE_APP=false`)
2. In Cursor, go to Settings (gear icon) > AI > Model Context Protocol
3. Add a new server with URL `http://localhost:8000` (or your configured host/port)
4. Select the server when using Cursor's AI features

You can also add this configuration to your Cursor settings JSON file (typically at `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "trello": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### Using with Other MCP Clients

For other MCP-compatible clients, point them to the SSE endpoint at `http://localhost:8000`.

### Minimal Client Example

Here's a minimal Python example to connect to the SSE endpoint:

```python
import asyncio
import httpx

async def connect_to_mcp_server():
    url = "http://localhost:8000/sse"
    headers = {"Accept": "text/event-stream"}
    
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url, headers=headers) as response:
            # Get the session ID from the first SSE message
            session_id = None
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    data = line[5:].strip()
                    if "session_id=" in data and not session_id:
                        session_id = data.split("session_id=")[1]
                        
                        # Send a message using the session ID
                        message_url = f"http://localhost:8000/messages/?session_id={session_id}"
                        message = {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": "Show me my Trello boards"
                            }
                        }
                        await client.post(message_url, json=message)

if __name__ == "__main__":
    asyncio.run(connect_to_mcp_server())
```

## Capabilities

| Operation | Board | List | Card | Checklist | Checklist Item |
|-----------|-------|------|------|-----------|----------------|
| Read      | ✅    | ✅    | ✅   | ✅        | ✅              |
| Write     | ✅    | ✅    | ✅   | ✅        | ✅              |
| Update    | ❌    | ✅    | ✅   | ✅        | ✅              |
| Delete    | ❌    | ✅    | ✅   | ✅        | ✅              |

### Detailed Capabilities

#### Board Operations
- ✅ Read all boards
- ✅ Read specific board details
- ✅ Create new boards (with comprehensive parameter support)

#### List Operations
- ✅ Read all lists in a board
- ✅ Read specific list details
- ✅ Create new lists
- ✅ Update list name
- ✅ Archive (delete) lists

#### Card Operations
- ✅ Read all cards in a list
- ✅ Read specific card details
- ✅ Create new cards
- ✅ Update card attributes
- ✅ Delete cards

#### Checklist Operations
- ✅ Get a specific checklist
- ✅ List all checklists in a card
- ✅ Create a new checklist
- ✅ Update a checklist
- ✅ Delete a checklist
- ✅ Add checkitem to checklist
- ✅ Update checkitem
- ✅ Delete checkitem

## Usage Examples

Once installed, you can interact with your Trello boards through any MCP-compatible AI client:

### Basic Operations
- "Show me all my boards"
- "Create a new board called 'Q1 Project Planning'"
- "What lists are in the 'Project Management' board?"
- "Create a new card called 'Review documentation' in the 'To Do' list"
- "Update the description of the 'Website redesign' card"
- "Move the 'Bug fixes' card to the 'In Progress' list"
- "Archive the 'Completed Tasks' list"

### Advanced Workflows
- "Create a new card with a checklist for project milestones"
- "Show me all overdue cards across my boards"
- "Add team members to the 'Sprint Planning' card"
- "Create a weekly report template with checklists"

### Example Screenshots

<img width="1277" alt="Example Usage: Listing cards in Guitar Board" src="https://github.com/user-attachments/assets/fef29dfc-04b2-4af9-92a6-f8db2320c860" />

<img width="1274" alt="Adding new song card to project" src="https://github.com/user-attachments/assets/2d8406ca-1dde-41c0-a035-86d5271dd78f" />

<img width="1632" alt="Creating card with checklist" src="https://github.com/user-attachments/assets/5a63f107-d135-402d-ab33-b9bf13eca751" />

## Architecture

This MCP server follows a clean layered architecture:

```
MCP Interface (FastMCP)
    ↓
Tools Layer (/server/tools/)
    ↓
Service Layer (/server/services/)  
    ↓
HTTP Client Layer (/server/utils/trello_api.py)
    ↓
Trello REST API
```

### Key Components
- **TrelloClient**: Async HTTP client for Trello API communication
- **Services**: Business logic layer (`BoardService`, `CardService`, etc.)
- **Tools**: MCP-compatible interface with error handling
- **Models**: Pydantic data models for type safety

## Development

### Local Development
```bash
# Install dependencies
uv sync

# Run with development logging
uv run mcp dev main.py

# Run standalone server
python main.py
```

### Code Quality
```bash
# Linting
ruff check .

# Type checking  
mypy .

# Formatting
ruff format .
```

### Testing
```bash
# Run tests (when implemented)
pytest
```

## Troubleshooting

If you encounter issues:

1. Verify your Trello API credentials in the `.env` file
2. Check that you have proper permissions in your Trello workspace
3. Ensure Claude for Desktop is running the latest version
4. Check the logs for any error messages with `uv run mcp dev main.py` command.
5. Make sure uv is properly installed and in your PATH

## Contributing

Contributions are welcome! This project is a fork of [m0xai/trello-mcp-server](https://github.com/m0xai/trello-mcp-server) with ongoing improvements.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following the existing code style
4. **Add tests** for new functionality (when test suite is implemented)
5. **Run quality checks**: `ruff check . && mypy .`
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Priorities

Current areas where contributions would be especially valuable:
- **Test Suite**: Adding comprehensive test coverage
- **Error Handling**: Improving error messages and recovery
- **Documentation**: Expanding examples and use cases
- **Performance**: Optimizing API call patterns

## License

This project maintains the same license as the original [m0xai/trello-mcp-server](https://github.com/m0xai/trello-mcp-server). Please refer to the original repository for license details.

---

**Acknowledgments**: Special thanks to [m0xai](https://github.com/m0xai) for creating the original Trello MCP server that serves as the foundation for this project.
