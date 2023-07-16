import discord
from discord.ext import commands


class TitleModal(discord.ui.Modal):
    """Modal for receiving the title of an embed to send or edit."""

    def __init__(self, *args, initial_title: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_title: str
            The initial title of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Embed Title:",
                placeholder="Please enter the title of the embed...",
                style=discord.InputTextStyle.long,
                max_length=256,
                value=initial_title,
                required=False
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Callback for when the modal is submitted.

        Parameters
        ------------
        interaction: discord.Interaction
            The interaction that submitted the modal."""
        user_embed: discord.Embed = interaction.message.embeds[0]
        user_embed.title = self.children[0].value
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class DescriptionModal(discord.ui.Modal):
    """Modal for receiving the description of an embed to send or edit."""

    def __init__(self, *args, initial_description: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_description: str
            The initial description of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Embed Description:",
                placeholder="Please enter the description of the embed...",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=initial_description,
                required=False
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Callback for when the modal is submitted.

        Parameters
        ------------
        interaction: discord.Interaction
            The interaction that submitted the modal."""
        user_embed: discord.Embed = interaction.message.embeds[0]
        user_embed.description = self.children[0].value
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class ColorModal(discord.ui.Modal):
    """Modal for receiving the color of an embed to send or edit."""

    def __init__(self, *args, initial_color: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_color: str
            The initial color of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Embed Color:",
                placeholder="Please enter the HEX code of the color of the embed...",
                style=discord.InputTextStyle.short,
                max_length=7,
                value=initial_color,
                required=False
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Callback for when the modal is submitted.

        Parameters
        ------------
        interaction: discord.Interaction
            The interaction that submitted the modal."""
        user_embed: discord.Embed = interaction.message.embeds[0]
        color_string = self.children[0].value
        color = await commands.ColorConverter().convert(interaction, color_string)
        user_embed.colour = color
        if self.tutorial_embed:
            self.tutorial_embed.colour = color
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        """Callback for when the modal has an error.

        Parameters
        ------------
        error: Exception
            The error that occurred.
        interaction: discord.Interaction
            The interaction that submitted the modal."""
        if isinstance(error, commands.BadArgument):
            await interaction.response.send_message(embed=discord.Embed(
                title="Invalid Color",
                description="The color you entered is invalid. Please try again using a valid HEX code.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        raise error
