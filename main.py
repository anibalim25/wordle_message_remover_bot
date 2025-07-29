import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')  # TOKEN del bot de discord
CANAL_OBJETIVO_ID = int(os.getenv('CANAL_ID'))  # ID del canal de discord del que quieres borrar mensajes

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    channel = bot.get_channel(CANAL_OBJETIVO_ID)
    if channel is None:
        print("No se encontró el canal")
        return
    def filtro(mensaje):
        return mensaje.author.bot and "playing" in mensaje.content

    print("Borrando mensajes antiguos...")
    deleted = await channel.purge(limit=100, check=filtro)
    print(f'Mensajes borrados: {len(deleted)}')


@bot.event
async def on_message(message):
    if message.channel.id != CANAL_OBJETIVO_ID:
        return

    if message.author.bot and "playing" in message.content:
        try:
            await message.delete()
            print(f'Mensaje eliminado: {message.content[:40]}...')
        except Exception as e:
            print(f'Error al eliminar mensaje: {e}')

    await bot.process_commands(message) #permite que siga procesando mensajes, de momento no hace falta

bot.run(TOKEN)
