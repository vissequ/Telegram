import asyncio
import os
from telethon import TelegramClient

# Replace these with your actual Telegram API credentials
api_id = number
api_hash = 'string'
session_name = 'session_server_a'

client = TelegramClient(session_name, api_id, api_hash)

async def main():
    # Start the Telegram client (uses stored session if available)
    await client.start()

    # Request the destination server's numeric ID
    destination_input = input("Enter the numeric ID for the destination server: ").strip()
    try:
        destination_id = int(destination_input)
    except ValueError:
        print("Invalid numeric ID. Please enter a valid number.")
        return

    # Retrieve the destination entity using its numeric ID
    try:
        destination_entity = await client.get_entity(destination_id)
    except Exception as e:
        print(f"Could not find an entity with ID {destination_id}: {e}")
        return

    # Define the path to the input text file inside the 'input_data' folder in the root directory
    input_file_path = os.path.join("input_data", "messages.txt")
    
    # Check if the file exists
    if not os.path.isfile(input_file_path):
        print(f"Input file not found: {input_file_path}")
        return

    # Read messages from the text file (assuming one message per line)
    with open(input_file_path, "r", encoding="utf-8") as f:
        messages = f.readlines()
    
    print(f"Read {len(messages)} messages from {input_file_path}")

    # For each message, send it to the destination server.
    # Here we prepend "Forwarded:" to simulate a forward.
    for idx, message in enumerate(messages, start=1):
        message = message.strip()
        if not message:
            continue  # Skip empty lines
        try:
            # Construct the message text (simulate forward)
            forwarded_text = f"Forwarded: {message}"
            await client.send_message(destination_entity, forwarded_text)
            print(f"Sent message {idx}")
            # Sleep briefly to avoid rate limiting (adjust as needed)
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Failed to send message {idx}: {e}")

    print("All messages have been forwarded to the destination server.")

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
