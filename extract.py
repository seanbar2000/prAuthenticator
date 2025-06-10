import requests
import os
#dont add .env to repo in github!!!!
# ------------------ GLOBALS ------------------ #
personal_access_token = os.getenv("GITHUB_TOKEN")
account_name = os.getenv("ACCOUNT_NAME")
repo_name = os.getenv("GITHUB_REPO")  # CHANGE THIS
base_github_api_url = os.getenv("BASE_GITHUB_URL")
headers = {
    "Authorization": f"token {personal_access_token}",
    "Accept": "application/vnd.github+json"
}
# ------------------------------------------- #


def fetch_merged_pull_requests(page: int)-> list|None:
    """
    input: integer which represents the page of pr's we recieve from the request
    return: a list of pr's from the repo or None if there are no pr's
    """
    print("Fetching merged pr's")
    url = f"{base_github_api_url}/repos/{account_name}/{repo_name}/pulls"
    if page == 1:
        params = {
            "state": "closed",
            "sort": "updated",
            "direction": "desc",
        }
    else:
        params = {
            "state": "closed",
            "sort": "updated",
            "direction": "desc",
            "page": page
        }

    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 404:
        print("There are no merged pr's")
        return None

    prs = res.json()
    print("Finished fetching merged pr's")
    print(len(prs))
    return prs


def get_reviews(pr_number: int)-> list:
    """
    input: pull request number
    output: a list of reviews
    """
    url = f"https://api.github.com/repos/{account_name}/{repo_name}/pulls/{pr_number}/reviews"
    raw_review_data = requests.get(url, headers=headers)
    reviews_list = raw_review_data.json()
    return reviews_list


def get_check_list(pr_sha: str)-> list:
    """
    input: pull request sha
    output: a list of checks
    """
    response = requests.get(f"{base_github_api_url}/repos/{account_name}/{repo_name}/commits/{pr_sha}/check-runs", headers=headers)
    jsonified_response = response.json()
    checks = jsonified_response["check_runs"]
    return checks
