from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Empty message, was intents not set?')
        return

    try:
        response: str = await get_response(user_message, message.author)
        await message.channel.send(response)
    except Exception as e:
        print(e)


@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


@client.event
async def on_message(message: Message) -> None:
    # prevents a potential infinite message loop
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    await send_message(message, user_message)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
