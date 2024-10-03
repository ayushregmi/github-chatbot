from github_scraper import GithubFolder

class GithubRepo:
    def __init__(self):
        self.owner = None
        self.repo_name = None
        self.branch = None
        self.file_structure = [None]
        self.url = None
    
    def to_dict(self):
        return {
            "repository_name":self.repo_name,
            "repository_owner": self.owner,
            "current_branch":self.branch,
            "repo_url": self.url,
            "folders": [x.to_dict() for x in self.file_structure]
        }
        
    def __str__(self):
        
        sub_folders = "\n".join([x.__str__(indent=0) for x in self.file_structure])
        return f"{self.owner}\n{self.repo_name}\n{self.branch}\n\n\n{sub_folders}"
    
    def get_all_files(self):
        names = [x['folder_name'] if isinstance(x, GithubFolder) else x['file_name'] for x in self.file_structure]
        return names