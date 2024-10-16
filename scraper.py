import re
from github_scraper import GithubRepo, GithubFile, GithubFolder
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import request_headers, process_blobs, process_folder

class Scraper:
    
    def __int__(self):
        self.repository = None
    
    def does_repo_exist(self, user, repo, branch):
        '''
        Checks if the repository and branch exists or not.
        '''
        
        # resp = requests.get(api_url+"repos/"+user+"/"+repo)
        
        resp = requests.get(f"https://api.github.com/repos/{user}/{repo}", headers=request_headers)
        
        # Checking to see if the repo exists or not
        if resp.status_code == 404:
            return "Repository doesn't exist"
        elif resp.status_code != 200:
            return json.loads(resp.content)
        else:
            
            # checking to see if the branch exists or not
            if branch is not None:
                branch_resp = requests.get(f"https://api.github.com/repos/{user}/{repo}/branches", headers=request_headers)
                branches = [x['name'].lower() for x in json.loads(branch_resp.content)]

                if branch_resp.status_code != 200:
                    return "Error occurred try again"

                if branch.lower() not in branches:
                    return "Branch doesn't exist"
                        
        return json.loads(resp.content)
        
    def is_url_valid(self, url):
        '''
        Checks if the url is valid or not
        '''
        
        pattern = (
            r'^https:\/\/github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+$'  # https://github.com/{user}/{repo}
            r'|^https:\/\/github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+\/tree\/[a-zA-Z0-9._-]+$'  # https://github.com/{user}/{repo}/tree/{branch}
        )
        return re.fullmatch(pattern, url) is not None
        
    def get_repo_info(self, url):
        '''
        Extracts the username, repository name and branch from the url.
        '''
        
        base_url = [x for x in url.split("/") if x]
        
        user = base_url[2]
        repo = base_url[3]
        branch = None if len(base_url) <= 4 else base_url[-1]
        
        return user, repo, branch
    
    def get_repository(self, url):
    
        if not self.is_url_valid(url):
            return "Invalid url"
        
        user, repo, branch = self.get_repo_info(url)
        
        resp = self.does_repo_exist(user, repo, branch)


        if branch is None:
            branch = resp['default_branch']
        
        default_branch_url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}"
        response = requests.get(default_branch_url, headers=request_headers)
        
        if response.status_code != 200:
            return json.loads(response.content)
        
        self.repository = GithubRepo()
        self.repository.owner = user
        self.repository.branch = branch
        self.repository.url = url
        self.repository.repo_name = repo
        self.repository.file_structure = []
        
        files = json.loads(response.content)['tree']
        
        blobs = [x for x in files if x['type'] == "blob"]
        folders = [x for x in files if x['type'] == "tree"]        
        tasks = [(process_folder, f) for f in folders] + [(process_blobs, b) for b in blobs]
        

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(func, args): args for func, args in tasks}

            
            for future in as_completed(futures):
                self.repository.file_structure.append(future.result()) 
        
         
        # selecting the folders
        for x in filter(lambda x: isinstance(x, GithubFolder), self.repository.file_structure):
            self.repository.all_files.extend(x.get_all_files())

        # selecting the files
        for x in filter(lambda x: isinstance(x, GithubFile), self.repository.file_structure):
            self.repository.all_files.append(x.file_name)

        return self.repository

