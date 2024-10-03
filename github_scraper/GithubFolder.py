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
