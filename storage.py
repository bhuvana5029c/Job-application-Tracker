"""
storage.py
Handles reading from and writing to the JSON file for persistent application storage.
"""

import json
import os
from utils import print_error, print_success

# Define storage file path relative to this script's directory
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "applications.json")

def load_applications():
    """
    Loads job applications from the JSON database file.
    If the file does not exist, it is created with an empty list.
    If the file is corrupted, it initializes an empty list and prints an error.
    """
    if not os.path.exists(DB_FILE):
        # Auto-create file with empty list
        save_applications([])
        return []
    
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print_error("Database file (applications.json) is corrupted. Starting with an empty application list.")
        # Backup the corrupted file
        backup_name = DB_FILE + ".bak"
        try:
            os.rename(DB_FILE, backup_name)
            print(f"[!] Corrupted file backed up as: {backup_name}")
        except Exception:
            pass
        save_applications([])
        return []
    except Exception as e:
        print_error(f"Unexpected error loading database: {e}")
        return []

def save_applications(applications):
    """
    Saves the list of job applications to the JSON database file.
    Returns True if save was successful, False otherwise.
    """
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(applications, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print_error(f"Failed to save data to database: {e}")
        return False
