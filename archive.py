#Download your channel's messages as a text file for backup purposes

import asyncio
from telethon import TelegramClient

# Replace these with your actual Telegram API credentials
api_id = number
api_hash = 'string'

# Name for the session file
session_name = 'session_name'

# Create a TelegramClient instance
client = TelegramClient(session_name, api_id, api_hash)

async def fetch_all_messages(entity):
    """
    Fetches all messages from the specified chat/channel.
    """
    messages = []
    async for msg in client.iter_messages(entity):
        messages.append(msg)
    return messages

async def main():
    await client.start()
    
    entity_input = input("Enter the chat/channel identifier for Server A: ").strip()
    try:
        # Try to interpret the input as a numeric ID
        entity_input = int(entity_input)
    except ValueError:
        # Otherwise, leave it as a string (e.g., '@username')
        pass

    print(f"Fetching messages from {entity_input}...")
    
    messages = await fetch_all_messages(entity_input)
    print(f"Fetched {len(messages)} messages.")
    
    with open("serverA_messages.txt", "w", encoding="utf-8") as f:
        for msg in messages:
            sender = msg.sender_id if msg.sender_id else "Unknown"
            f.write(f"{msg.date} - {sender}: {msg.text}\n")
    
    print("Messages have been saved to serverA_messages.txt")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
