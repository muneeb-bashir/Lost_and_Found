import re

email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
password_regex = "^(?=.*\d)(?=.*[a-z])(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*#?&]).{8,}$"


def password_is_valid(password):
    return bool(re.match(password_regex, password))


def email_is_valid(email):
    return bool(re.match(email_regex,email))


def username_valid(username):
    return len(username) <= 100
