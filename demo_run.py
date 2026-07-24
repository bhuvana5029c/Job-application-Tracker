"""
demo_run.py
Runs a non-interactive demonstration of the Job Application Tracker
to display the formatting, tables, statistics, and reports.
Saves the console output to output_demo_py.txt in UTF-8.
"""

import sys
import os

# Redirect stdout to both console and a UTF-8 file
class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# Set up logging to output_demo_py.txt in the same directory
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_demo_py.txt")
sys.stdout = Logger(log_path)

from storage import load_applications
from application import view_applications
from search import search_applications, view_upcoming_interviews
from report import view_statistics, generate_success_rate_report
from utils import print_header

def run_demo():
    print_header("Job Application Tracker - Live Demo")
    
    # 1. Load applications
    print("[1] Loading applications from database...")
    apps = load_applications()
    print(f"Loaded {len(apps)} applications successfully.\n")
    
    # 2. View All Applications
    print("[2] Displaying all applications (sorted by Applied Date):")
    view_applications(apps)
    
    # 3. Filter Applications by Status
    print("[3] Filtering applications by status 'Selected':")
    view_applications(apps, filter_status="Selected")
    
    # 4. Search Applications
    print("[4] Searching applications for query 'meta':")
    # Mocking input query by replacing input() temporarily
    import builtins
    original_input = builtins.input
    builtins.input = lambda _: "meta"
    try:
        search_applications(apps)
    finally:
        builtins.input = original_input
        
    # 5. View Upcoming Interviews
    print("[5] Checking upcoming interviews (7-Day Outlook):")
    view_upcoming_interviews(apps)
    
    # 6. View Statistics
    print("[6] Generating Dashboard Statistics:")
    view_statistics(apps)
    
    # 7. View Funnel Report
    print("[7] Generating Success-Rate & Funnel Report:")
    generate_success_rate_report(apps)

if __name__ == "__main__":
    run_demo()
    # Close stdout log file
    sys.stdout.log.close()
