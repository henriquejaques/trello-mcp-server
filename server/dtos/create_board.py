from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class BoardPermissionLevel(str, Enum):
    """Valid permission levels for a board."""
    PRIVATE = "private"
    ORG = "org"
    PUBLIC = "public"


class BoardVoting(str, Enum):
    """Valid voting settings for a board."""
    DISABLED = "disabled"
    MEMBERS = "members"
    OBSERVERS = "observers"
    ORG = "org"
    PUBLIC = "public"


class BoardComments(str, Enum):
    """Valid comment settings for a board."""
    DISABLED = "disabled"
    MEMBERS = "members"
    OBSERVERS = "observers"
    ORG = "org"
    PUBLIC = "public"


class CardAging(str, Enum):
    """Valid card aging types for a board."""
    PIRATE = "pirate"
    REGULAR = "regular"


class BoardPreferencesPayload(BaseModel):
    """
    Nested model for board preferences.
    
    Attributes:
        permissionLevel (BoardPermissionLevel): Permission level of the board.
        voting (BoardVoting): Who can vote on this board.
        comments (BoardComments): Who can comment on cards on this board.
        invitations (str): What types of members can invite users to join.
        selfJoin (bool): Whether users can join the boards themselves.
        cardCovers (bool): Whether card covers are enabled.
        background (str): Background color or image ID.
        cardAging (CardAging): Type of card aging that should take place.
    """
    
    permissionLevel: Optional[BoardPermissionLevel] = None
    voting: Optional[BoardVoting] = None
    comments: Optional[BoardComments] = None
    invitations: Optional[str] = None  # Valid: "members", "admins"
    selfJoin: Optional[bool] = None
    cardCovers: Optional[bool] = None
    background: Optional[str] = None
    cardAging: Optional[CardAging] = None

    class Config:
        use_enum_values = True


class CreateBoardPayload(BaseModel):
    """
    Payload for creating a new Trello board.
    
    Attributes:
        name (str): The name of the board (1-16384 characters).
        desc (str): A description for the board.
        defaultLabels (bool): Whether to use the default set of labels.
        defaultLists (bool): Whether to add default lists (To Do, Doing, Done).
        idOrganization (str): The ID of the organization the board should belong to.
        idBoardSource (str): The ID of a board to copy into the new board.
        keepFromSource (str): To keep cards from the original board pass "cards".
        powerUps (str): Power-Ups that should be enabled on the new board.
        prefs (BoardPreferencesPayload): Board preferences settings.
    """
    
    name: str = Field(..., min_length=1, max_length=16384, description="The name of the board to create")
    desc: Optional[str] = Field(None, description="A description for the board")
    defaultLabels: Optional[bool] = Field(True, description="Whether to use the default set of labels")
    defaultLists: Optional[bool] = Field(True, description="Whether to add default lists")
    idOrganization: Optional[str] = Field(None, description="The ID of the organization")
    idBoardSource: Optional[str] = Field(None, description="The ID of a board to copy")
    keepFromSource: Optional[str] = Field("none", description="What to keep from source board")
    powerUps: Optional[str] = Field(None, description="Power-Ups to enable")
    prefs: Optional[BoardPreferencesPayload] = Field(None, description="Board preferences")