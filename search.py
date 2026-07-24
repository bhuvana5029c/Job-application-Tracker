"""
search.py
Contains search and filtering features, including matching company/role
and retrieving upcoming interviews within the next 7 days.
"""

from datetime import datetime, date, timedelta
from utils import print_table, print_header, print_error

def search_applications(applications):
    """
    Search applications by company name or role (case-insensitive substring match).
    """
    print_header("Search Applications")
    
    if not applications:
        print_error("No applications to search. Add some first.")
        return
        
    query = input("Enter company name or role to search for: ").strip().lower()
    if not query:
        print_error("Search query cannot be empty.")
        return
        
    results = []
    for app in applications:
        company = app.get("company", "").lower()
        role = app.get("role", "").lower()
        if query in company or query in role:
            results.append(app)
            
    # Sort results by applied date descending (newest first)
    results = sorted(results, key=lambda x: x.get("applied_date", ""), reverse=True)
    
    headers = ["ID", "Company", "Role", "Location", "Applied Date", "Interview Date", "Status", "Notes"]
    rows = []
    
    for app in results:
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
        
    print_table(headers, rows, title=f"Search Results for '{query}'")

def view_upcoming_interviews(applications):
    """
    Finds and displays applications with interview dates scheduled in the next 7 days.
    """
    print_header("Upcoming Interviews (Next 7 Days)")
    
    if not applications:
        print("No applications registered.")
        return
        
    today = date.today()
    seven_days_later = today + timedelta(days=7)
    
    upcoming_list = []
    for app in applications:
        int_date_str = app.get("interview_date")
        if int_date_str:
            try:
                int_date = datetime.strptime(int_date_str, "%Y-%m-%d").date()
                if today <= int_date <= seven_days_later:
                    upcoming_list.append((int_date, app))
            except ValueError:
                # Silently skip bad dates if any (data integrity check)
                pass
                
    # Sort by interview date ascending (earliest first)
    upcoming_list.sort(key=lambda x: x[0])
    upcoming_apps = [item[1] for item in upcoming_list]
    
    headers = ["ID", "Company", "Role", "Interview Date", "Status", "Location"]
    rows = []
    
    for app in upcoming_apps:
        rows.append([
            app.get("id"),
            app.get("company"),
            app.get("role"),
            app.get("interview_date"),
            app.get("status"),
            app.get("location")
        ])
        
    print_table(headers, rows, title=f"Interviews from {today.strftime('%Y-%m-%d')} to {seven_days_later.strftime('%Y-%m-%d')}")
