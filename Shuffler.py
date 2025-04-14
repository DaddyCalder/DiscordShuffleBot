
import discord
from discord.ext import commands, tasks
import logging
import asyncio
import random
import re
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Configuration
CONFIG = {
    'token': os.getenv('DISCORD_TOKEN'),
    'command_prefix': '!',
    'shuffle_interval': 1800,  # 30 minutes in seconds
    'max_retries': 3,
    'log_level': 'INFO',
    'channel_id': int(os.getenv('CHANNEL_ID', '0')),
    'required_role_id': int(os.getenv('ROLE_ID', '0')),
}

# Validate configuration
if not CONFIG['token']:
    raise ValueError("Discord token not found in environment variables!")
if CONFIG['channel_id'] == 0:
    raise ValueError("Discord channel ID not set in environment variables!")
if CONFIG['required_role_id'] == 0:
    raise ValueError("Discord role ID not set in environment variables!")

# Initial entries list change this to your own users & links, This can be added & removed from without editing code
entries = [
    {"@name": "- @ChoccyMarino", "link": "https://www.instagram.com/someartonacanvas"},
    {"@name": "- @turbotony", "link": "https://www.facebook.com/share/1CUudTMy8c/"},
    {"@name": "- @AnomalyArchive", "link": "https://www.tiktok.com/@anomalyarchive01"},
    {"@name": "- @Chucci", "link": "https://www.instagram.com/someartonacanvas"},
    {"@name": "- @Draingang.co", "link": "https://www.instagram.com/underground.ai"},
    {"@name": "- @DronesMid", "link": "https://www.tiktok.com/@ufocasefiles"},
    {"@name": "- @Dubsy", "link": "https://www.tiktok.com/@pxlsqshr"},
    {"@name": "- @EXPMNT", "link": "https://www.tiktok.com/@the_ai_experiment"},
    {"@name": "- @Fiend", "link": "https://www.tiktok.com/@fiendcore"},
    {"@name": "- @impossiblecore.ai", "link": "https://www.tiktok.com/@impossiblecore.ai"},
    {"@name": "- @Julia", "link": "https://www.tiktok.com/@hauntantica"},
    {"@name": "- @Max", "link": "https://www.instagram.com/visionart.ai"},
    {"@name": "- @Myles", "link": "https://www.tiktok.com/@druid.art"},
    {"@name": "- @myst", "link": "https://www.instagram.com/myst.cult/"},
    {"@name": "- @NightTerrorZzz", "link": "https://www.tiktok.com/@nightterrorzzz"},
    {"@name": "- @Pastor", "link": "https://www.tiktok.com/@pastor_fussycat"},
    {"@name": "- @piptycoon", "link": "https://www.tiktok.com/@darcckore"},
    {"@name": "- @PromptMonster", "link": "https://www.tiktok.com/@prompt_monster"},
    {"@name": "- @RetroFACE", "link": "https://www.instagram.com/retroface.official/"},
    {"@name": "- @Scruff", "link": "https://www.tiktok.com/@strangeai"},
    {"@name": "- @The5_1", "link": "https://www.adamantarsenal.com/"},
    {"@name": "- @rift", "link": "https://www.instagram.com/riftsurge_"}
]

# Setup logging
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(CONFIG['log_level'])
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

logger = setup_logging()

# Flask app for keep_alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Utility functions
def parse_message_link(link: str) -> tuple:
    pattern = r"https?://discord\.com/channels/(\d+)/(\d+)/(\d+)"
    match = re.match(pattern, link)
    if not match:
        raise ValueError("Invalid Discord message link format")
    return tuple(map(int, match.groups()))

def shuffle_list_content(content: str = None) -> str:
    try:
        if content:
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            random.shuffle(non_empty_lines)
            return '\n'.join(non_empty_lines)
        else:
            shuffled_entries = entries.copy()
            random.shuffle(shuffled_entries)
            formatted_entries = []
            for entry in shuffled_entries:
                formatted_entries.extend([
                    f"**{entry['@name']}**",
                    entry['link'],
                    ""
                ])
            return "**Updated List:**\n\n" + "\n".join(formatted_entries[:-1])
    except Exception as e:
        logger.error(f"Error shuffling content: {e}")
        raise

def add_entry(name: str, link: str) -> str:
    global entries
    try:
        new_entry = {"@name": f"@{name}", "link": link}
        entries.append(new_entry)
        return f"Added {new_entry['@name']} with link {link} to the list."
    except Exception as e:
        logger.error(f"Error adding entry: {e}")
        raise

def remove_entry(name: str) -> str:
    global entries
    try:
        initial_length = len(entries)
        entries = [entry for entry in entries if name.lower() not in entry['@name'].lower()]
        if len(entries) == initial_length:
            return "No matching entry found."
        return f"Removed {name} from the list."
    except Exception as e:
        logger.error(f"Error removing entry: {e}")
        raise

async def get_message_from_link(bot: discord.Client, link: str) -> discord.Message:
    try:
        guild_id, channel_id, message_id = parse_message_link(link)
        guild = bot.get_guild(guild_id)
        if not guild:
            raise ValueError("Guild not found")
        channel = guild.get_channel(channel_id)
        if not channel:
            raise ValueError("Channel not found")
        message = await channel.fetch_message(message_id)
        if not message:
            raise ValueError("Message not found")
        return message
    except Exception as e:
        logger.error(f"Error retrieving message: {e}")
        raise

