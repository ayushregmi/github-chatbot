from langchain_groq import ChatGroq
from langchain import hub

from langchain.agents import create_tool_calling_agent, AgentExecutor

class Agent:
    def __init__(self, tools):
        self.tools = tools
        self.llm = ChatGroq(temperature=0.0, model="llama-3.1-70b-versatile")
        self._create_agent()
        self._create_agent_executor()
    
    def _create_agent(self):
        prompt = hub.pull("hwchase17/openai-functions-agent")
        prompt.messages[0].prompt.template = """You are a helpful AI assistant. 
        You can provide information about owners, commit counts, file contents, folder structures, and more.
        Always use the appropriate tool for each task, and make sure to search and provide the correct file/folder paths when using the tools.
        If a tool returns an error message, relay that message to the user and offer suggestions on how to proceed or ask for clarification."""
        prompt.messages[2].prompt.template = """Greet the user accordingly, and use the tools to answer the question. Return the tool output as it is unless instructed in the input.
        When summarizing and explaining files return the codes in them as well.
        Input: {input}"""

        self.agent = create_tool_calling_agent(llm=self.llm, tools=self.tools, prompt=prompt)
    
    def _create_agent_executor(self):

        self.agent_executor = AgentExecutor(tools=self.tools, agent=self.agent, llm=self.llm)


    def __call__(self, query):
        return self.agent_executor.invoke({"input":query})
    
