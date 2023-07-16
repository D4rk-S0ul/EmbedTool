import discord


class FooterTextModal(discord.ui.Modal):
    """Modal for receiving the footer text of an embed to send or edit."""

    def __init__(self, *args, initial_footer: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_footer: str
            The initial footer of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Embed Footer:",
                placeholder="Please enter the footer of the embed...",
                style=discord.InputTextStyle.long,
                max_length=2048,
                value=initial_footer,
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
        icon_url = user_embed.footer.icon_url
        user_embed.set_footer(text=self.children[0].value, icon_url=icon_url)
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)
