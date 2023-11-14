import psycopg
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def prompt(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input},
        ],
    )
    print(response)


def add_todo(description, due_date):
    with psycopg.connect("dbname=vaia") as conn:
        with conn.cursor() as curs:
            curs.execute(
                "INSERT INTO todo (description, due_date) VALUES (%s, %s)",
                (description, due_date),
            )
