import discord
from discord.ext import commands

from cinevoraces.env_variables import load_env_variables, check_env_variables
from cinevoraces.movie_thread import get_thread_infos

env_variables = load_env_variables()

# Create a bot instance
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) # Create a bot instance

@bot.event
async def on_ready():
    # Check that all environment variables are defined
    check_env_variables(env_variables)
    
    channel = bot.get_channel(int(env_variables['ADMIN_CHANNEL_ID']))
    print(f"{bot.user.name} is listenning to {channel.name}")
    print("------")
    await channel.send(f"Bonjour, {bot.user.name} est à l'écoute !\nPour rappatrier le dernier film publié sur le site, entrer la commande !import_last_movie. ")
    return

# Command to import the last movie from the API and create a new thread in the forum
@bot.command()
async def import_last_movie(ctx):
    forum = bot.get_channel(int(env_variables['FORUM_ID']))

    # Get the thread infos from the API, then format them for the thread creation
    name, content, error = get_thread_infos(env_variables, forum)

    if error:
        await ctx.send(error['message'])
        return

    # Create the new thread in the forum
    await forum.create_thread(name=name, content=content)
    return

# Run the bot
bot.run(env_variables['BOT_TOKEN']) # Run the bot