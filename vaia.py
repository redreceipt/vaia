import argparse
import json

import psycopg
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def create_todo(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",
            },
            {
                "role": "user",
                "content": f"""
                    Take the following user input and turn it into a todo item.
                    Format as JSON with description and due_date keys.
                    due_date should be ISO format:

                    {user_input}
                """,
            },
        ],
    )
    return json.loads(response.choices[0].message.content)


def add_todo(description, due_date):
    print(f"Adding todo: {description} due on {due_date}")
    exit()
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            curs.execute(
                "INSERT INTO todo (description, due_date) VALUES (%s, %s)",
                (description, due_date),
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a todo item")
    parser.add_argument("prompt", help="Prompt to use for GPT-3")
    args = parser.parse_args()
    todo = create_todo(args.prompt)
    print(todo)
    add_todo(todo["description"], todo["due_date"])
