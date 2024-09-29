import discord

async def clear_messages(interaction: discord.Interaction, limit=None):
    """Usuwa wszystkie wiadomości z kanału, lub do określonego limitu"""
    
    await interaction.response.defer(thinking=True)

    if limit is None:
        await interaction.channel.purge()
        await interaction.channel.send("Wszystkie wiadomości zostały usunięte!", delete_after=5, silent=True)
    else:
        deleted = await interaction.channel.purge(limit=limit)
        await interaction.channel.send(f"Usunięto {len(deleted)} wiadomości.", delete_after=5, silent=True)
