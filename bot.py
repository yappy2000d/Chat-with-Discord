import asyncio, time

import discord
from discord.ext import commands

TOKEN = "<your token>"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

async def run(prompt: str):
    proc = await asyncio.create_subprocess_exec(
        "./gemma",
        "--tokenizer", "tokenizer.spm", 
        "--model", "2b-it", 
        "--compressed_weights", "2b-it-sfp.sbs",
        "--num_threads", "2",
        "--verbosity", "0",
        # "--multiturn", "1",  # 使用CLI模式時，不支援多輪對話
        "--temperature", "0.4",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate(input=prompt.encode())

    return stdout.decode()

@bot.event
async def on_message(message: discord.Message):
    if bot.user.mentioned_in(message):
        cmd = message.content.replace(f"<@{bot.user.id}>", "").strip()

        t = time.time()

        print(f"From {message.author.name}, At {time.strftime("%H:%M:%S", time.localtime(t))}")

        async with message.channel.typing():
            reply = await run(cmd)
        await message.reply(reply)

        print(f"Replied to {message.author.name}, took {time.time() - t:.1f} seconds.")

@bot.event
async def on_ready():
    print(f"\"{bot.user}\" is ready!")

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
