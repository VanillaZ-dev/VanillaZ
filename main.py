import os
import requests
import discord
from discord.ext import tasks
from threading import Thread

# Load secrets
API_TOKEN = os.getenv("API_TOKEN")
SERVER_ID = os.getenv("SERVER_ID")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}
API_URL = f"https://api.cftools.cloud/v1/server/{SERVER_ID}/info"

# Discord bot setup
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    update_status.start()

@tasks.loop(minutes=5)
def get_player_count():
    url = f"https://api.cftools.cloud/v1/server/{os.getenv('SERVER_ID')}/current-player-count"
    headers = {
        "Authorization": f"Bearer {os.getenv('API_TOKEN')}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]["player_count"]
    else:
        print("CF Tools API Error:", response.status_code, response.text)
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        status = "Error"

    await client.change_presence(activity=discord.Game(name=status))

client.run(DISCORD_TOKEN)
