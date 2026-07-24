"""
report.py
Generates statistics, summaries, and success rate analysis reports
for the job tracker.
"""

from datetime import datetime, date
from utils import print_table, print_header, print_error, STATUS_OPTIONS

def view_statistics(applications):
    """
    Displays overall dashboard statistics, including total count,
    breakdown by status, and applications submitted in the current month.
    """
    print_header("Application Statistics & Dashboard")
    
    if not applications:
        print_error("No applications registered yet. Statistics are not available.")
        return
        
    total_apps = len(applications)
    
    # 1. Status Breakdown
    status_counts = {status: 0 for status in STATUS_OPTIONS}
    for app in applications:
        status = app.get("status")
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = status_counts.get(status, 0) + 1
            
    status_headers = ["Status Option", "Count", "Percentage"]
    status_rows = []
    for status, count in status_counts.items():
        percentage = (count / total_apps) * 100 if total_apps > 0 else 0.0
        status_rows.append([status, str(count), f"{percentage:.1f}%"])
        
    # 2. Submitted This Month
    today = date.today()
    this_month_apps = []
    for app in applications:
        try:
            app_date = datetime.strptime(app["applied_date"], "%Y-%m-%d").date()
            if app_date.year == today.year and app_date.month == today.month:
                this_month_apps.append(app)
        except ValueError:
            pass
            
    print(f"Total Applications Tracker: {total_apps}")
    print(f"Applications Submitted this Month ({today.strftime('%B %Y')}): {len(this_month_apps)}\n")
    
    # Print status breakdown table
    print_table(status_headers, status_rows, title="Status Distribution Breakdown")
    
    # Print applications submitted this month
    if this_month_apps:
        month_headers = ["ID", "Company", "Role", "Applied Date", "Status"]
        month_rows = []
        for app in this_month_apps:
            month_rows.append([
                app.get("id"),
                app.get("company"),
                app.get("role"),
                app.get("applied_date"),
                app.get("status")
            ])
        print_table(month_headers, month_rows, title=f"Applications Submitted in {today.strftime('%B %Y')}")
    else:
        print(f"--- No applications submitted in {today.strftime('%B %Y')} yet ---\n")

def generate_success_rate_report(applications):
    """
    Generates a recruitment conversion funnel and success rate analysis.
    """
    print_header("Success Rate & Funnel Report")
    
    if not applications:
        print_error("No applications registered yet. Funnel reports are not available.")
        return
        
    total_apps = len(applications)
    
    # Funnel Metric Calculations
    selected_count = 0
    rejected_count = 0
    interview_secured = 0
    active_count = 0
    
    for app in applications:
        status = app.get("status", "")
        int_date_str = app.get("interview_date")
        
        # Count selected/rejected
        if status == "Selected":
            selected_count += 1
        elif status == "Rejected":
            rejected_count += 1
        else:
            active_count += 1
            
        # Count interviews secured (either by status or if interview date was scheduled)
        is_interview_status = any(s in status for s in ["Interview", "HR", "Selected"])
        if is_interview_status or int_date_str:
            interview_secured += 1
            
    decided_apps = selected_count + rejected_count
    
    # Percentages
    interview_rate = (interview_secured / total_apps) * 100 if total_apps > 0 else 0.0
    offer_rate = (selected_count / total_apps) * 100 if total_apps > 0 else 0.0
    success_rate = (selected_count / decided_apps) * 100 if decided_apps > 0 else 0.0
    
    # Display the funnel metrics
    print(f"{'Funnel Metric':<30} | {'Value':<10} | {'Conversion Rate'}")
    print("-" * 65)
    print(f"{'Total Job Applications':<30} | {total_apps:<10} | 100.0%")
    print(f"{'Interviews Secured':<30} | {interview_secured:<10} | {interview_rate:.1f}% of total applications")
    print(f"{'Offers Received (Selected)':<30} | {selected_count:<10} | {offer_rate:.1f}% of total applications")
    print("-" * 65)
    
    print("\n[ Analysis & Verdict ]")
    print(f" - Active Applications (In-Progress): {active_count}")
    print(f" - Completed Applications (Decided) : {decided_apps} (Offers: {selected_count}, Rejections: {rejected_count})")
    
    if decided_apps > 0:
        print(f" - Interview-to-Offer Success Rate  : {success_rate:.1f}% (Offer / Decided applications)")
        if success_rate >= 50.0:
            verdict = "Excellent performance! Keep negotiating and reviewing offer details."
        elif success_rate >= 25.0:
            verdict = "Healthy success rate. Good interview conversion."
        else:
            verdict = "Success rate is lower. Consider practicing mock interviews or refining your resume."
        print(f" - Strategy Verdict                 : {verdict}")
    else:
        print(" - Interview-to-Offer Success Rate  : N/A (No applications have reached Selected or Rejected status yet)")
        print(" - Strategy Verdict                 : Awaiting final decisions to compute success rate.")
    print()
