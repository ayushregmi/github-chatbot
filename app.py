import streamlit as st
from pydantic import BaseModel, Field

from langchain.tools import StructuredTool

from Agent import Agent

st.title("Github Chatbot")

from scraper import Scraper


def append_message(message, agent):
    st.session_state.messages.append({"content":message, "role":agent})
# Tools
class SearchPathInput(BaseModel):
    name: str=Field("The name of file/folder whose path is needed")

def search_path(name:str)->str:
    '''
    Searches for a file in the repository by its filename.

    This function looks through all files in the repository's `all_files` collection 
    to find a match for the provided filename. The search is case-insensitive and 
    only considers the filename itself, without any directory paths.

    Args:
        name (str): The name of the file to search for (e.g., 'input.jsx'). 
                    This should be just the filename without any path.

    Returns:
        str: The full path of the file if found. If the file is not present 
             in the repository, returns the string "File not found".

    Example:
        If the repository contains a file at '/src/components/input.jsx' 
        and you search with 'input.jsx', this function will return 
        '/src/components/input.jsx'. However, searching with 
        '/src/components/input.jsx' will result in "File not found".
    '''
    
    for f in st.session_state.repo.all_files:
        if f.lower().endswith(name.lower()):
            return f
    
    return "File not found"
search_path_tool = StructuredTool.from_function(func=search_path, tool="search_path", args_schema=SearchPathInput)

class GetFileContentInput(BaseModel):

    path: str=Field("The path of file that needs to be summarized")

def get_file_content(path:str)->str:
    """
    Retrieves the content of a file given its full path.

    This function checks if the specified path points to a valid file 
    within the repository. If the path is invalid or the file does 
    not exist, it will return an appropriate error message. 
    It is important to provide the full path to the file, not just 
    the filename.

    Args:
        path (str): The full path to the file whose content is to be retrieved.

    Returns:
        str: The content of the file if it exists. If the path is invalid 
             or the file is not found, returns "File not found". 
             If the repository is not initialized, returns "Repository not initialized".

    Example:
        If the repository contains a file at '/src/components/input.jsx' 
        and you call `get_file_content('/src/components/input.jsx')`, 
        it will return the content of that file. 
        If you call `get_file_content('invalid/path/file.txt')`, 
        it will return "File not found".
    """

    path = path.strip()

    if st.session_state.repo == None:
        return "Repository not initialized"
    
    f = st.session_state.repo.get(path)

    if isinstance(f, str):
        return "File not found"
    
    return f.content

get_file_content_tool = StructuredTool.from_function(func=get_file_content, tool="get_file_content", args_schema=GetFileContentInput)

def repo_info():
    """
    Retrieves general information about the repository.

    This function provides key details about the repository, including 
    the repository name, owner, current branch, and a list of files 
    contained within it.

    Returns:
        dict: A dictionary containing the following information about the repository:
            - "repository name": The name of the repository.
            - "owner": The owner of the repository.
            - "branch": The current branch of the repository.
            - "files": A list of all files in the repository.

    Example:
        {
            "repository name": "example-repo",
            "owner": "user123",
            "branch": "main",
            "files": ["/src/components/input.jsx", "/src/utils/helpers.js"]
        }
    """

    return {
        "repostory name":st.session_state.repo.repo_name,
        "owner": st.session_state.repo.owner,
        "branch": st.session_state.repo.branch,
        "files": st.session_state.repo.all_files
    }

repo_info_tool = StructuredTool.from_function(func=repo_info, name="get_repository_info")

if 'repo_link' not in st.session_state:
    st.session_state.repo_link = ''
    st.session_state.repo = None
    st.session_state.text_disabled = False
    st.session_state.loading_repo = False
    st.session_state.messages = []
    st.session_state.loaded_repo = None
    st.session_state.tools = [repo_info_tool, search_path_tool, get_file_content_tool]
    st.session_state.agent = Agent(tools=st.session_state.tools)

with st.sidebar: 
    st.text_input(label="Link", label_visibility='collapsed', key="repo_link", placeholder="Github repository link", disabled=st.session_state.text_disabled)
    if st.session_state.repo_link and st.session_state.repo_link != st.session_state.loaded_repo:
        st.session_state.loaded_repo = st.session_state.repo_link
        with st.spinner("Loading Repository"):
            st.markdown("<small>*Loading time varies according to the size of the repository*</small>", unsafe_allow_html=True)
            try:
                st.session_state.repo = Scraper().get_repository(st.session_state.repo_link)
                if isinstance(st.session_state.repo, str):
                    st.write(f":red[Error: {st.session_state.repo}]")
                    st.session_state.repo = None
                else:
                    st.write(f":green[Imported Repository]", )
            except Exception as e:
                print(e)
                st.write(f":red[Error {e}]")

if st.session_state.repo is not None:

    prompt = st.chat_input("Ask me something...")
    
    if prompt:
        append_message(prompt, "user")

        response = st.session_state.agent(prompt)

        append_message(response['output'], "assistant")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

