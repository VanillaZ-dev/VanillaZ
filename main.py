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
async def update_status():
    print("🔄 Updating player count...")
    try:
        response = requests.get(API_URL, headers=HEADERS)
        if response.status_code == 200:
            data = response.json().get("data", {})
            players = data.get("players", {}).get("connected", 0)
            max_players = data.get("players", {}).get("slots", 0)
            status = f"{players}/{max_players} online"
        else:
            status = "API error"
    except Exception as e:
        print(f"❌ Error: {e}")
        status = "Error"

    await client.change_presence(activity=discord.Game(name=status))

client.run(DISCORD_TOKEN)
