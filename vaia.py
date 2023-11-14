import argparse
import json

import psycopg
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def create_todo(user_input, messages=[]):
    if not len(messages):
        messages = [
            {
                "role": "system",
                "content": """
                        You are a helpful assistant designed to output JSON.
                        You are given a user input and asked to turn it into a todo item.
                        Try to make assumptions about a valid description and reminder time
                        from the initial user input. If you don't have enough information,
                        for a concise item description and a reminder time, keep asking questions
                        until you have enough information, and then confrim with the user.
                        Once the user confirms, output the final message in JSON format
                        with description, reminder_time, and confirmation keys.
                        Format the reminder_time as a string in ISO 8601 format in the America/New_York timezone.
                        The confirmation key should be the message you are giving to the user confirming
                        the details of the reminder in a friendly, concise format, well suited for an SMS response.
                    """,
            },
        ]

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
    )

    try:
        return json.loads(response.choices[0].message.content)
    except json.decoder.JSONDecodeError:
        content = response.choices[0].message.content
        messages.append(
            {
                "role": "assistant",
                "content": content,
            }
        )
        new_input = input(f"{content} \n\n> ")
        return create_todo(new_input, messages)


def add_todo(description, reminder_time, confirmation):
    print(confirmation)
    exit()
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            curs.execute(
                "INSERT INTO todo (description) VALUES (%s)",
                (description,),
            )


if __name__ == "__main__":
    prompt = input("Prompt: ")
    todo = create_todo(prompt)
    add_todo(todo["description"], todo["reminder_time"], todo["confirmation"])
