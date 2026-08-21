from src.auth import login_user

success, result = login_user(
    username="testuser123",
    phone="9999999999",
    password="TestPassword123"
)

if success:
    print("Login successful!")
    print("User:", result["name"])
    print("Username:", result["username"])
else:
    print("Login failed:")
    print(result)