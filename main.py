"""
main.py
The main entry point for the Job Application Tracker. Orchestrates
loading database records, presenting a console menu, and invoking module actions.
"""

import sys
from storage import load_applications
from application import (
    add_application,
    view_applications,
    update_status,
    delete_application
)
from search import search_applications, view_upcoming_interviews
from report import view_statistics, generate_success_rate_report
from utils import clear_console, print_header, print_error, prompt_status

def display_menu():
    """
    Prints the professional main menu options.
    """
    print_header("Job Application Tracker Dashboard")
    print("  [1] Add a New Job Application")
    print("  [2] View All Applications (Sorted by Applied Date)")
    print("  [3] Filter Applications by Status")
    print("  [4] Search Applications by Company or Role")
    print("  [5] Update Application Status")
    print("  [6] Delete an Application")
    print("  [7] View Application Statistics")
    print("  [8] View Upcoming Interviews (7-Day Outlook)")
    print("  [9] View Success-Rate & Funnel Report")
    print("  [10] Exit Program")
    print("-" * 60)

def main():
    """
    Main application loop.
    """
    # Load existing data on startup
    applications = load_applications()
    
    clear_console()
    print("Welcome to your Job Application Tracker!")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-10): ").strip()
        
        if choice == "1":
            clear_console()
            add_application(applications)
        elif choice == "2":
            clear_console()
            print_header("All Job Applications")
            view_applications(applications)
        elif choice == "3":
            clear_console()
            print_header("Filter Applications by Status")
            if not applications:
                print_error("No applications stored. Add some first.")
                continue
            status_filter = prompt_status()
            clear_console()
            view_applications(applications, filter_status=status_filter)
        elif choice == "4":
            clear_console()
            search_applications(applications)
        elif choice == "5":
            clear_console()
            update_status(applications)
        elif choice == "6":
            clear_console()
            delete_application(applications)
        elif choice == "7":
            clear_console()
            view_statistics(applications)
        elif choice == "8":
            clear_console()
            view_upcoming_interviews(applications)
        elif choice == "9":
            clear_console()
            generate_success_rate_report(applications)
        elif choice == "10":
            print("\nThank you for using Job Application Tracker. Good luck with your job hunt!")
            sys.exit(0)
        else:
            print_error("Invalid choice. Please enter a number between 1 and 10.")
            
        input("\nPress Enter to return to the Main Menu...")
        clear_console()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting. Good luck with your job search!")
        sys.exit(0)
