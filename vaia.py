import psycopg2


def add_todo(description, due_date):
    with psycopg2.connect("dbname=vaia") as conn:
        with conn.cursor() as curs:
            curs.execute(
                "INSERT INTO todo (description, due_date) VALUES (%s, %s)",
                (description, due_date),
            )
