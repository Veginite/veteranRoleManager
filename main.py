import datetime
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from dbc import create_server_connection
from queue import Queue
from discord.ext import tasks
from datetime import datetime, timezone

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
#DBPASS: Final[str] = os.getenv("DBPASS")

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
#dbc = create_server_connection("localhost", "root", DBPASS)
q: Queue = Queue()


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Empty message, was intents not set?')
        return

    response: str = ''
    try:
        #response = await get_response(user_message, message.author)
        #await message.channel.send(response)
        await message.channel.send("test")

    except Exception as e:
        print(e)


@client.event
async def on_ready() -> None:
    handle_message_queue.start()
    print(f'{client.user} is now running!')


@client.event
async def on_message(message: Message) -> None:
    # Prevents a potential infinite message loop
    if message.author == client.user:
        return

    q.put(message)

    next_interval = handle_message_queue.next_iteration
    next_interval = next_interval.astimezone(tz=timezone.utc)
    now = datetime.now(tz=timezone.utc)

    eta = ((next_interval - now).total_seconds() + ((q.qsize() - 1) * handle_message_queue.seconds))

    await message.channel.send(f'There are currently {q.qsize()} requests queued. ETA is {round(eta, 1)} seconds.'
                               + f' Additional delay will incur if your profile has more than one private league page.')


@tasks.loop(seconds=20)
async def handle_message_queue():
    if not q.empty():
        message = q.get()
        await send_message(message, message.content)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
