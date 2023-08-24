from telethon import errors
import asyncio
import pytz
from telethon.tl.functions.messages import ForwardMessagesRequest
from datetime import datetime
from dependency import get_message_file_name, get_user_data_from_json, user_data


async def handle_forwarding(event):
    user_id = event.sender_id
    json_data = get_user_data_from_json(user_id)
    if user_id in user_data:
        data = user_data[user_id]
    elif json_data:
        data = json_data
    else:
        await event.reply(
            "No saved data found. Use the relevant commands to save your data."
        )
        return

    source_channel_link = data.get("source_channel_link")
    destination_channel_link = data.get("destination_channel_link")
    start_date_input = data.get("start_date_input")
    end_date_input = data.get("end_date_input")
    try:
        try:
            source_channel = await event.client.get_entity(source_channel_link)
            destination_channel = await event.client.get_entity(
                destination_channel_link
            )
        except ValueError as ve:
            await event.reply(f"Error getting entities: {ve}")
            return
        start_date = datetime.strptime(start_date_input, "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(end_date_input, "%Y-%m-%d %H:%M")
        start_date_utc_aware = start_date.replace(tzinfo=pytz.utc)
        end_date_utc_aware = end_date.replace(tzinfo=pytz.utc)
        await event.reply("Starting message forwarding process...")
        async with event.client as client:
            try:
                source_participants = await client.get_participants(source_channel)
                destination_participants = await client.get_participants(
                    destination_channel
                )
                bot_username = "idontknowwhattonamethebot"
                if bot_username in [
                    participant.username for participant in source_participants
                ] and bot_username in [
                    participant.username for participant in destination_participants
                ]:
                    all_messages = []
                    async for message in client.iter_messages(source_channel):
                        all_messages.append(message)
                    all_messages = list(reversed(all_messages))
                    all_messages.sort(key=get_message_file_name, reverse=False)
                    forwarded_count = 0
                    total_forwarded_count = 0
                    for message in all_messages:
                        message_date_utc = message.date.replace(tzinfo=pytz.utc)
                        if (
                            start_date_utc_aware
                            <= message_date_utc
                            < end_date_utc_aware
                        ):
                            try:
                                await client(
                                    ForwardMessagesRequest(
                                        from_peer=source_channel,
                                        to_peer=destination_channel,
                                        id=[message.id],
                                        drop_author=True,
                                    )
                                )
                                forwarded_count += 1
                                total_forwarded_count += 1
                                await asyncio.sleep(
                                    3
                                )  # Sleep for a short interval between messages
                                if forwarded_count == 800:
                                    await event.reply(
                                        "Reached 800 forwarded messages. Sleeping for 5 minutes..."
                                    )
                                    await asyncio.sleep(
                                        300
                                    )  # Sleep for 5 minutes (300 seconds)
                                    forwarded_count = 0
                            except errors.FloodWaitError as e:
                                wait_time = (
                                    e.seconds + 10
                                )  # Add an additional 10 seconds to the wait time
                                await event.reply(
                                    f"Error: FloodWaitError. Sleeping for {wait_time} seconds."
                                )
                                await asyncio.sleep(wait_time)
                            except errors.RPCError as e:
                                await event.reply(f"Error: {e}")
                    await event.reply(f"Forwarded {total_forwarded_count} messages.")
                elif bot_username in [
                    participant.username for participant in source_participants
                ] and destination_channel_link == "me":
                    all_messages = []
                    async for message in client.iter_messages(source_channel):
                        all_messages.append(message)
                    all_messages = list(reversed(all_messages))
                    all_messages.sort(key=get_message_file_name, reverse=False)
                    forwarded_count = 0
                    total_forwarded_count = 0
                    for message in all_messages:
                        message_date_utc = message.date.replace(tzinfo=pytz.utc)
                        if (
                            start_date_utc_aware
                            <= message_date_utc
                            < end_date_utc_aware
                        ):
                            name = get_message_file_name(message)
                            print(name)
                            try:
                                await client(
                                    ForwardMessagesRequest(
                                        from_peer=source_channel,
                                        to_peer=destination_channel,
                                        id=[message.id],
                                        drop_author=True,
                                    )
                                )
                                forwarded_count += 1
                                total_forwarded_count += 1
                                await asyncio.sleep(
                                    0
                                )  # Sleep for a short interval between messages
                                if forwarded_count == 800:
                                    await event.reply(
                                        "Reached 800 forwarded messages. Sleeping for 5 minutes..."
                                    )
                                    await asyncio.sleep(
                                        300
                                    )  # Sleep for 5 minutes (300 seconds)
                                    forwarded_count = 0
                            except errors.FloodWaitError as e:
                                wait_time = (
                                    e.seconds + 10
                                )  # Add an additional 10 seconds to the wait time
                                await event.reply(
                                    f"Error: FloodWaitError. Sleeping for {wait_time} seconds."
                                )
                                await asyncio.sleep(wait_time)
                            except errors.RPCError as e:
                                await event.reply(f"Error: {e}")
                    await event.reply(f"Forwarded {total_forwarded_count} messages.")
                else:
                    await event.reply(
                        "Please make sure the bot is a member of both channels."
                    )
            except errors.RPCError as rpc_error:
                await event.reply(f"RPCError occurred: {rpc_error}")
            except Exception as e:
                await event.reply(f"An error occurred: {e}")

    except Exception as e:
        await event.reply(f"An error occurred: {e}")
