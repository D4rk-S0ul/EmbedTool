import discord

import core


class Embeds(core.Cog):
    """Send or edit embeds!"""

    embed_group = discord.SlashCommandGroup(
        name="embed",
        description="Group of send/edit embed commands!",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @embed_group.command(name="send", description="Sends an embed to the channel specified!")
    async def embed_send(self, ctx: discord.ApplicationContext,
                         channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!",
                                                 required=False)):
        """Sends an embed to the channel specified!

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        channel: discord.abc.GuildChannel
            The channel to send the embed to."""
        if channel is None:
            channel = ctx.channel
        user_embed = discord.Embed(
            title="Embed Tool",
            description='Use the buttons below to edit the embed.\nPress "Tutorial" to hide/show the embed below.',
            color=ctx.guild.me.color
        )
        tutorial_embed = core.get_tutorial_embed(ctx=ctx)
        embed_tool = core.EmbedToolView(channel_or_message=channel, is_new_embed=True, tutorial_embed=tutorial_embed,
                                        ctx=ctx)
        await ctx.respond(embeds=[user_embed, tutorial_embed], view=embed_tool, ephemeral=True)

    @embed_group.command(name="edit", description="Edits an embed in the channel specified!")
    async def embed_edit(self, ctx: discord.ApplicationContext,
                         message_id: discord.Option(str, "Please enter the message ID!", required=True),
                         channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!",
                                                 required=False)):
        """Edits an embed in the channel specified!

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        message_id: str
            The ID of the message to edit.
        channel: discord.abc.GuildChannel
            The channel to edit the embed in."""
        if channel is None:
            channel = ctx.channel
        message = await channel.fetch_message(message_id)
        if message.author != self.bot.user:
            await ctx.respond(embed=discord.Embed(
                title="Error",
                description="Can't edit this embed as it wasn't sent by me!",
                color=discord.Color.red()
            ), ephemeral=True)
            return
        user_embed = message.embeds[0]
        tutorial_embed = core.get_tutorial_embed(ctx=ctx)
        embed_tool = core.EmbedToolView(channel_or_message=message, is_new_embed=False, tutorial_embed=tutorial_embed,
                                        ctx=ctx)
        await ctx.respond(embeds=[user_embed, tutorial_embed], view=embed_tool, ephemeral=True)


def setup(bot):
    bot.add_cog(Embeds(bot))
