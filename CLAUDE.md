# Trello MCP Server - Claude Code Instructions

## Project Overview
This is a Model Context Protocol (MCP) server for Trello integration, forked from [m0xai/trello-mcp-server](https://github.com/m0xai/trello-mcp-server). It enables AI assistants to interact with Trello boards, lists, cards, and checklists through a standardized interface.

## Architecture
- **Layered Architecture**: MCP Interface → Tools → Services → HTTP Client → Trello API
- **Tech Stack**: Python 3.12+, FastMCP, httpx, Pydantic, uvicorn
- **Pattern**: Clean separation of concerns with async/await throughout

## Key Directories
- `server/tools/` - MCP interface layer with error handling
- `server/services/` - Business logic layer
- `server/models.py` - Pydantic data models
- `server/utils/trello_api.py` - HTTP client for Trello API

## Development Guidelines

### Code Style
- Use async/await for all API operations
- Follow existing Pydantic model patterns
- Include comprehensive docstrings with type hints
- Use proper MCP error handling with `ctx.error()` in tools

### Testing
Run tests with: `pytest` (once test suite is implemented)

### Linting & Type Checking
- Run: `ruff check .` for linting
- Run: `mypy .` for type checking

### Docker
- Development: `docker-compose up --build`
- Production: Build with `Dockerfile`

## Current Technical Debt
1. **Data Model Inconsistency**: Checklist services return `Dict` instead of Pydantic models
2. **Error Handling**: Checklist tools missing proper MCP error reporting with `ctx` parameter
3. **Missing Tests**: No automated test suite yet

## Critical Files to Understand
- `main.py` - Application entry point with dual-mode support
- `server/utils/trello_api.py` - Core HTTP client implementation
- `server/services/*.py` - Business logic for each Trello entity
- `server/tools/*.py` - MCP tool interfaces

## Environment Setup
Required environment variables:
- `TRELLO_API_KEY` - Your Trello API key
- `TRELLO_TOKEN` - Your Trello token

## Known Issues
- Checklist operations need Pydantic model consistency (see server/services/checklist.py:28-32)
- Error handling inconsistency in checklist tools (server/tools/checklist.py)
- Missing test coverage across all modules

## Deployment Notes
- Supports both Claude Desktop integration and standalone SSE mode
- Fully containerized with Docker support
- Stateless design supports horizontal scaling
- Rate limited by Trello API constraints