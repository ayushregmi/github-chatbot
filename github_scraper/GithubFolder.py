from github_scraper import GithubFile

class GithubFolder:
    def __init__(self):
        self.sha = None
        self.folder_name = None
        self.url = None
        self.file_structure = []
        
    def to_dict(self):
        return {
            "folder_name": self.folder_name,
            "type":"folder",
            "sub_folders": [x.to_dict() for x in self.file_structure]
        }
    
    def __str__(self, indent=0):
        
        sub_folders = "\n".join([x.__str__(indent=indent+1) for x in self.file_structure])
        
        return "---" * indent + f"{self.folder_name}\n{sub_folders}"

    def get_all_files(self):

        all_files = [self.folder_name]

        # selecting the folders
        for x in filter(lambda x: isinstance(x, GithubFolder), self.file_structure):
            # print(x.folder_name)
            all_files.extend([f"{self.folder_name}/"+y for y in x.get_all_files()])

        # selecting the files
        for x in filter(lambda x: isinstance(x, GithubFile), self.file_structure):
            all_files.extend([f"{self.folder_name}/"+x.file_name])
        
        return all_files

        # select all files
    
    def get(self, path):

        path = path.split("/")

        print(path)

        if len(path) == 1:
            
            if  path[0].lower() == self.folder_name.lower():
                return self
        
        # All files
        for x in filter(lambda x: isinstance(x, GithubFile), self.file_structure):
            if x.file_name.lower() == path[1].lower():
                return x

        # all folders
        for x in filter(lambda x: isinstance(x, GithubFolder), self.file_structure):

            if path[1].lower() == x.folder_name.lower():
                return x.get("/".join(path[1:]))
        
        return "Request folder/file doesn't exist"


