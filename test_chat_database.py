from src.database import (
    create_chat_session,
    save_message,
    get_chat_history
)


# Test user ID
user_id = 2


# Create a new chat session
session_id = create_chat_session(
    user_id,
    "Recipe Recommendation Chat"
)

print("Created session ID:", session_id)


# Save user message
save_message(
    session_id,
    "user",
    "chicken, rice, onion, tomato"
)

print("User message saved.")


# Save chatbot response
save_message(
    session_id,
    "bot",
    "I found 5 recipes for you."
)

print("Bot message saved.")


# Read chat history
history = get_chat_history(session_id)

print("\nChat History:")
print("-" * 50)

for sender, message, created_at in history:

    print(
        f"{sender}: {message}"
    )

    print(
        f"Time: {created_at}"
    )

    print("-" * 50)