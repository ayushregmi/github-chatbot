# GitHub Chatbot

## Overview

The GitHub Chatbot allows users to interact with GitHub repositories in a conversational manner. By utilizing the GitHub API and Langchain agents, this project enables users to ask questions about the contents of a repository, and the chatbot can access and read files to provide insightful answers.

## Features

- **Repository Scraping:** The chatbot scrapes the specified GitHub repository to gather relevant information.
- **File Access:** It can read various files within the repository, such as README.md, source code files, and documentation.
- **Conversational Interface:** Users can interact with the chatbot in natural language, asking questions about the repository’s structure, content, and purpose.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- GitHub API token
- GROQ API token

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ayushregmi/github-chatbot
   cd github-chatbot
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file in the root directory and add your API tokens:

   ```bash
   GITHUB_TOKEN=your_github_api_token
   GROQ_TOKEN=your_groq_api_token
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

### Example Questions
- "What files are in this repository?"
- "Can you summarize the README?"
- "What does this function do in main.py?"