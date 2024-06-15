import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Učitaj .env datoteku
load_dotenv()

# Učitaj vrijednosti iz .env datoteke
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ROLE_ID = int(os.getenv('ROLE_ID'))
WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID'))
RULES_CHANNEL_ID = int(os.getenv('RULES_CHANNEL_ID'))
WHITELIST_CHANNEL_ID = int(os.getenv('WHITELIST_CHANNEL_ID'))

intents = discord.Intents.default()
intents.members = True  # Potrebno za praćenje članova

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} je uspješno povezan!')

@bot.event
async def on_member_join(member):
    # Dodjeljivanje role
    role = member.guild.get_role(ROLE_ID)
    await member.add_roles(role)

    # Pravljenje embed poruke
    embed = discord.Embed(
        title="👋 Dobrodošli na Legion RolePlay!",
        description=f"Zdravo {member.mention}! Dobrodošao/la na naš server. 😊\n"
                    f"🌟 **Uživaj u igranju i zabavi!**\n"
                    f"📕 **Molimo te da pročitaš pravila servera**\n\n"
                    f"📝 **Informacije o polaganju Whiteliste možeš pronaći klikom na dugme Whitelist.**",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Klikni na 'Pravila Servera' ili 'Whitelist' za više informacija.")

    # Dodavanje dugmeta za preusmjeravanje u kanal s pravilima
    rules_channel = bot.get_channel(RULES_CHANNEL_ID)
    whitelist_channel = bot.get_channel(WHITELIST_CHANNEL_ID)
    
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Pravila Servera", url=f"https://discord.com/channels/{member.guild.id}/{rules_channel.id}"))
    view.add_item(discord.ui.Button(label="Whitelist", url=f"https://discord.com/channels/{member.guild.id}/{whitelist_channel.id}"))

    # Slanje embed poruke s dugmetom
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    await welcome_channel.send(embed=embed, view=view)

# Pokretanje bota
bot.run(DISCORD_TOKEN)
