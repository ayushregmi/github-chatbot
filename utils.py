import os
from dotenv import load_dotenv
from github_scraper import *
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import base64

load_dotenv()

request_headers = {
        'Authorization': f'token {os.getenv("GITHUB_ACCESS_TOKEN")}',
        'Accept': 'application/vnd.github.v3+json'
}

# files_to_ignore = [".gif", ".svg", ".png", ".gitignore", ".jpeg", ".jpg", ".pdf"]
supported_files = [".py", ".hpp", ".cpp", ".h", ".c", ".js", ".jsx", ".ts", ".tsx", ".css", ".html", ".java"]


def check_supported_language(string):
    
    '''
    Checking to see if the file can be ignored or not.
    
    Parameters:
        - string(str): file name to check if it can be ignore or not
    
    Returns:
        - bool
    
    '''
    
    return any(string.endswith(substring) for substring in supported_files)

def decode_base64(encoded_str):
    
    '''
    Convert base64 encoding to string
    
    Parameters:
        - encoded_str(str): base64 encoded string
        
    Returns:
        - str: decodes the encoded string
    
    
    '''
    
    # Decode the Base64 string
    decoded_bytes = base64.b64decode(encoded_str)
    # Convert bytes to a string
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def process_folder(f):
    
    '''
    Get the files and sub folders present in the give folder.
    
    Parameters:
        - f(requests.Response): the response of the api call to the folder tree
    
    Returns: 
        - GithubFolder(obj): Github Folder object with all the subfolers and files.
    
    '''
    
    folder = GithubFolder()
    folder.folder_name = f['path']
    folder.sha = f['sha']
    folder.url = f['url']
    folder.file_structure = []
    
    resp = requests.get(folder.url, headers=request_headers)
    
    if resp.status_code != 200:
        print(f"Error trying to access {folder.folder_name}")
    
    else:
        print(f"Reading: {folder.folder_name}")
        files = json.loads(resp.content)['tree']
        blobs = [x for x in files if x['type'] == "blob"]
        folders = [x for x in files if x['type'] == "tree"]

        tasks = [(process_folder, f) for f in folders] + [(process_blobs, b) for b in blobs]
        
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(func, args): args for func, args in tasks}
        
        # with ThreadPoolExecutor() as executor:
        #     futures = {executor.submit(process_blobs, b): b for b in blobs}    

            
            for future in as_completed(futures):
                folder.file_structure.append(future.result()) 
    
    return folder
    
def process_blobs(b):
    
    '''
    Creates a GithubFile object and fills in data.
    
    Parameters:
        - b (requests.Response): the response of calling the blob url.
    
    Returns:
        - GithubFile (obj): a GithubFile object with the contents of the file
    '''
        
    blob = GithubFile()
    blob.file_name = b['path']
    blob.sha = b['sha']
    blob.size = b['size']
    
    try:
        if check_supported_language(blob.file_name):
            print(f"Reading: {blob.file_name}")
            blob = read_blobs(b['url'], blob)
            
        else:
            print(f"Skipping: {blob.file_name}")
    except Exception as e:
        print(f"Error Reading file {blob.file_name}\n{e}")
    return blob
    

def read_blobs(url, gh_file_obj):
    
    response = requests.get(url, headers=request_headers)
    
    if response.status_code == 200:
        encoded_string = json.loads(response.content)['content']
        
        decoded = decode_base64(encoded_str=encoded_string)
        gh_file_obj.content = decoded        
    else:
        print(f"Error occured trying to read: {gh_file_obj.file_name}")
    
    return gh_file_obj