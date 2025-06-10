from modules.pr import PullRequest
from modules.report import Report
import extract
import queue

def compute_pull_requests(pull_requests: list, pull_request_converter_input_queue: queue.Queue):
    """
    input: pr's list, input queue for the pr converter Thread
    """
    print("Starting to compute pr's")

    #each iteration converts a pr dict to PullRequest object
    #checks if all pr checks passed
    #checks if there is an approved review
    #generates a report from the information above
    #sends the report to the input queue
    for raw_pr in pull_requests:
        parsed_pr = create_parsed_pr(raw_pr)
        
        if parsed_pr == None:
            continue
        
        passed_checks = passed_all_checks(parsed_pr.sha)
        passed_reviews = has_review_approval(parsed_pr.number)
        report = generate_report(parsed_pr, passed_checks, passed_reviews)
        pull_request_converter_input_queue.put(report)
    print("finished computing pr's")

def generate_report(parsed_pr: PullRequest, passed_checks: bool, passed_reviews: bool):
    """
    input: a PullRequest object,
    a boolean indicating if the pr passed all checks,
    a boolean indicating if the pr passed atleast 1 review
    output: Report object containing information on the pr
    """
    report = Report(parsed_pr.number, parsed_pr.title, parsed_pr.author, parsed_pr.merge_date, passed_reviews, passed_checks)
    return report

def create_parsed_pr(raw_pr: dict)-> PullRequest|None:
    """
    input: dict
    output: PullRequest
    This function creates a PullRequest from the pull request dict
    it recives from the input. If the merged_at key in the dict is None
    the function returnes None(it means the pr was not merged)
    """
    pr_merge_date = raw_pr["merged_at"]

    #Checks if the pr was merged
    if pr_merge_date == None:
        return None
    
    pr_sha = raw_pr['head']['sha']
    pr_number = raw_pr['number']
    pr_author = raw_pr['user']['login']
    pr_title = raw_pr['title']
    parsed_pull_request = PullRequest(pr_number, pr_title, pr_author, pr_sha, pr_merge_date)
    return parsed_pull_request

def has_review_approval(pr_number: int):
    """
    input: pull request number
    output: boolean
    This function gets a list of reviews on the pr
    and checks if there is an approved review
    otherwise returnes false
    """
    reviews_list = extract.get_reviews(pr_number)
    for review in reviews_list:
        if review['state'] == "APPROVED":
            return True
    return False

def passed_all_checks(pr_sha: str):
    """
    input: pull request sha
    output: boolean
    This function gets a list of checks that the pr needs to pass,
    if there isn't a check that didn't pass returns True
    """
    check_list = extract.get_check_list(pr_sha)
    for check in check_list:
        if check['status'] != 'completed' or check['conclusion'] != 'success':
            return False
    return True