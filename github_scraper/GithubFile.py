class GithubFile:
    def __init__(self):
        self.sha = None
        self.file_name = None
        self.content = None
        self.size = None
    
    def to_dict(self):
        return {
            "file_name":self.file_name,
            "type":"file",
            "size":self.size,
            "content":self.content
        }
        
    def __str__(self, indent=0):
        return "---" * indent + self.file_name
