"""
utils.py
Helper functions and utilities for input validation, date operations, and terminal UI formatting.
"""

import os
from datetime import datetime

# Allowed status options for a job application
STATUS_OPTIONS = [
    "Applied",
    "OA Scheduled",
    "OA Completed",
    "Interview Scheduled",
    "Interview Completed",
    "HR Round",
    "Selected",
    "Rejected"
]

def clear_console():
    """
    Clears the console/terminal. Works on Windows and Unix-based systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """
    Prints a beautiful header block in the CLI.
    """
    border = "=" * 60
    print(f"\n{border}")
    print(f"{title.upper().center(60)}")
    print(f"{border}\n")

def print_success(message):
    """
    Prints a success message with clean formatting.
    """
    print(f"\n[+] SUCCESS: {message}\n")

def print_error(message):
    """
    Prints an error message with clean formatting.
    """
    print(f"\n[-] ERROR: {message}\n")

def validate_date(date_str):
    """
    Validates if a string is in YYYY-MM-DD format.
    Returns datetime.date if valid, otherwise raises ValueError.
    """
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

def prompt_non_empty(prompt_text):
    """
    Prompts the user for input and ensures it is not empty/whitespace only.
    """
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")

def prompt_date(prompt_text, optional=False):
    """
    Prompts the user for a date in YYYY-MM-DD format and validates it.
    If optional is True, allows the user to press Enter to skip.
    Returns the date string or None.
    """
    suffix = " (YYYY-MM-DD, or press Enter to skip): " if optional else " (YYYY-MM-DD): "
    while True:
        value = input(prompt_text + suffix).strip()
        if not value and optional:
            return None
        try:
            # Validate input format
            validate_date(value)
            return value
        except ValueError as e:
            print(f"Error: {e}")

def prompt_status(current_status=None):
    """
    Displays the list of status options and prompts the user to select one by number.
    If current_status is provided, marks it in the list.
    """
    print("\nSelect Application Status:")
    for idx, option in enumerate(STATUS_OPTIONS, 1):
        status_marker = " (Current)" if current_status == option else ""
        print(f"  [{idx}] {option}{status_marker}")
        
    while True:
        choice = input("\nEnter the number corresponding to the status: ").strip()
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(STATUS_OPTIONS):
                return STATUS_OPTIONS[choice_num - 1]
            print(f"Please enter a number between 1 and {len(STATUS_OPTIONS)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def print_table(headers, rows, title=None):
    """
    Prints data in a beautiful, aligned tabular format with unicode borders.
    headers: List of column header names.
    rows: List of lists/tuples containing row values.
    title: Optional string printed as a centered header.
    """
    if not rows:
        print("\n┌──────────────────────────────────────────────┐")
        print("│            No applications found             │")
        print("└──────────────────────────────────────────────┘\n")
        return

    # Convert all cell values to string
    str_rows = [[str(cell) if cell is not None else "" for cell in row] for row in rows]
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in str_rows:
        for idx, cell in enumerate(row):
            if idx < len(col_widths):
                col_widths[idx] = max(col_widths[idx], len(cell))
            else:
                col_widths.append(len(cell))
                
    # Build borders
    top_border    = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
    header_sep    = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
    bottom_border = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"
    
    if title:
        # Calculate total width of table (sum of cols + spacers)
        # 3 chars per border separator: ' │ '
        total_width = sum(col_widths) + 3 * (len(col_widths) - 1) + 2
        print(f"┌{'─' * total_width}┐")
        print(f"│{title.center(total_width)}│")
        print("├" + "┬".join("─" * (w + 2) for w in col_widths) + "┤")
    else:
        print(top_border)
        
    # Print headers
    header_str = "│ " + " │ ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " │"
    print(header_str)
    print(header_sep)
    
    # Print rows
    for row in str_rows:
        row_str = "│ " + " │ ".join(row[i].ljust(col_widths[i]) for i in range(len(col_widths))) + " │"
        print(row_str)
        
    print(bottom_border)
