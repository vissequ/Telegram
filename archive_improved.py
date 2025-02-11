import asyncio
from telethon import TelegramClient

# Replace these with your actual Telegram API credentials
api_id = number
api_hash = 'string'

# Name for the session file for Server A
session_name = 'session_server_a'

# Create a TelegramClient instance
client = TelegramClient(session_name, api_id, api_hash)

async def fetch_all_messages(entity):
    """
    Fetches all messages from the specified chat/channel entity.
    """
    messages = []
    async for msg in client.iter_messages(entity):
        messages.append(msg)
    return messages

async def main():
    # Start the client and log in if necessary
    await client.start()
    
    # Ask for the identifier (username or numeric ID)
    entity_input = input("Enter the chat/channel identifier for Server A (username or numeric ID): ").strip()
    
    # Try to convert to an integer if the input is numeric
    try:
        possible_int = int(entity_input)
        entity_input = possible_int
    except ValueError:
        # Leave as string if not numeric (for example, '@YourChannelUsername')
        pass

    # Resolve the entity using get_entity
    try:
        resolved_entity = await client.get_entity(entity_input)
    except Exception as e:
        print(f"Error resolving entity '{entity_input}': {e}")
        await client.disconnect()
        return

    print(f"Fetching messages from {resolved_entity}...")
    
    # Fetch all messages from the resolved entity
    messages = await fetch_all_messages(resolved_entity)
    print(f"Fetched {len(messages)} messages.")
    
    # Write the messages to a file
    with open("serverA_messages.txt", "w", encoding="utf-8") as f:
        for msg in messages:
            sender = msg.sender_id if msg.sender_id else "Unknown"
            f.write(f"{msg.date} - {sender}: {msg.text}\n")
    
    print("Messages have been saved to serverA_messages.txt")
    
    # Disconnect the client
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