# Bot setup
def setup_bot_intents():
    intents = discord.Intents.default()
    intents.message_content = True
    logger.info("Bot intents configured: message_content=%s", intents.message_content)
    return intents

bot = commands.Bot(command_prefix=CONFIG['command_prefix'], intents=setup_bot_intents())

# ShuffleCommands cog
class ShuffleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_messages = set()
        self.periodic_shuffle.start()

    def cog_unload(self):
        self.periodic_shuffle.cancel()

    @tasks.loop(seconds=CONFIG['shuffle_interval'])
    async def periodic_shuffle(self):
        logger.info(f"Running periodic shuffle")
        for message_link in self.active_messages.copy():
            try:
                message = await get_message_from_link(self.bot, message_link)
                shuffled_content = shuffle_list_content() 
                await message.edit(content=shuffled_content)
                logger.info(f"Successfully shuffled message {message.id}")
            except Exception as e:
                logger.error(f"Failed to shuffle message {message_link}: {e}")
                self.active_messages.remove(message_link)

    @commands.command(name='post')
    @commands.has_role(CONFIG['required_role_id'])
    async def post_initial_message(self, ctx):
        try:
            channel = self.bot.get_channel(CONFIG['channel_id'])
            if not channel:
                await ctx.send("Could not find the configured channel!")
                return
            initial_content = shuffle_list_content()
            message = await channel.send(initial_content)
            message_link = f"https://discord.com/channels/{ctx.guild.id}/{channel.id}/{message.id}"
            self.active_messages.add(message_link)
            await ctx.send(f"Posted and tracking new message! Use this link to reference it: {message_link}")
        except Exception as e:
            logger.error(f"Error in post command: {e}")
            await ctx.send(f"Failed to post message: {str(e)}")

    @commands.command(name='shuffle')
    @commands.has_role(CONFIG['required_role_id'])
    async def shuffle_message(self, ctx, message_link: str):
        try:
            message = await get_message_from_link(self.bot, message_link)
            if message.author != self.bot.user:
                await ctx.send("I can only shuffle messages that I created!")
                return
            shuffled_content = shuffle_list_content()
            await message.edit(content=shuffled_content)
            await ctx.send("Message shuffled successfully!")
        except Exception as e:
            logger.error(f"Error in shuffle command: {e}")
            await ctx.send(f"Failed to shuffle message: {str(e)}")

    @commands.command(name='track')
    @commands.has_role(CONFIG['required_role_id'])
    async def track_message(self, ctx, message_link: str):
        try:
            message = await get_message_from_link(self.bot, message_link)
            if message.author != self.bot.user:
                await ctx.send("I can only track messages that I created!")
                return
            self.active_messages.add(message_link)
            await ctx.send("Message is now being tracked for periodic shuffling!")
        except Exception as e:
            logger.error(f"Error in track command: {e}")
            await ctx.send(f"Failed to track message: {str(e)}")

    @commands.command(name='untrack')
    @commands.has_role(CONFIG['required_role_id'])
    async def untrack_message(self, ctx, message_link: str):
        try:
            if message_link in self.active_messages:
                self.active_messages.remove(message_link)
                await ctx.send("Message is no longer being tracked!")
            else:
                await ctx.send("This message was not being tracked!")
        except Exception as e:
            logger.error(f"Error in untrack command: {e}")
            await ctx.send(f"Failed to untrack message: {str(e)}")

    @commands.command(name='add')
    @commands.has_role(CONFIG['required_role_id'])
    async def add_entry_command(self, ctx, name: str, link: str):
        try:
            result = add_entry(name, link)
            await ctx.send(result)
        except Exception as e:
            logger.error(f"Error in add command: {e}")
            await ctx.send(f"Failed to add entry: {str(e)}")

    @commands.command(name='remove')
    @commands.has_role(CONFIG['required_role_id'])
    async def remove_entry_command(self, ctx, name: str):
        try:
            result = remove_entry(name)
            await ctx.send(result)
        except Exception as e:
            logger.error(f"Error in remove command: {e}")
            await ctx.send(f"Failed to remove entry: {str(e)}")

@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')
    try:
        await bot.add_cog(ShuffleCommands(bot))
        logger.info('Loaded shuffle commands cog')
    except Exception as e:
        logger.error(f'Failed to load shuffle commands cog: {e}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command!")
    elif isinstance(error, discord.errors.PrivilegedIntentsRequired):
        error_message = (
            "The bot requires the 'Message Content Intent' to be enabled in the Discord Developer Portal. "
            "Please enable it at https://discord.com/developers/applications"
        )
        logger.critical(error_message)
        await ctx.send(error_message)
    else:
        logger.error(f'An error occurred: {error}')
        await ctx.send(f"An error occurred: {str(error)}")

def main():
    try:
        logger.info("Starting bot...")
        keep_alive()
        bot.run(CONFIG['token'])
    except discord.errors.PrivilegedIntentsRequired:
        logger.critical("Failed to start bot: Message Content Intent is not enabled in Discord Developer Portal")
        raise
    except Exception as e:
        logger.critical(f'Failed to start bot: {e}')
        raise

if __name__ == '__main__':
    main()
