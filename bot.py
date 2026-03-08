import discord
from discord import app_commands
import requests
import socket
import os

from keep_alive import keep_alive

class WultiBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"WULTI Bot connecté en tant que {self.user}")
        await self.tree.sync()
        print("Slash commands synchronisées.")

bot = WultiBot()

# ============================
#        /ip
# ============================
@bot.tree.command(name="ip", description="Analyse une adresse IP")
async def ip(interaction: discord.Interaction, adresse_ip: str):
    try:
        url = f"http://ip-api.com/json/{adresse_ip}"
        data = requests.get(url).json()

        if data["status"] == "fail":
            await interaction.response.send_message("❌ IP invalide ou introuvable.")
            return

        message = (
            f"🌍 **Informations sur l'IP : {adresse_ip}**\n"
            f"• Pays : {data.get('country', 'N/A')}\n"
            f"• Région : {data.get('regionName', 'N/A')}\n"
            f"• Ville : {data.get('city', 'N/A')}\n"
            f"• FAI : {data.get('isp', 'N/A')}\n"
            f"• Latitude : {data.get('lat', 'N/A')}\n"
            f"• Longitude : {data.get('lon', 'N/A')}\n"
        )

        await interaction.response.send_message(message)

    except:
        await interaction.response.send_message("⚠️ Une erreur est survenue.")

# ============================
#        /geo
# ============================
@bot.tree.command(name="geo", description="Géolocalisation détaillée d'une IP")
async def geo(interaction: discord.Interaction, adresse_ip: str):
    try:
        url = f"http://ip-api.com/json/{adresse_ip}?fields=66846719"
        data = requests.get(url).json()

        if data["status"] == "fail":
            await interaction.response.send_message("❌ IP invalide ou introuvable.")
            return

        message = (
            f"🛰️ **Géolocalisation détaillée : {adresse_ip}**\n"
            f"• Pays : {data.get('country', 'N/A')}\n"
            f"• Code pays : {data.get('countryCode', 'N/A')}\n"
            f"• Région : {data.get('regionName', 'N/A')}\n"
            f"• Ville : {data.get('city', 'N/A')}\n"
            f"• Code postal : {data.get('zip', 'N/A')}\n"
            f"• Fuseau horaire : {data.get('timezone', 'N/A')}\n"
            f"• FAI : {data.get('isp', 'N/A')}\n"
            f"• Organisation : {data.get('org', 'N/A')}\n"
            f"• AS : {data.get('as', 'N/A')}\n"
            f"• Latitude : {data.get('lat', 'N/A')}\n"
            f"• Longitude : {data.get('lon', 'N/A')}\n"
        )

        await interaction.response.send_message(message)

    except:
        await interaction.response.send_message("⚠️ Une erreur est survenue.")

# ============================
#        /host
# ============================
@bot.tree.command(name="host", description="Analyse un site web et récupère son IP")
async def host(interaction: discord.Interaction, site: str):
    try:
        ip = socket.gethostbyname(site)
        url = f"http://ip-api.com/json/{ip}?fields=66846719"
        data = requests.get(url).json()

        if data["status"] == "fail":
            await interaction.response.send_message("❌ Impossible d'obtenir les informations de cet hôte.")
            return

        message = (
            f"🖥️ **Informations sur l'hôte : {site}**\n"
            f"• IP : {ip}\n"
            f"• Pays : {data.get('country', 'N/A')}\n"
            f"• Région : {data.get('regionName', 'N/A')}\n"
            f"• Ville : {data.get('city', 'N/A')}\n"
            f"• FAI : {data.get('isp', 'N/A')}\n"
            f"• Organisation : {data.get('org', 'N/A')}\n"
            f"• AS : {data.get('as', 'N/A')}\n"
            f"• Latitude : {data.get('lat', 'N/A')}\n"
            f"• Longitude : {data.get('lon', 'N/A')}\n"
        )

        await interaction.response.send_message(message)

    except socket.gaierror:
        await interaction.response.send_message("❌ Site invalide ou introuvable.")
    except:
        await interaction.response.send_message("⚠️ Une erreur est survenue.")

# ============================
#         TOKEN + KEEP ALIVE
# ============================

keep_alive()
bot.run(os.getenv("TOKEN"))
