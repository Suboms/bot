from dependency import *
from datetime import datetime


async def start_command(event):
    user_id = event.sender_id
    json_data = get_user_data_from_json(user_id)

    if json_data:
        reply = "Welcome back! Your user data has been loaded from the JSON file. Use /help command to view the list of commands."
    else:
        reply = "Hello! I am your message forwarding bot. Please use the /help command to view the list of commands."
            # Initialize user data if not present in memory
        if str(user_id) not in user_data:
            user_data[(user_id)] = {}
    await event.reply(reply)


# Command to input source channel link


async def source_channel_command(event):
    user_id = event.sender_id
    try:
        if str(user_id) not in user_data:
            user_data[str(user_id)] = {}
        user_data[str(user_id)]["source_channel_link"] = event.raw_text.split(
            maxsplit=1
        )[1]
        update_github_file(PAT, REPO_OWNER, REPO_NAME, FILE_PATH, user_data)
        reply = "Source channel link saved. Please use the /destination."
    except IndexError:
        reply = "Please send /source followed-by-the-source-url"
    await event.reply(reply)


# Command to input destination channel link


async def destination_channel_command(event):
    if event.sender_id == 6522874768:
        try:
            user_id = event.sender_id
            if str(user_id) not in user_data:
                user_data[str(user_id)] = {}
            user_data[str(user_id)]["destination_channel_link"] = event.raw_text.split(
                maxsplit=1
            )[1]
            update_github_file(PAT, REPO_OWNER, REPO_NAME, FILE_PATH, user_data)
            reply = "Destination channel link saved. Please use the /datestart."
        except IndexError:
            reply = "Please send /destination followed-by-the-source-url"
        await event.reply(reply)


# Command to input start date


async def start_date_command(event):
    user_id = event.sender_id
    try:
        date_str = event.raw_text.split(maxsplit=1)[1]
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        if str(user_id) not in user_data:
            user_data[str(user_id)] = {}
        user_data[str(user_id)]["start_date_input"] = parsed_date.strftime(
            "%Y-%m-%d %H:%M"
        )  # Convert to string
        update_github_file(PAT, REPO_OWNER, REPO_NAME, FILE_PATH, user_data)
        reply = "Start date saved. Please use the /enddate command next."
    except ValueError:
        reply = "Invalid date format. Please use the format 'YYYY-MM-DD HH:MM'."
    except IndexError:
        reply = "Please send /datestart followed-by-the-begining-date in 'YYYY-MM-DD HH:MM' format"
    await event.reply(reply)




async def end_date_command(event):
    user_id = event.sender_id
      # Get the date string
    try:
        date_str = event.raw_text.split(maxsplit=1)[1]
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        if str(user_id) not in user_data:
            user_data[str(user_id)] = {}
        user_data[str(user_id)]["end_date_input"] = parsed_date.strftime(
            "%Y-%m-%d %H:%M"
        )  # Convert to string
        update_github_file(PAT, REPO_OWNER, REPO_NAME, FILE_PATH, user_data)
        reply = "End date saved. You can now use the /settings command to view your saved data."
    except ValueError:
        reply = "Invalid date format. Please use the format 'YYYY-MM-DD HH:MM'."
    except IndexError:
        reply = "Please send /enddate followed-by-the-end-date in 'YYYY-MM-DD HH:MM' format"
    await event.reply(reply)


# Command to view saved data
async def settings_command(event):
    user_id = event.sender_id

    data = get_user_data_from_json(user_id)

    if data:
        response = (
            f"Your saved data:\nSource Channel: {data.get('source_channel_link')}\n"
            f"Destination Channel: {data.get('destination_channel_link')}\n"
            f"Start Date: {data.get('start_date_input')}\n"
            f"End Date: {data.get('end_date_input')}"
        )
        await event.reply(response)
    else:
        await event.reply(
            "No saved data found. Use the relevant commands to save your data."
        )


async def help_command(event):
    help_message = (
        "Available commands:\n"
        "/source the-source-channel-link\n"
        "/destination the-destination-channel-link\n"
        "/datestart the-start-date\n"
        "/enddate the-end-date\n"
        "/settings - View your saved data\n"
        "/help - Show this help message\n"
        "/forward - Start the message forwarding process"
    )
    await event.reply(help_message)
update_github_file(PAT, REPO_OWNER, REPO_NAME, FILE_PATH, user_data)