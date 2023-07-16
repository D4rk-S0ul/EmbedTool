import discord


class ThumbnailModal(discord.ui.Modal):
    """Modal for receiving the thumbnail of an embed to send or edit."""

    def __init__(self, *args, initial_thumbnail_url: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_thumbnail_url: str
            The initial thumbnail url of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Thumbnail URL:",
                placeholder="Please enter Thumbnail URL of the embed...",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=initial_thumbnail_url,
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
        user_embed.set_thumbnail(url=self.children[0].value)
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class ImageModal(discord.ui.Modal):
    """Modal for receiving the image of an embed to send or edit."""

    def __init__(self, *args, initial_image_url: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_image_url: str
            The initial image url of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Image URL:",
                placeholder="Please enter Image URL of the embed...",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=initial_image_url,
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
        user_embed.set_image(url=self.children[0].value)
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class FooterImageModal(discord.ui.Modal):
    """Modal for receiving the footer image of an embed to send or edit."""

    def __init__(self, *args, initial_footer_image_url: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_footer_image_url: str
            The initial footer image url of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Footer Image URL:",
                placeholder="Please enter Footer Image URL of the embed...",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=initial_footer_image_url,
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
        user_embed.footer.icon_url = self.children[0].value
        footer_text = user_embed.footer.text
        if footer_text is discord.Embed.Empty:
            footer_text = "⠀"
        user_embed.set_footer(text=footer_text, icon_url=self.children[0].value)
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)
