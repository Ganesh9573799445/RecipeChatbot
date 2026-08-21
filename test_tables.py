from src.database import get_connection

try:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SHOW TABLES")

    tables = cursor.fetchall()

    print("Tables in recipe_chatbot:")

    for table in tables:
        print("-", table[0])

    cursor.close()
    connection.close()

except Exception as e:
    print("Error:")
    print(e)