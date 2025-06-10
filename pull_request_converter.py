import queue
import threading
from modules.report import Report
import pandas as pd

class PullRequestConverter(threading.Thread):
    def __init__(self, input_queue: queue.Queue):
        super().__init__()
        self.input_queue = input_queue

    def generate_csv(self, report: Report):
        data = {
            "PR_Number": report.pr_number,
            "Title": report.pr_title,
            "Author": report.author,
            "Merge_Date": report.merge_date,
            "CR_PASSED": report.CR_passed,
            "CHECKS_PASSED": report.passed_checks
        }
        df = pd.DataFrame([data])
        file_name = self.generate_file_name(report)
        if report.CR_passed == True and report.passed_checks == True:
            df.to_csv(f"reports/pass/{file_name}", index=False)
        
        else:
            if report.CR_passed == False:
                df.to_csv(f"reports/didn't_pass/review/{file_name}", index=False)
            
            if report.passed_checks == False:
                df.to_csv(f"reports/didn't_pass/checks/{file_name}", index=False)
            

    def generate_file_name(self, report: Report):
        file_path = f"pr_report_{report.pr_number}.csv"
        return file_path

    def consume_input(self): 
        report = self.input_queue.get()
        return report

    
    def run(self):
        while True:
            report = self.consume_input()
            if type(report) != Report:
                break
            self.generate_csv(report)
