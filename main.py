import discord
import logging
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import aiohttp
from keep_alive import run_webserver

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")

TOKEN = os.getenv('TOKEN')  # TOKEN del bot de discord
CANAL_OBJETIVO_ID = int(os.getenv('CANAL_ID'))  # ID del canal de discord del que quieres borrar mensajes
KEEP_ALIVE_URL = os.getenv('KEEP_ALIVE_URL') # URL de donde esté desplegado el bot

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Bot conectado como {bot.user}')
    channel = bot.get_channel(CANAL_OBJETIVO_ID)
    if channel is None:
        logger.warning("No se encontró el canal")
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
            logger.info(f'Mensaje eliminado: {message.content[:40]}...')
        except Exception as e:
            logger.warning(f'Error al eliminar mensaje: {e}')

    await bot.process_commands(message) #permite que siga procesando mensajes, de momento no hace falta

async def keep_awake():
    if not KEEP_ALIVE_URL:
        logger.warning("KEEP_ALIVE_URL no configurado, auto-pings desactivados.")
        return

    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(KEEP_ALIVE_URL) as resp:
                    logger.info(f"🔄 Auto-ping enviado, status: {resp.status}")
        except Exception as e:
            logger.warning(f"Error en auto-ping: {e}")

        await asyncio.sleep(300)

async def main():
    await asyncio.gather(
        bot.start(TOKEN),
        run_webserver(),
        keep_awake()
    )

if __name__ == "__main__":
    if not TOKEN:
        logger.warning("No se encontró el TOKEN en las variables de entorno")
    else:
        asyncio.run(main())
