from async_hcaptcha import AioHcaptcha
from subprocess import check_output

o = check_output(['chromedriver', '--version'])
try:
    o = o.decode("utf8").strip()
except:
    pass
print(f"\"chromedriver --version\" output: {o}")

import logging
logging.basicConfig(filename="bot.log", filemode="a", level=logging.DEBUG)

async def main():
    print("Testing async-hcaptcha...")
    solver = AioHcaptcha("f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34", "https://discord.com/channels/@me", {"executable_path": "chromedriver"})
    resp = await solver.solve(retry_count=3, custom_params={"rqdata": "xHJHshn3p71FcYoVCW5zA3m2CFw59JXBecFaR2l90z/NjjoYaXq2FBTi05LPnOX1v/MwStZg9DZKQA4f4ExkDjwlMaS3AKGIrcb2rUKsg8nDI9IaXEFDAhWqvuuCuaW3urxO2J1B/NEkfS938O58cqrE00aPILCQPUHVU1l/Ek8"})
    print(resp)
    print("Success!" if resp else "Failed!")

if __name__ == "__main__":
    from asyncio import get_event_loop
    get_event_loop().run_until_complete(main())