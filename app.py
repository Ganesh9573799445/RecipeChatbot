import streamlit as st
import json
import pandas as pd
import ast
from PIL import Image
from src.auth import register_user, login_user
from src.recommender import recommend_recipes
from src.image_processor import detect_ingredients

df = pd.read_csv(
    "data/RAW_recipes.csv"
)

from src.database import (
    create_chat_session,
    save_message,
    get_chat_history,
    get_user_sessions,
    delete_chat_session
)


st.set_page_config(
    page_title="Recipe Chatbot",
    page_icon="🍳",
    layout="centered"
)


# --------------------------------
# Session state
# --------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = None

if "selected_session_id" not in st.session_state:
    st.session_state.selected_session_id = None

# --------------------------------
# Login / Register
# --------------------------------

if not st.session_state.logged_in:

    st.title("🍳 Recipe Chatbot")

    st.write(
        "Login or create an account to get recipe recommendations."
    )

    page = st.radio(
        "Choose an option:",
        ["Login", "Register"],
        horizontal=True
    )


    # --------------------------------
    # Login
    # --------------------------------

    if page == "Login":

        st.subheader("🔐 Login")

        username = st.text_input("Username")
        phone = st.text_input("Phone Number")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if not username or not phone or not password:

                st.error(
                    "Please fill in all required fields."
                )

            else:

                success, result = login_user(
                    username=username,
                    phone=phone,
                    password=password
                )

                if success:

                    st.session_state.logged_in = True
                    st.session_state.user = result

                    st.session_state.chat_session_id = create_chat_session(
                        result["user_id"],
                        "Recipe Recommendation Chat"
                    )

                    st.success("Login successful!")

                    st.rerun()

                else:

                    st.error(result)


    # --------------------------------
    # Register
    # --------------------------------

    else:

        st.subheader("📝 Create Account")

        name = st.text_input("Name")
        username = st.text_input("Username")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email (Optional)")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Register"):

            if not name or not username or not phone or not password:

                st.error(
                    "Please fill in all required fields."
                )

            else:

                success, message = register_user(
                    name=name,
                    username=username,
                    phone=phone,
                    email=email,
                    password=password
                )

                if success:

                    st.success(message)
                    st.info(
                        "You can now switch to Login."
                    )

                else:

                    st.error(message)


# --------------------------------
# Recipe Chatbot
# --------------------------------

