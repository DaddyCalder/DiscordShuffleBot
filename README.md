🔀 Discord Shuffle Bot
A feature-rich Discord bot that automatically shuffles and reposts a custom list of users and links at regular intervals. Perfect for promoting social media creators, rotating featured content, or displaying randomized shoutouts. Built with Python, discord.py, and Flask for uptime support.

🚀 Features:

🔁 Automatically shuffles your list every X minutes.

✍️ Allows admins to post, track, and untrack messages for auto-updating.

➕ Add or remove entries dynamically using commands.

🔗 Supports editing existing bot messages with fresh shuffled content.

🔒 Role-protected commands to prevent misuse.

🌐 Keep-alive server via Flask (ideal for Replit or other hosting platforms).


🛠️ Setup & Installation
1. Clone the repo:

git clone https://github.com/daddycalder/discordshufflebot.git

cd discordshufflebot


3. Install dependencies:

pip install -r requirements.txt


5. Create a .env file in the root directory with the following:
   
DISCORD_TOKEN=your_discord_bot_token

CHANNEL_ID=target_channel_id

ROLE_ID=admin_role_id


7. Run the bot:
   
python Shuffler.py


🔧 Configuration
You can adjust the shuffle interval and other settings in the script:

'shuffle_interval': 1800  # Time in seconds (1800s = 30 mins)

'command_prefix': '!'     # Change to your preferred prefix


💬 Bot Commands:
All commands require the user to have the configured role (ROLE_ID).

!post	Posts a new shuffled message to the configured channel and starts tracking it.

!shuffle <link>	Manually reshuffles a tracked message by its link.

!track <link>	Start auto-shuffling a previously posted bot message.

!untrack <link>	Stops auto-shuffling a specific message.

!add <name> <link>	Adds a new entry to the shuffle list. Example: !add @NewUser https://link.com

!remove <name>	Removes a user by name from the shuffle list. Partial matches allowed.


Note: Message links must follow this format:
https://discord.com/channels/<guild_id>/<channel_id>/<message_id>

🧠 How It Works:
The bot maintains an internal list of name-link pairs.

On an interval (default 30 minutes), it shuffles and updates the message content with a randomized version of the list.

Messages must be posted by the bot to be tracked or shuffled.

Commands are role-gated for security.

🌐 Keep Alive (for Replit/Free Hosting):
This bot includes a built-in Flask server to keep the bot alive when deployed on services like Replit. It listens on port 8080 and can be pinged periodically with an external uptime monitor.



If you have any request or want your own custom bot for any task at all then join our community and give myself @Matt a message or DM. :)

https://discord.gg/6eXGnRZE9V

