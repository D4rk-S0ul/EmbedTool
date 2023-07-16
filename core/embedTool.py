import discord

from .fields import AddFieldModal, RemoveFieldView, EditFieldView
from .general import TitleModal, DescriptionModal, ColorModal
from .images import ThumbnailModal, ImageModal, FooterImageModal
from .options import FooterTextModal


class EmbedToolView(discord.ui.View):
    """View for the embed tool."""

    def __init__(self, *args, channel_or_message: discord.abc.GuildChannel | discord.Message, is_new_embed: bool,
                 tutorial_embed: discord.Embed, ctx: discord.ApplicationContext, **kwargs):
        """Initializes the view.

        Parameters
        ------------
        channel_or_message: discord.abc.GuildChannel or discord.Message
            The channel to send the embed in or the message to edit.
        is_new_embed: bool
            Whether the embed is new or not. Decides whether to send or edit the embed.
        tutorial_embed: discord.Embed
            The tutorial embed to show.
        ctx: discord.ApplicationContext
            The context used for command invocation."""
        super().__init__(*args, disable_on_timeout=True, **kwargs)
        self.is_new_embed: bool = is_new_embed
        if self.is_new_embed:
            self.channel: discord.abc.GuildChannel = channel_or_message
        else:
            self.message = channel_or_message
            self.channel = self.message.channel
        self.tutorial_embed: discord.Embed = tutorial_embed
        self.ctx: discord.ApplicationContext = ctx
        self.tutorial_hidden: bool = False
        self.author_hidden: bool = True
        self.timestamp_hidden: bool = True
        self.canceled_before: bool = False

    @discord.ui.button(label="GENERALﾠ", style=discord.ButtonStyle.blurple, disabled=True, row=0)
    async def general_row(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="⠀ﾠTitleﾠ⠀", style=discord.ButtonStyle.gray, row=0)
    async def set_title(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the title button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_title = interaction.message.embeds[0].title
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            TitleModal(title="Set the Embed Title", initial_title=initial_title, tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="Description", style=discord.ButtonStyle.gray, row=0)
    async def set_description(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the description button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_description = interaction.message.embeds[0].description
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            DescriptionModal(title="Set the Embed Description", initial_description=initial_description,
                             tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="ﾠ⠀Colorﾠ⠀", style=discord.ButtonStyle.gray, row=0)
    async def set_color(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the color button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_color = str(interaction.message.embeds[0].color)
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            ColorModal(title="Set the Embed Color", initial_color=initial_color, tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="FIELDSﾠﾠﾠ", style=discord.ButtonStyle.blurple, disabled=True, row=1)
    async def fields_row(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="ﾠﾠﾠAddﾠ⠀", style=discord.ButtonStyle.gray, row=1)
    async def add_field(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the add field button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            AddFieldModal(title="Add a Field", tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="ﾠRemoveﾠﾠ", style=discord.ButtonStyle.gray, row=1)
    async def remove_field(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the remove field button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        fields = interaction.message.embeds[0].fields
        if not fields:
            await interaction.response.send_message(embed=discord.Embed(
                title="Error",
                description="There are no fields to remove.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        options = []
        for index, field in enumerate(fields):
            options.append(discord.SelectOption(label=field.name, description=field.value, value=str(index)))
        await interaction.response.send_message(embed=discord.Embed(
            title="Remove a Field",
            description="Select the field you want to remove.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), view=RemoveFieldView(
            ctx=self.ctx,
            user_embed=interaction.message.embeds[0],
            tutorial_embed=tutorial_embed,
            options=options
        ), ephemeral=True)

    @discord.ui.button(label="ﾠﾠﾠEditﾠﾠﾠ", style=discord.ButtonStyle.gray, row=1)
    async def edit_field(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the edit field button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        fields = interaction.message.embeds[0].fields
        if not fields:
            await interaction.response.send_message(embed=discord.Embed(
                title="Error",
                description="There are no fields to edit.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        options = []
        for index, field in enumerate(fields):
            options.append(discord.SelectOption(label=field.name, description=field.value, value=str(index)))
        await interaction.response.send_message(embed=discord.Embed(
            title="Edit a Field",
            description="Select the field you want to edit.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), view=EditFieldView(
            ctx=self.ctx,
            user_embed=interaction.message.embeds[0],
            tutorial_embed=tutorial_embed,
            options=options
        ), ephemeral=True)

    @discord.ui.button(label="IMAGESﾠﾠ", style=discord.ButtonStyle.blurple, disabled=True, row=2)
    async def images_row(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="Thumbnail", style=discord.ButtonStyle.gray, row=2)
    async def set_thumbnail(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the thumbnail button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_thumbnail_url = interaction.message.embeds[0].thumbnail.url
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            ThumbnailModal(title="Set the Thumbnail", initial_thumbnail_url=initial_thumbnail_url,
                           tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="⠀ﾠImage⠀ﾠ", style=discord.ButtonStyle.gray, row=2)
    async def set_image(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the image button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_image_url = interaction.message.embeds[0].image.url
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            ImageModal(title="Set the Image", initial_image_url=initial_image_url, tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="ﾠﾠFooterﾠﾠ", style=discord.ButtonStyle.gray, row=2)
    async def set_footer_image(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the footer image button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_footer_icon_url = interaction.message.embeds[0].footer.icon_url
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            FooterImageModal(title="Set the Footer Image", initial_footer_image_url=initial_footer_icon_url,
                             tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="OPTIONSﾠ", style=discord.ButtonStyle.blurple, disabled=True, row=3)
    async def options_row(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="ﾠAuthorﾠﾠ", style=discord.ButtonStyle.gray, row=3)
    async def set_author(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the author button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        user_embed = interaction.message.embeds[0]
        if self.author_hidden:
            self.author_hidden = False
            user_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        else:
            self.author_hidden = True
            user_embed.remove_author()
        if not self.tutorial_hidden:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)

    @discord.ui.button(label="ﾠﾠFooterﾠﾠ", style=discord.ButtonStyle.gray, row=3)
    async def set_footer_text(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the footer text button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_footer = interaction.message.embeds[0].footer.text
        if initial_footer == "⠀":
            initial_footer = None
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            FooterTextModal(title="Set the Embed Description", initial_footer=initial_footer,
                            tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="Timestamp", style=discord.ButtonStyle.gray, row=3)
    async def set_timestamp(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the timestamp button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        user_embed = interaction.message.embeds[0]
        if self.timestamp_hidden:
            self.timestamp_hidden = False
            user_embed.timestamp = discord.utils.utcnow()
        else:
            self.timestamp_hidden = True
            user_embed.timestamp = discord.Embed.Empty
        if not self.tutorial_hidden:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)

    @discord.ui.button(label="SETTINGS", style=discord.ButtonStyle.blurple, disabled=True, row=4)
    async def settings_row(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="⠀ﾠSend⠀⠀", style=discord.ButtonStyle.green, row=4)
    async def send_embed(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the send button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        user_embed = interaction.message.embeds[0]
        await interaction.response.defer()
        if self.is_new_embed:
            message = await self.channel.send(embed=user_embed)
            await interaction.followup.send(embed=discord.Embed(
                title="Embed Send",
                description=f"[Jump to message]({message.jump_url})",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
        else:
            await self.message.edit(embed=user_embed)
            await interaction.followup.send(embed=discord.Embed(
                title="Embed Edited",
                description=f"[Jump to message]({self.message.jump_url})",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
        await interaction.delete_original_response()

    @discord.ui.button(label="ﾠTutorialﾠﾠ", style=discord.ButtonStyle.gray, row=4)
    async def show_tutorial(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the tutorial button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        user_embed = interaction.message.embeds[0]
        if self.tutorial_hidden:
            self.tutorial_hidden = False
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        self.tutorial_hidden = True
        await interaction.response.edit_message(embed=user_embed)

    @discord.ui.button(label="ﾠﾠCancelﾠﾠ", style=discord.ButtonStyle.red, row=4)
    async def cancel_editing(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the cancel button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        if self.canceled_before:
            await interaction.response.defer()
            await interaction.delete_original_response()
            return
        self.canceled_before = True
        button.label = "ﾠConfirmﾠﾠ"
        await interaction.response.edit_message(view=self)


def get_tutorial_embed(ctx: discord.ApplicationContext) -> discord.Embed:
    """Returns the tutorial embed.

    Parameters
    ------------
    ctx: discord.ApplicationContext
        The context used for command invocation."""
    tutorial_embed = discord.Embed(
        title="Title",
        description="Description",
        color=ctx.guild.me.color,
        timestamp=discord.utils.utcnow()
    )
    tutorial_embed.add_field(name="Inline Field 1", value="← Color sets color of the bar on the left!")
    tutorial_embed.add_field(name="Inline Field 2", value="Value 2")
    tutorial_embed.add_field(name="Inline Field 3", value="Inline fields will be next to each other!")
    tutorial_embed.add_field(name="Non-inline Field", value="Value", inline=False)
    tutorial_embed.set_author(name="Author", icon_url=ctx.guild.me.avatar.url)
    tutorial_embed.set_footer(text="Footer", icon_url="https://cdn.discordapp.com/attachments/751512715872436416"
                                                      "/1125701630273261629/13YRA70M.png")
    tutorial_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/751512715872436416"
                                     "/1125132998967304412/t6HnzvR8.png")
    tutorial_embed.set_image(url="https://cdn.discordapp.com/attachments/751512715872436416/1125132939160731799"
                                 "/kJ9NYtR1.png")
    return tutorial_embed
