from github_scraper import GithubFolder, GithubFile

class GithubRepo:
    def __init__(self):
        self.owner = None
        self.repo_name = None
        self.branch = None
        self.file_structure = []
        self.url = None
        self.all_files = []
    
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
    
    def get(self, path):

        '''
        path: "/public/../.."
        '''

        if self.file_structure == None:
            return "Repo empty"
        
       
            
        

        paths = [x for x in path.split("/") if x]

        if len(paths) == 1:
            # selecting the files
            for x in filter(lambda x: isinstance(x, GithubFile), self.file_structure):
                if paths[0].lower() == x.file_name.lower():
                    return x

        # selecting the folders
        for x in filter(lambda x: isinstance(x, GithubFolder), self.file_structure):
            if x.folder_name.lower().strip() == paths[0].lower().strip():
                return x.get("/".join(paths))

        return "File/Folder doesn't exist"



