from datetime import datetime
from psycopg2.extras import NamedTupleCursor
import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def connect_to_db():
    return psycopg2.connect(DATABASE_URL)


def get_urls_from_db():
    try:
        with connect_to_db() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute('''
                SELECT DISTINCT ON (urls.id, urls.name) urls.id, urls.name,
                    url_checks.created_at, url_checks.status_code
                FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id
                ORDER BY urls.id DESC''')
                data = curs.fetchall()
        return data
    except psycopg2.Error:
        return 'error'


def get_id_if_exist(url: str) -> int:
    with connect_to_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('''
            SELECT id FROM urls WHERE name = %s''', (url,))
            data = curs.fetchone()
    if data:
        return data.id


def save_new_url_to_bd_urls(url: str):
    try:
        with connect_to_db() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute('''
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s) RETURNING id''', (
                    url, datetime.now().isoformat(timespec="seconds")),
                )
                data = curs.fetchone()
        return data
    except psycopg2.Error:
        return None


def save_to_db_url_checks(id, status_code, h1, title, description):
    with connect_to_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('''
            INSERT INTO url_checks
            (url_id, created_at, status_code, h1, title, description)
            VALUES (%s, %s, %s, %s, %s, %s)''', (
                id, datetime.today().isoformat(),
                status_code, h1, title, description),
            )
    return


def get_urls_data(id: int):
    with connect_to_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            try:
                curs.execute('''
                SELECT * FROM urls WHERE id = %s''', (id,))
            except psycopg2.errors.InvalidTextRepresentation:
                return None
            urls_data = curs.fetchone()
    return urls_data


def get_checks_data(id: int):
    with connect_to_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('''
            SELECT * FROM url_checks
            WHERE url_id = %s ORDER BY id DESC''', (id,))
            checks_data = curs.fetchall()
    return checks_data


def get_url_from_db(id: int):
    with connect_to_db() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('''
            SELECT name from urls WHERE id = %s''', (id,))
            data = curs.fetchone()
    return data.name
