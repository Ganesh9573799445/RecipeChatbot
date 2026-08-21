import os
import mysql.connector
from dotenv import load_dotenv

# Explicitly locate the .env file
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


def get_connection():

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return connection


def create_chat_session(user_id, title="New Chat"):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO chat_sessions (user_id, title)
        VALUES (%s, %s)
    """

    cursor.execute(query, (user_id, title))
    conn.commit()

    session_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return session_id


def save_message(session_id, sender, message_text):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO chat_messages
        (session_id, sender, message_text)
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (session_id, sender, message_text)
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_chat_history(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT sender, message_text, created_at
        FROM chat_messages
        WHERE session_id = %s
        ORDER BY created_at ASC
    """

    cursor.execute(query, (session_id,))

    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return messages


def create_chat_session(user_id, session_title="New Chat"):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO chat_sessions
        (user_id, session_title)
        VALUES (%s, %s)
    """

    cursor.execute(
        query,
        (user_id, session_title)
    )

    conn.commit()

    session_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return session_id


def save_message(session_id, sender, message):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO chat_messages
        (session_id, sender, message)
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (session_id, sender, message)
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_chat_history(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT sender, message, created_at
        FROM chat_messages
        WHERE session_id = %s
        ORDER BY created_at ASC
    """

    cursor.execute(
        query,
        (session_id,)
    )

    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return messages


def get_user_sessions(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT session_id, session_title, created_at
        FROM chat_sessions
        WHERE user_id = %s
        ORDER BY created_at DESC
    """

    cursor.execute(query, (user_id,))

    sessions = cursor.fetchall()

    cursor.close()
    conn.close()

    return sessions

def update_session_title(session_id, title):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE chat_sessions
        SET session_title = %s
        WHERE session_id = %s
    """

    cursor.execute(
        query,
        (title, session_id)
    )

    conn.commit()

    cursor.close()
    conn.close()


def delete_chat_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Delete messages belonging to the session
    cursor.execute(
        """
        DELETE FROM chat_messages
        WHERE session_id = %s
        """,
        (session_id,)
    )

    # Delete the chat session
    cursor.execute(
        """
        DELETE FROM chat_sessions
        WHERE session_id = %s
        """,
        (session_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()
