import os
import platform
import traceback

import discord


class EmbedTool(discord.Bot):
    on_ready_fired: bool = False

    def __init__(self):
        super().__init__(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=f"/embed"
            ),
            help_command=None,
            owner_ids=[672768917885681678],
        )

        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                self.load_cog(f"cogs.{filename[:-3]}")

    def load_cog(self, cog: str) -> None:
        try:
            self.load_extension(cog)
        except Exception as e:
            e = getattr(e, "original", e)
            print("".join(traceback.format_exception(type(e), e, e.__traceback__)))

    async def on_ready(self):
        if self.on_ready_fired:
            return
        self.on_ready_fired = True

        msg = f"""{self.user.name} is online now!
            BotID: {self.user.id}
            Ping: {round(self.latency * 1000)} ms
            Python Version: {platform.python_version()}
            PyCord API version: {discord.__version__}"""
        print(f"\n\n{msg}\n\n")

    def run(self, token: str):
        super().run(os.environ.get(token))
