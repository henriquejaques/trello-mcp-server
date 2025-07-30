"""
This module contains tools for managing Trello boards.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloBoard, TrelloLabel
from server.services.board import BoardService
from server.dtos.create_board import CreateBoardPayload
from server.trello import client

logger = logging.getLogger(__name__)

service = BoardService(client)


async def get_board(ctx: Context, board_id: str) -> TrelloBoard:
    """Retrieves a specific board by its ID.

    Args:
        board_id (str): The ID of the board to retrieve.

    Returns:
        TrelloBoard: The board object containing board details.
    """
    try:
        logger.info(f"Getting board with ID: {board_id}")
        result = await service.get_board(board_id)
        logger.info(f"Successfully retrieved board: {board_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get board: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_board_labels(ctx: Context, board_id: str) -> List[TrelloLabel]:
    """Retrieves all labels for a specific board.
    Args:
        board_id (str): The ID of the board whose labels to retrieve.
    Returns:
        List[TrelloLabel]: A list of label objects for the board.
    """
    try:
        logger.info(f"Getting labels for board: {board_id}")
        result = await service.get_board_labels(board_id)
        logger.info(
            f"Successfully retrieved {len(result)} labels for board: {board_id}"
        )
        return result
    except Exception as e:
        error_msg = f"Failed to get board labels: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_boards(ctx: Context) -> List[TrelloBoard]:
    """Retrieves all boards for the authenticated user.

    Returns:
        List[TrelloBoard]: A list of board objects.
    """
    try:
        logger.info("Getting all boards")
        result = await service.get_boards()
        logger.info(f"Successfully retrieved {len(result)} boards")
        return result
    except Exception as e:
        error_msg = f"Failed to get boards: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def create_board(ctx: Context, payload: CreateBoardPayload) -> TrelloBoard:
    """Creates a new board.

    Args:
        ctx: MCP context for error reporting.
        payload: Board creation parameters.

    Returns:
        TrelloBoard: The newly created board object.
    """
    try:
        logger.info(f"Creating board: {payload.name}")
        result = await service.create_board(payload)
        logger.info(f"Successfully created board '{result.name}' with ID: {result.id}")
        return result
    except Exception as e:
        error_msg = f"Failed to create board '{payload.name}': {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
