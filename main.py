import discord
import re
import os
import dotenv
from anthropic import Anthropic

dotenv.load_dotenv()

client = discord.Client(intents=discord.Intents.all())
gpt = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

async def generate(lan, code):
    response = gpt.messages.create(
        max_tokens=4096,
        model = "claude-3-opus-20240229",
        messages=[
            {"role": "user", "content": f"You are a Code bug reviewer. You have to check if the code user provided has the following bugs:\nA. SQL Injection\nB. Information Leak\nC. Filter Bypass\nD. Local File Inclusion\nE. Server-Side Request Forgery\nF. Arbitrary File extension\nG. Length Extension\nH. Length Zipping\nI. Content Replacement\nJ. Signature Confusion\nK. Insecure Deserialization\n\nIf you find any of the above bugs, please provide the line number and the bug name. If you don't find any bugs, please reply with 'No bugs found'. The user will provide the code now.\n\n```{lan[0]}\n{code[0]}```"},
        ]
    )
    return response.content[0].text

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
@client.event
async def on_message(message):
    if message.content.startswith("!check"):
        conetnet = re.sub("!check ", "", message.content)
        lan = re.findall(r'```(.*?)\n', conetnet)
        code = re.findall(r'```(.*?)```', conetnet, re.DOTALL)
        print("Language: ", lan)
        print("Code: ", code)
        reply = await generate(lan, code)
        await message.reply(reply)

client.run(os.getenv("DISCORD_TOKEN"))