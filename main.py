from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
# from dbc import create_server_connection
from queue import Queue
from discord.ext import tasks
import datetime
from datetime import datetime, timezone

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
# DBPASSWORD: Final[str] = os.getenv("DBPASSWORD")

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
# dbc = create_server_connection("localhost", "root", DBPASSWORD)
q: Queue = Queue()
msg_counter: int = 0
busy: bool = False


async def send_message(message: Message) -> None:
    if not message.content:
        print('Empty message, was intents not set?')
        return

    try:
        response: str = await get_response(message)
        await message.channel.send(response)

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

    channel_id = message.channel.id
    general_bot_spam_channel_id: int = 1221773773339099228  # replace this on deployment!
    want_to_sell_channel_id: int = 1264691307360555089      # replace this on deployment!
    staff_bot_spam_channel_id: int = 1264760259915026472    # replace this on deployment!

    if channel_id == general_bot_spam_channel_id:
        global q
        q.put(message)

        next_interval = handle_message_queue.next_iteration
        next_interval = next_interval.astimezone(tz=timezone.utc)
        now = datetime.now(tz=timezone.utc)

        eta = ((next_interval - now).total_seconds() + ((q.qsize() - 1) * handle_message_queue.seconds))

        await message.channel.send(
            f'There are currently {q.qsize()} requests queued. ETA is {round(eta, 1)} seconds.'
            + f' Additional delay will incur if your profile has more than one private league page.')

    elif channel_id == want_to_sell_channel_id:
        global msg_counter
        msg_counter += 1
        if msg_counter == 15:  # adjust this parameter to change the message threshold
            msg_counter = 0
            await message.channel.send(
                "Please remember to follow rule #5 <#1264692541500952607>")  # REPLACE THIS CHANNEL ID

    # staff reserved bot spam channel, bypasses the queue
    elif channel_id == staff_bot_spam_channel_id:
        await send_message(message)


@tasks.loop(seconds=30)
async def handle_message_queue():
    global busy
    if not q.empty() and not busy:
        busy = True

        message = q.get()
        await send_message(message)

        busy = False


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
