import bcrypt
from src.database import get_connection


def register_user(name, username, phone, email, password):

    connection = get_connection()
    cursor = connection.cursor()

    # Check whether username or phone already exists
    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE username = %s OR phone = %s
        """,
        (username, phone)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()
        return False, "Username or phone number already exists."

    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Insert user
    cursor.execute(
        """
        INSERT INTO users
        (name, username, phone, email, password_hash)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            name,
            username,
            phone,
            email,
            password_hash
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return True, "Registration successful."




def login_user(username, phone, password):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT user_id, name, username, phone, email, password_hash
        FROM users
        WHERE username = %s AND phone = %s
        """,
        (username, phone)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user is None:
        return False, "Invalid username or phone number."

    password_valid = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    )

    if not password_valid:
        return False, "Invalid password."

    return True, user