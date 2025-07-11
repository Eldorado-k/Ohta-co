import dns.resolver
from pyrogram import idle
from . import web_server, WEBHOOK
from aiohttp import web
from . import app, log
import traceback

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']  # this is a google public dns

async def main():
    await app.start()
    if WEBHOOK:
        apps = web.AppRunner(await web_server())
        await apps.setup()       
        await web.TCPSite(apps, "0.0.0.0", 8080).start()     
        print(f"Webhook is running on port 8080")
    
    try:
        await app.send_message(chat_id=log, text='<b>Le bot est en marche !</b>')
    except Exception as e:
        print(f"Failed to send startup message: {e}")
        traceback.print_exc()  # Optionnel: affiche la trace complète de l'erreur
    
    await idle()
    await app.stop()

app.loop.run_until_complete(main())