else:

    user = st.session_state.user

    # --------------------------------
    # Chat History
    # --------------------------------

    st.sidebar.title("💬 Chat History")
    if st.sidebar.button(
        "➕ New Chat",
        use_container_width=True
    ):

        new_session_id = create_chat_session(
            user["user_id"],
            "New Chat"
        )

        st.session_state.chat_session_id = new_session_id
        st.session_state.selected_session_id = None
        st.session_state.image_ingredients = ""

        st.rerun()

    sessions = get_user_sessions(
        user["user_id"]
    )

    if sessions:

        for session_id, session_title, created_at in sessions:

            col1, col2 = st.sidebar.columns([4, 1])

            with col1:

                if st.button(
                    session_title,
                    key=f"session_{session_id}",
                    use_container_width=True
                ):

                    st.session_state.selected_session_id = session_id
                    st.rerun()

            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{session_id}"
                ):

                    delete_chat_session(
                        session_id
                    )

                    if (
                        st.session_state.selected_session_id
                        == session_id
                    ):
                        st.session_state.selected_session_id = None

                    st.rerun()

    else:

        st.sidebar.info(
            "No previous chats."
        )


    # --------------------------------
    # Previous Conversation
    # --------------------------------

    if st.session_state.selected_session_id:

        st.subheader("💬 Previous Conversation")

        history = get_chat_history(
            st.session_state.selected_session_id
        )

        for sender, message, created_at in history:

            if sender == "user":

                st.write(
                    "Enter ingredients separated by commas"
                )

                st.markdown(
                    f"**{message}**"
                )

            elif sender == "bot":

                try:

                    recipes = json.loads(message)

                    st.markdown(
                        "### 🍽️ Recommended Recipes"
                    )

                    for recipe in recipes:

                        st.markdown(
                            f"### 🍴 "
                            f"{recipe['name'].title()}"
                        )

                        st.write(
                            f"**Match Score:** "
                            f"{recipe['final_score']:.2%}"
                        )

                        st.write("**You have:**")

                        for ingredient in recipe["you_have"]:

                            st.write(
                                f"✅ {ingredient}"
                            )

                        st.write("**You need:**")

                        for ingredient in recipe["you_need"]:

                            st.write(
                                f"🛒 {ingredient}"
                            )

                        with st.expander(
                            "View Cooking Steps"
                        ):

                            for i, step in enumerate(
                                recipe["steps"],
                                start=1
                            ):

                                st.write(
                                    f"**{i}.** {step}"
                                )

                        st.divider()

                except json.JSONDecodeError:

                    # Display old chat messages
                    # that were saved before this change

                    st.markdown(
                        f"🤖 **Recipe Chatbot:** {message}"
                    )


    # --------------------------------
    # Recipe Chatbot
    # --------------------------------

    st.title("🍳 Recipe Chatbot")

    st.write(
        f"Welcome, {user['name']}! 👋"
    )


    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.chat_session_id = None
        st.session_state.selected_session_id = None

        st.rerun()


    st.divider()


    # --------------------------------
    # Ingredient Input
    # --------------------------------

    st.subheader("🥕 What ingredients do you have?")


    # Image upload

    st.subheader("📷 Or upload an ingredient image")

    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    image_ingredients = st.session_state.get(
        "image_ingredients",
        ""
    )


    if uploaded_image is not None:

        st.image(
            uploaded_image,
            caption="Uploaded ingredient image",
            use_container_width=True
        )

        if st.button(
            "🔍 Detect Ingredients From Image"
        ):

            from PIL import Image

            with st.spinner(
                "Analyzing image..."
            ):

                image = Image.open(
                    uploaded_image
                )

                detected = detect_ingredients(
                    image
                )

            if detected:

                image_ingredients = ", ".join(
                    ingredient
                    for ingredient, score in detected
                )

                st.session_state.image_ingredients = (
                    image_ingredients
                )

                st.success(
                    "Ingredients detected!"
                )

                st.write(
                    "**Detected ingredients:**"
                )

                for ingredient, score in detected:

                    st.write(
                        f"✅ {ingredient} "
                        f"({score:.2f})"
                    )

            else:

                st.warning(
                    "No ingredients detected."
                )


    # Ingredient text box

    user_ingredients = st.text_input(
        "Enter ingredients separated by commas",
        value=st.session_state.get(
            "image_ingredients",
            ""
        ),
        placeholder="chicken, rice, onion, tomato"
    )


    # --------------------------------
    # Find Recipes
    # --------------------------------

    if st.button("🔍 Find Recipes"):

        if not user_ingredients.strip():

            st.warning(
                "Please enter at least one ingredient."
            )

        else:

            # Give the chat a meaningful title
            if st.session_state.chat_session_id:

                from src.database import update_session_title

                update_session_title(
                    st.session_state.chat_session_id,
                    user_ingredients[:50]
                )
            # Save user message

            save_message(
                st.session_state.chat_session_id,
                "user",
                user_ingredients
            )


            # Get recommendations

            with st.spinner(
                "Finding the best recipes..."
            ):

                recommendations = recommend_recipes(
                    user_ingredients
                )


            # Save bot response

            recipes_for_history = []

            for _, recipe in recommendations.iterrows():

                recipes_for_history.append({
                    "name": recipe["name"],
                    "final_score": float(recipe["final_score"]),
                    "you_have": recipe["you_have"],
                    "you_need": recipe["you_need"],
                    "steps": recipe["steps"]
                })


            bot_message = json.dumps(
                recipes_for_history
            )

            save_message(
                st.session_state.chat_session_id,
                "bot",
                bot_message
            )


            # Display recommendations

            st.subheader(
                "🍽️ Recommended Recipes"
            )


            for _, recipe in recommendations.iterrows():

                st.markdown(
                    f"### 🍴 "
                    f"{recipe['name'].title()}"

                )
                st.write(
                    f"**Match Score:** "
                    f"{recipe['final_score']:.2%}"
                )

                st.write("**You have:**")

                for ingredient in recipe["you_have"]:

                    st.write(
                        f"✅ {ingredient}"
                    )


                st.write("**You need:**")

                for ingredient in recipe["you_need"]:

                    st.write(
                        f"🛒 {ingredient}"
                    )


                with st.expander(
                    "View Cooking Steps"
                ):

                    for i, step in enumerate(
                        recipe["steps"],
                        start=1
                    ):

                        st.write(
                            f"**{i}.** {step}"
                        )


                st.divider()