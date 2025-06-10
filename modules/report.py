class Report:
    def __init__(self, pr_number: int, pr_title: str, author: str, merge_date, CR_passed: bool, passed_checks: bool):
        self.pr_number = pr_number
        self.pr_title = pr_title
        self.author = author
        self.merge_date = merge_date
        self.CR_passed = CR_passed
        self.passed_checks = passed_checks