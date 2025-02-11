import asyncio
import os
from telethon import TelegramClient

# Telegram API credentials (replace with your own if needed)
api_id = number
api_hash = 'string'
session_name = 'session_name'

# Create a single TelegramClient instance for reuse
client = TelegramClient(session_name, api_id, api_hash)

async def find_id(client):
    """
    Finds and displays the numeric ID and title of a Telegram channel or chat.
    """
    username = input("Enter the channel username (without @) or invite link: ").strip()
    try:
        channel = await client.get_entity(username)
    except Exception as e:
        print("Error retrieving entity:", e)
        return
    print("Channel ID:", channel.id)
    print("Channel Title:", getattr(channel, 'title', 'No title found'))

async def archive(client):
    """
    Fetches all messages from a specified channel/chat and writes them to a text file.
    """
    entity_input = input("Enter the chat/channel identifier (username or numeric ID): ").strip()
    try:
        possible_int = int(entity_input)
        entity_input = possible_int
    except ValueError:
        pass

    try:
        resolved_entity = await client.get_entity(entity_input)
    except Exception as e:
        print(f"Error resolving entity '{entity_input}': {e}")
        return

    print(f"Fetching messages from {resolved_entity}...")
    messages = []
    # Download all messages; change 'limit=None' to a number if you wish to cap the total.
    async for msg in client.iter_messages(resolved_entity, limit=None):
        messages.append(msg)
    print(f"Fetched {len(messages)} messages.")

    # Save messages to a file
    with open("serverA_messages.txt", "w", encoding="utf-8") as f:
        for msg in messages:
            sender = msg.sender_id if msg.sender_id else "Unknown"
            f.write(f"{msg.date} - {sender}: {msg.text}\n")

    print("Messages have been saved to serverA_messages.txt")

async def upload(client):
    """
    Reads messages from 'input_data/messages.txt' and sends each to a specified destination server.
    """
    destination_input = input("Enter the numeric ID for the destination server: ").strip()
    try:
        destination_id = int(destination_input)
    except ValueError:
        print("Invalid numeric ID. Please enter a valid number.")
        return

    try:
        destination_entity = await client.get_entity(destination_id)
    except Exception as e:
        print(f"Could not find an entity with ID {destination_id}: {e}")
        return

    # Define the path to the input text file
    input_file_path = os.path.join("input_data", "messages.txt")
    if not os.path.isfile(input_file_path):
        print(f"Input file not found: {input_file_path}")
        return

    # Read messages from the file (one message per line)
    with open(input_file_path, "r", encoding="utf-8") as f:
        messages = f.readlines()

    print(f"Read {len(messages)} messages from {input_file_path}")

    # Forward each message to the destination server
    for idx, message in enumerate(messages, start=1):
        message = message.strip()
        if not message:
            continue  # Skip empty lines
        try:
            forwarded_text = f"Forwarded: {message}"
            await client.send_message(destination_entity, forwarded_text)
            print(f"Sent message {idx}")
            # Sleep briefly to help avoid rate limits; adjust as necessary
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Failed to send message {idx}: {e}")

    print("All messages have been forwarded to the destination server.")

async def count_total_messages(client):
    """
    Counts and displays the total number of messages in a specified chat/channel.
    """
    entity_input = input("Enter the chat/channel identifier (username or numeric ID) to count messages: ").strip()
    try:
        possible_int = int(entity_input)
        entity_input = possible_int
    except ValueError:
        pass

    try:
        resolved_entity = await client.get_entity(entity_input)
    except Exception as e:
        print(f"Error resolving entity '{entity_input}': {e}")
        return

    print(f"Counting messages from {resolved_entity}...")
    count = 0
    async for msg in client.iter_messages(resolved_entity, limit=None):
        count += 1
    print(f"Total messages: {count}")

async def main():
    """
    Main menu that lets the user select an operation.
    """
    await client.start()
    while True:
        print("\nSelect an option:")
        print("1. Find Id")
        print("2. Archive")
        print("3. Upload")
        print("4. Count Total Messages")
        print("5. Exit")
        option = input("Enter your choice (1-5): ").strip()
        if option == "1":
            await find_id(client)
        elif option == "2":
            await archive(client)
        elif option == "3":
            await upload(client)
        elif option == "4":
            await count_total_messages(client)
        elif option == "5":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
