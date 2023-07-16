from discord.ext import commands

from .bot import EmbedTool
from .embedTool import EmbedToolView, get_tutorial_embed

__all__ = (
    "Cog",
    "EmbedTool",
    "EmbedToolView",
    "get_tutorial_embed"
)


class Cog(commands.Cog):
    """Base class for all cogs"""

    def __init__(self, bot: EmbedTool) -> None:
        self.bot: EmbedTool = bot
