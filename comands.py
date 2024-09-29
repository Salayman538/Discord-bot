import typing
import discord
from discord.ext import commands
from discord import app_commands
from comands_functions.clear import clear_messages
from comands_functions.odrabiamy import odrabiamy_get_answers

books = ["matematyka - podręcznik", "matematyka - karty pracy"]

books_numbers = {
    "matematyka - podręcznik": "matematyka/ksiazka-13468",
    "matematyka - karty pracy": "matematyka/ksiazka-13084"
}

def setup(bot):
    @bot.tree.command()
    async def clear(interaction: discord.Interaction, limit: int = None):
        await clear_messages(interaction, limit)

    # Obsługa błędów dla komendy clear
    @clear.error
    async def clear_error(interaction: discord.Interaction, error):
        if error:
            await interaction.channel.send("Wystąpił błąd przy usuwaniu wiadomości.", silent=True)
            await interaction.channel.send(error, silent=True)

    @bot.tree.command()
    @app_commands.describe(book="Wybierz, który podręcznik", page="Wpisz, która strona")
    @app_commands.rename(book="podręcznik", page="strona")
    async def odrabiamy(interaction: discord.Interaction, book: str, page: int):
        await interaction.response.send_message("Daj chwilę", silent=True)
        await odrabiamy_get_answers(interaction, book, page)

    # autouzupełnianie dla argumentu "podręcznik" przy wpisywaniu komendy
    @odrabiamy.autocomplete("book")
    async def odrabiamy_autocompetion(
        interaction: discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for odrabiamy_choice in books:
            if current.lower() in odrabiamy_choice.lower():
                data.append(app_commands.Choice(name=odrabiamy_choice, value=books_numbers[odrabiamy_choice]))
        return data

    # Obsługa błędów dla komendy odrabiamy
    @odrabiamy.error
    async def odrabiamy_error(interaction: discord.Interaction, error):
        if error:
            await interaction.channel.send("Wystąpił błąd przy przetwarzaniu komendy odrabiamy.", silent=True)
            await interaction.channel.send(error, silent=True)