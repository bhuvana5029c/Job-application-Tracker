"""
application.py
Manages core actions on job applications: adding, viewing (with sorting/filtering),
updating status, and deleting.
"""

from datetime import date
from utils import (
    prompt_non_empty,
    prompt_date,
    prompt_status,
    print_table,
    print_success,
    print_error,
    clear_console,
    print_header
)
from storage import save_applications

def generate_id(applications):
    """
    Generates a unique sequential ID starting at 1001.
    """
    if not applications:
        return 1001
    return max(app["id"] for app in applications) + 1

def add_application(applications):
    """
    Prompts user for application details, creates a new entry, and saves it.
    """
    print_header("Add New Job Application")
    
    app_id = generate_id(applications)
    print(f"Generated Application ID: {app_id}")
    
    company = prompt_non_empty("Enter Company Name: ")
    role = prompt_non_empty("Enter Role/Position: ")
    location = prompt_non_empty("Enter Location (e.g. Remote, City Name): ")
    
    # Prompt for applied date, defaulting to today
    today_str = date.today().strftime("%Y-%m-%d")
    applied_date_input = input(f"Enter Applied Date (YYYY-MM-DD, or press Enter for today [{today_str}]): ").strip()
    if not applied_date_input:
        applied_date = today_str
    else:
        while True:
            from utils import validate_date
            try:
                validate_date(applied_date_input)
                applied_date = applied_date_input
                break
            except ValueError as e:
                print_error(str(e))
                applied_date_input = input("Enter Applied Date (YYYY-MM-DD): ").strip()
    
    # Select status
    status = prompt_status()
    
    # If the user selected an interview-related status, prompt for interview date
    interview_date = None
    if "Interview" in status:
        print("\nYou selected an interview status. Please specify the interview date.")
        interview_date = prompt_date("Enter Interview Date", optional=True)
    else:
        # Prompt for optional interview date
        interview_date = prompt_date("Enter Interview Date", optional=True)
        
    notes = input("Enter any Notes (optional): ").strip()
    
    new_app = {
        "id": app_id,
        "company": company,
        "role": role,
        "location": location,
        "applied_date": applied_date,
        "interview_date": interview_date if interview_date else None,
        "status": status,
        "notes": notes
    }
    
    applications.append(new_app)
    if save_applications(applications):
        print_success(f"Application for '{role}' at '{company}' added successfully!")
    else:
        print_error("Could not save the new application.")

def view_applications(applications, filter_status=None):
    """
    Displays all applications in a tabular format, sorted by applied date (newest first).
    Can filter applications by status.
    """
    title = "All Job Applications"
    apps_to_display = applications
    
    if filter_status:
        apps_to_display = [app for app in applications if app["status"].lower() == filter_status.lower()]
        title = f"Job Applications - Status: {filter_status}"
        
    # Sort applications by applied date descending (most recent first)
    apps_to_display = sorted(
        apps_to_display, 
        key=lambda x: x.get("applied_date", ""), 
        reverse=True
    )
    
    headers = ["ID", "Company", "Role", "Location", "Applied Date", "Interview Date", "Status", "Notes"]
    rows = []
    
    for app in apps_to_display:
        # Truncate notes for display formatting
        notes_display = app.get("notes", "")
        if len(notes_display) > 25:
            notes_display = notes_display[:22] + "..."
            
        rows.append([
            app.get("id"),
            app.get("company"),
            app.get("role"),
            app.get("location"),
            app.get("applied_date"),
            app.get("interview_date") if app.get("interview_date") else "-",
            app.get("status"),
            notes_display if notes_display else "-"
        ])
        
    print_table(headers, rows, title=title)

def update_status(applications):
    """
    Updates the status of an existing application.
    """
    print_header("Update Application Status")
    
    if not applications:
        print_error("No applications stored. Add some first.")
        return
        
    try:
        app_id_input = input("Enter the Application ID to update: ").strip()
        app_id = int(app_id_input)
    except ValueError:
        print_error("Invalid ID format. Please enter a valid number.")
        return
        
    # Find application
    target_app = None
    for app in applications:
        if app["id"] == app_id:
            target_app = app
            break
            
    if not target_app:
        print_error(f"Application with ID {app_id} not found.")
        return
        
    print(f"\nUpdating Application: {target_app['role']} at {target_app['company']}")
    print(f"Current Status: {target_app['status']}")
    
    # Prompt for new status
    new_status = prompt_status(current_status=target_app['status'])
    target_app["status"] = new_status
    
    # If updated status is interview related and there is no interview date, ask for one
    if "Interview" in new_status and not target_app.get("interview_date"):
        print("\nThis status is interview-related. Would you like to set an interview date?")
        int_date = prompt_date("Enter Interview Date", optional=True)
        if int_date:
            target_app["interview_date"] = int_date
            
    # Prompt for optional note update
    update_notes = input("Would you like to update the Notes? (y/n, press Enter to keep current): ").strip().lower()
    if update_notes == 'y':
        new_notes = input("Enter new notes: ").strip()
        target_app["notes"] = new_notes
        
    if save_applications(applications):
        print_success(f"Application ID {app_id} updated successfully!")
    else:
        print_error("Could not save updated status.")

def delete_application(applications):
    """
    Deletes an application by its ID.
    """
    print_header("Delete Application")
    
    if not applications:
        print_error("No applications stored. Add some first.")
        return
        
    try:
        app_id_input = input("Enter the Application ID to delete: ").strip()
        app_id = int(app_id_input)
    except ValueError:
        print_error("Invalid ID format. Please enter a valid number.")
        return
        
    # Find application
    target_idx = -1
    for idx, app in enumerate(applications):
        if app["id"] == app_id:
            target_idx = idx
            break
            
    if target_idx == -1:
        print_error(f"Application with ID {app_id} not found.")
        return
        
    app = applications[target_idx]
    print(f"\nSelected Application: ID {app['id']} | {app['role']} at {app['company']}")
    
    confirm = input("Are you sure you want to permanently delete this application? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        applications.pop(target_idx)
        if save_applications(applications):
            print_success(f"Application ID {app_id} deleted successfully!")
        else:
            print_error("Could not save changes after deletion.")
    else:
        print("\nDeletion cancelled.")
