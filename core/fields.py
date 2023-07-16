import discord


class AddFieldModal(discord.ui.Modal):
    """Modal for receiving a field to be added to an embed to send or edit."""

    def __init__(self, *args, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Field Title:",
                placeholder="Please enter the title of the field...",
                style=discord.InputTextStyle.long,
                max_length=256,
                required=False
            ),
            discord.ui.InputText(
                label="Field Value:",
                placeholder="Please enter the value of the field...",
                style=discord.InputTextStyle.long,
                max_length=1024,
                required=False
            ),
            discord.ui.InputText(
                label="Inline:",
                placeholder="Whether the field should be inline (True/False)...",
                style=discord.InputTextStyle.short,
                max_length=5,
                required=True
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
        title = self.children[0].value
        value = self.children[1].value
        inline_str = self.children[2].value.lower()
        if inline_str in ["true", "1"]:
            inline = True
        elif inline_str in ["false", "0"]:
            inline = False
        else:
            await interaction.response.send_message(embed=discord.Embed(
                title="Invalid Inline",
                description="The inline value you entered is invalid. Please try again using True or False.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        user_embed.add_field(name=title, value=value, inline=inline)
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class RemoveFieldView(discord.ui.View):
    """View for removing a field from an embed."""

    def __init__(self, *args, ctx: discord.ApplicationContext, user_embed: discord.Embed, tutorial_embed=None,
                 options: list[discord.SelectOption], **kwargs):
        """Initialize the view.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial.
        options: list[discord.SelectOption]
            The options to show in the select."""
        self.ctx: discord.ApplicationContext = ctx
        self.user_embed: discord.Embed = user_embed
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(*args, **kwargs)
        self.remove_field.options = options

    @discord.ui.string_select(placeholder="Please select a field to remove...")
    async def remove_field(self, select: discord.ui.Select, interaction: discord.Interaction) -> None:
        """Callback for when a field is selected to be removed.

        Parameters
        ------------
        select: discord.ui.Select
            The select that was used to select the field.
        interaction: discord.Interaction
            The interaction that selected the field."""
        print("remove field inside view")
        await interaction.response.defer()
        field_index: int = int(select.values[0])
        self.user_embed.remove_field(field_index)
        if self.tutorial_embed:
            await self.ctx.edit(embeds=[self.user_embed, self.tutorial_embed])
            return
        await self.ctx.edit(embed=self.user_embed)
        await interaction.delete_original_response()


class EditFieldView(discord.ui.View):
    """View for editing a field from an embed."""

    def __init__(self, *args, ctx: discord.ApplicationContext, user_embed: discord.Embed, tutorial_embed=None,
                 options: list[discord.SelectOption], **kwargs):
        """Initialize the view.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial.
        options: list[discord.SelectOption]
            The options to show in the select."""
        self.ctx: discord.ApplicationContext = ctx
        self.user_embed: discord.Embed = user_embed
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(*args, **kwargs)
        self.edit_field.options = options

    @discord.ui.string_select(placeholder="Please select a field to remove...")
    async def edit_field(self, select: discord.ui.Select, interaction: discord.Interaction) -> None:
        """Callback for when a field is selected to be removed.

        Parameters
        ------------
        select: discord.ui.Select
            The select that was used to select the field.
        interaction: discord.Interaction
            The interaction that selected the field."""
        field_index: int = int(select.values[0])
        await interaction.response.send_modal(
            EditFieldModal(
                ctx=self.ctx,
                title="Edit a Field",
                user_embed=self.user_embed,
                tutorial_embed=self.tutorial_embed,
                field_index=field_index)
        )
        await interaction.delete_original_response()


class EditFieldModal(discord.ui.Modal):
    """Modal for editing a field in an embed."""

    def __init__(self, *args, ctx: discord.ApplicationContext, user_embed: discord.Embed, tutorial_embed=None,
                 field_index: int, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.ctx: discord.ApplicationContext = ctx
        self.user_embed: discord.Embed = user_embed
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        self.field_index: int = field_index
        super().__init__(
            discord.ui.InputText(
                label="Field Title:",
                placeholder="Please enter the title of the field...",
                style=discord.InputTextStyle.long,
                max_length=256,
                value=self.user_embed.fields[self.field_index].name,
                required=False
            ),
            discord.ui.InputText(
                label="Field Value:",
                placeholder="Please enter the value of the field...",
                style=discord.InputTextStyle.long,
                max_length=1024,
                value=self.user_embed.fields[self.field_index].value,
                required=False
            ),
            discord.ui.InputText(
                label="Inline:",
                placeholder="Whether the field should be inline (True/False)...",
                style=discord.InputTextStyle.short,
                max_length=5,
                value=str(self.user_embed.fields[self.field_index].inline),
                required=True
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
        await interaction.response.defer()
        title = self.children[0].value
        value = self.children[1].value
        inline_str = self.children[2].value.lower()
        if inline_str in ["true", "1"]:
            inline = True
        elif inline_str in ["false", "0"]:
            inline = False
        else:
            await interaction.response.send_message(embed=discord.Embed(
                title="Invalid Inline",
                description="The inline value you entered is invalid. Please try again using True or False.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        self.user_embed.set_field_at(index=self.field_index, name=title, value=value, inline=inline)
        if self.tutorial_embed:
            await self.ctx.edit(embeds=[self.user_embed, self.tutorial_embed])
            return
        await self.ctx.edit(embed=self.user_embed)
