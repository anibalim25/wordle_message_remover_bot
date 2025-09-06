import os
from aiohttp import web

async def handle(request):
    return web.Response(text="¡wena notisia mi gente!")

async def run_webserver():
    app = web.Application()
    app.add_routes([web.get('/', handle)])

    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
