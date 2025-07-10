from .common import prompt, currtime
from .file_ops import load_file
from .config import USER_FILE

def err_message(username, msg, role):
    print(f"\n🚫 '{username}' is not authorized to '{msg}' bugs. Only users with the '{role}' role can do this.")

def invalid_msg(field, output):
    print(f"\n❌ Invalid {field}: {output}")
    print(f"Please choose {field} only from the available configuration.\n")

def is_authentic_user(user, users):
    return any(u["username"] == user for u in users)

def is_valid_user_for_role(inp_msg, expected_role, err_msg, emoji, emoji_width=2):
    users = load_file(USER_FILE)

    while True:
        inp_field = prompt(emoji, inp_msg, emoji_width)
        is_user = is_authentic_user(inp_field, users)

        if not is_user:
            invalid_msg("user", inp_field)
        else:
            is_valid_role = any(user["username"] == inp_field and user["role"] == expected_role for user in users)
            
            if not is_valid_role:
                err_message(inp_field, err_msg, f"{emoji}  {expected_role}")
            else:
                return inp_field
