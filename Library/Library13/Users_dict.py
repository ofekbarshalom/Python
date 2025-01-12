from FileHandler import FileHandler
from Book import Book
from queue import Queue
from path import Paths
import pandas as pd

users_dict = {}

def initialize_users_dict():
    global users_dict
    users_dict = FileHandler.create_users_dict_from_csv()
    print("Global users_dict has been initialized.")

def add_user_to_dict(user):
    if user.name in users_dict:
        print(f"User '{user.name}' already exists in the dictionary.")
        return
    users_dict[user.name] = user
    print(f"User '{user.name}' added to the dictionary.")

def remove_user_from_dict(username):
    if username in users_dict:
        del users_dict[username]
        print(f"User '{username}' removed from the dictionary.")
        return
    print(f"User '{username}' not found in the dictionary.")

def get_user_object(username):
    if username in users_dict:
        return users_dict[username]
    else:
        print(f"User '{username}' not found in the dictionary.")
        return None

def update_user_messages(username, message):
    if username in users_dict:
        user = users_dict[username]
        user.update(message)
        print(f"Message added to user '{username}': {message}")
        return True
    print(f"User '{username}' not found in the dictionary.")
    return False

def print_dict():
    if not users_dict:
        print("The users_dict is empty.")
        return

    print("Current users in the dictionary:")
    for username, user in users_dict.items():
        print(f"Username: {username}, Messages: {user.messages}")

