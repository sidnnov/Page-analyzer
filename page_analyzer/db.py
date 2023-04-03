from datetime import datetime
from psycopg2.extras import NamedTupleCursor
import psycopg2


def create_connection(app):
    return psycopg2.connect(app.config["DATABASE_URL"])


def close(conn):
    return conn.close()


def get_urls_4(conn):
    try:
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


def get_id_if_exist(conn, url: str) -> int:
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''
        SELECT id FROM urls WHERE name = %s''', (url,))
        data = curs.fetchone()
    if data:
        return data.id


def save_url(conn, url: str):
    try:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('''
            INSERT INTO urls (name, created_at)
            VALUES (%s, %s) RETURNING id''', (
                url, datetime.now().isoformat(timespec="seconds")),
            )
            data = curs.fetchone()
            conn.commit()
        return data
    except psycopg2.Error:
        return None


def save_url_checks(conn, id, status_code, content):
    h1, title, description = content
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''
        INSERT INTO url_checks
        (url_id, created_at, status_code, h1, title, description)
        VALUES (%s, %s, %s, %s, %s, %s)''', (
            id, datetime.today().isoformat(),
            status_code, h1, title, description),
        )
        conn.commit()
    return


def get_urls(conn, id: int):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        try:
            curs.execute('''
            SELECT * FROM urls WHERE id = %s''', (id,))
        except psycopg2.errors.InvalidTextRepresentation:
            return None
        urls_data = curs.fetchone()
    return urls_data


def get_checks(conn, id: int):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''
        SELECT * FROM url_checks
        WHERE url_id = %s ORDER BY id DESC''', (id,))
        checks_data = curs.fetchall()
    return checks_data


def get_url(conn, id: int):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('''
        SELECT name from urls WHERE id = %s''', (id,))
        data = curs.fetchone()
    return data.name
