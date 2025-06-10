class PullRequest:
    def __init__(self, pr_number, pr_title, pr_author, sha, merge_date):
        self.number = pr_number
        self.title = pr_title
        self.author = pr_author
        self.sha = sha
        self.merge_date = merge_date