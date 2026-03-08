import discord
from discord.ext import commands
import requests
import socket
import os
import asyncio  # nécessaire pour le ping toutes les 5 min

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# ============================
#       CONFIG BOT
# ============================
# ID du salon où envoyer le ping automatique
AUTO_CHANNEL_ID = 1479973171653251243  # ton salon Discord

@bot.event
async def on_ready():
    print(f"WULTI Bot connecté en tant que {bot.user}")
    try:
        channel = await bot.fetch_channel(AUTO_CHANNEL_ID)
        if channel:
            await channel.send("Salut ! Le bot est maintenant en ligne !")
    except Exception as e:
        print(f"Erreur en envoyant le message de démarrage : {e}")

# ============================
#        COMMANDE !ip
# ============================
@bot.command()
async def ip(ctx, adresse_ip):
    try:
        url = f"http://ip-api.com/json/{adresse_ip}"
        data = requests.get(url).json()

        if data["status"] == "fail":
            await ctx.send("❌ IP invalide ou introuvable.")
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
        await ctx.send(message)

    except Exception:
        await ctx.send("⚠️ Une erreur est survenue.")

# ============================
#       COMMANDE !geo
# ============================
@bot.command()
async def geo(ctx, adresse_ip):
    try:
        url = f"http://ip-api.com/json/{adresse_ip}?fields=66846719"
        data = requests.get(url).json()

        if data["status"] == "fail":
            await ctx.send("❌ IP invalide ou introuvable.")
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
        await ctx.send(message)

    except Exception:
        await ctx.send("⚠️ Une erreur est survenue.")

# ============================
#       COMMANDE !host
# ============================
@bot.command()
async def host(ctx, site):
    try:
        ip_addr = socket.gethostbyname(site)
        url = f"http://ip-api.com/json/{ip_addr}?fields=66846719"
        data = requests.get(url).json()

        if data["status"] == "fail":
            await ctx.send("❌ Impossible d'obtenir les informations de cet hôte.")
            return

        message = (
            f"🖥️ **Informations sur l'hôte : {site}**\n"
            f"• IP : {ip_addr}\n"
            f"• Pays : {data.get('country', 'N/A')}\n"
            f"• Région : {data.get('regionName', 'N/A')}\n"
            f"• Ville : {data.get('city', 'N/A')}\n"
            f"• FAI : {data.get('isp', 'N/A')}\n"
            f"• Organisation : {data.get('org', 'N/A')}\n"
            f"• AS : {data.get('as', 'N/A')}\n"
            f"• Latitude : {data.get('lat', 'N/A')}\n"
            f"• Longitude : {data.get('lon', 'N/A')}\n"
        )
        await ctx.send(message)

    except socket.gaierror:
        await ctx.send("❌ Site invalide ou introuvable.")
    except Exception:
        await ctx.send("⚠️ Une erreur est survenue.")

# ============================
#       TACHE PING 5 MINUTES
# ============================
async def message_periodique():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            channel = await bot.fetch_channel(AUTO_CHANNEL_ID)
            if channel:
                await channel.send("🔔 Message automatique toutes les 5 minutes !")
        except Exception as e:
            print(f"Erreur en envoyant le message automatique : {e}")
        await asyncio.sleep(300)  # 5 minutes

bot.loop.create_task(message_periodique())

# ============================
#       LANCEMENT DU BOT
# ============================
bot.run(os.getenv("TOKEN"))
