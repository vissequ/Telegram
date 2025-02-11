#When run via CLI you can enter invite link to receive your channel's numeric ID. This is useful for developing applications.

import asyncio
from telethon import TelegramClient

# Replace these with your actual Telegram API credentials
api_id = number
api_hash = 'string'
# Name for the session file
session_name = 'session_name'

client = TelegramClient(session_name, api_id, api_hash)

async def main():
    # Start the client (this will use your saved session if available)
    await client.start()
    
    # Ask for the channel's username (without the '@') or invite link
    username = input("Enter the channel username (without @) or invite link: ").strip()
    
    # Retrieve the channel entity
    channel = await client.get_entity(username)
    
    # Print the channel's numeric ID
    print("Channel ID:", channel.id)

    # Optionally, print more details about the channel
    print("Channel Title:", getattr(channel, 'title', 'No title found'))

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
