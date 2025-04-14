
A Discord bot that posts and periodically shuffles a list of usernames and links (such as social media profiles or promotions) in a specific channel. Ideal for rotating exposure for artists, creators, or community projects.

---

## 🔧 Features

- ✅ Periodically shuffles a list every X minutes (default: 30min).
- 🔁 Supports manual shuffle on command.
- ➕ Add new users/links via command.
- ➖ Remove users/links via command.
- 🔍 Track specific messages to be shuffled.
- 🚫 Untrack messages from auto-shuffle.
- 🛠️ Flask server integration for hosting environments (like Replit).
- 🛡️ Role-based access to commands.

---

## 📦 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure you have the following installed:
- `discord.py`
- `python-dotenv`
- `flask`

### 2. Environment Variables

Create a `.env` file in the root folder with the following content:

```
DISCORD_TOKEN=your_discord_bot_token
CHANNEL_ID=channel_for_the_bot_to_post_and_track
ROLE_ID=your_bots_role
```

### 3. Running the Bot

```bash
python shuffler.py
```

---

## ⚙️ Commands

All commands are prefixed with `!` by default.

| Command | Description |
|--------|-------------|
| `!post` | Posts the current shuffled list and begins auto-shuffling it every X minutes |
| `!shuffle <message_link>` | Manually reshuffles a bot message |
| `!track <message_link>` | Begins auto-shuffling a specific message |
| `!untrack <message_link>` | Stops auto-shuffling a message |
| `!add <name> <link>` | Adds a new user/link to the list |
| `!remove <name>` | Removes a user/link from the list |

**Note:** These commands require the configured role ID to be used.

---

## 🧪 Example Entry Format

```python
entries = [
    {"@name": "- @YourName", "link": "https://your-social-link.com"},
    ...
]
```

---

## 🌐 Hosting

This bot uses a simple Flask server (`keep_alive`) to stay online in hosting platforms like Replit. If not needed, you can remove this part.

---

## 🛠️ Customization

- To change the shuffle interval, update `shuffle_interval` in `CONFIG`.
- To modify the list of entries manually, edit the `entries` list directly in `shuffler.py`.

---

## 🤖 Permissions Required

Make sure your bot has:
- **Message Content Intent** enabled in the [Discord Developer Portal](https://discord.com/developers/applications).
- Permissions to manage messages in the target channel.

---

# If you have any request or want your own custom bot for any task at all then join our community and give myself @Matt a message or DM. :)

- https://discord.gg/6eXGnRZE9V

