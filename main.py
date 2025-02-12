from agno.agent import Agent
from agno.document import Document
from agno.knowledge.document import DocumentKnowledgeBase
from agno.models.openai import OpenAIChat
from agno.agent import RunResponse  # noqa
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.tools.tavily import TavilyTools
from models.verifyLLMResponseModel import VerifyLLMResponseModel
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from config import AI_ASSISTANT_NAME, USER_NAME, EXIT_COMMANDS, LLM_MAX_ATTEMPTS, INFOS, WELCOME_MESSAGE, END_MESSAGE

# global Variables
knowledgeBase: DocumentKnowledgeBase | None = None
agent: Agent | None = None
console = Console()

def LoadKnowledgeBase():
    global knowledgeBase

    # configure vectorstore
    vectorstore: LanceDb = LanceDb(
        table_name = "xstudios",
        uri = "db/lancedb",
        search_type = SearchType.vector,
        embedder = OpenAIEmbedder(id = "text-embedding-3-small")
    )

    # convert infos to documents
    documents: list[Document] = [Document(content = info) for info in INFOS]
    # create knowledge base
    knowledgeBase = DocumentKnowledgeBase(
        path = "db/lancedb",
        vector_db = vectorstore,
        documents = documents,
    )

    # load knowledge base
    knowledgeBase.load(recreate = False)


def CreateAgent():
    global agent

    agent = Agent(
    model = OpenAIChat(id = "gpt-4o-mini"),
    knowledge = knowledgeBase,
    tools = [TavilyTools()],
    add_references = True,
    search_knowledge = True,
    show_tool_calls = True,
    add_history_to_messages = True, # be careful when using this
    #debug_mode = True,
    #markdown = True,
    description = """
    You are a helpful assistant that can answer questions about the company.
    When answering questions:
    1. ALWAYS search the knowledge base first
    2. If information is found in the knowledge base:
    - Provide ONLY the information found in the knowledge base
    - Do not add any interpretations or additional comments
    - Be precise and factual
    - Only state what is explicitly mentioned

    3. If information is NOT found in the knowledge base:
    - Use Tavily to search the internet
    - Clearly indicate that the information comes from web search
    - Provide a clear and concise answer based on the search results

    Remember: Never mix knowledge base information with web search results. Either use one or the other.
    """
)

def VerifyLLMResponse(query: str, response: RunResponse) -> VerifyLLMResponseModel:
    prompt: str = f"""
    Query: {query}
    Response: {response.content}
    
    You are the verify agent. Check the hallucination according to the response and query you receive. If there is no error in the response, just return True. If there is an error, just return False. Do not use any tools while doing this.
    """

    verifyAgent = Agent(
        model = OpenAIChat(id = "gpt-4o-mini"),
        description = prompt,
        response_model = VerifyLLMResponseModel,
        structured_outputs = True,
        #debug_mode = True,
        #markdown = True
    )
    
    result: RunResponse[VerifyLLMResponseModel] = verifyAgent.run(message = prompt)
    return result.content

def GetAgentResponse(query: str) -> VerifyLLMResponseModel | str:
    attempt: int = 0

    while attempt < LLM_MAX_ATTEMPTS:
        response: RunResponse = agent.run(message = query)
        verifyResult: VerifyLLMResponseModel = VerifyLLMResponse(query, response)

        if verifyResult.isValid:
            return response.content
        
        attempt += 1

    return "Sorry, I cannot generate a reliable response. Please ask your question in more detail or more accurately."

def main():
    LoadKnowledgeBase()
    CreateAgent()
    console.print(Panel(WELCOME_MESSAGE, title = f"{AI_ASSISTANT_NAME}".upper(), border_style = "magenta3"))
    console.print("\n")

    while True:
        userInput: str = console.input(f"[deep_sky_blue1]{USER_NAME}:[/deep_sky_blue1] ")
        if userInput.lower() in EXIT_COMMANDS:
            console.print(f"[magenta3]{AI_ASSISTANT_NAME}:[/magenta3]", end = " ")
            console.print(Markdown(END_MESSAGE), end = "")
            break
            
        response: VerifyLLMResponseModel | str = GetAgentResponse(userInput)
        console.print(f"[magenta3]{AI_ASSISTANT_NAME}:[/magenta3]", end = " ")
        console.print(Markdown(response), end = "")

if __name__ == "__main__":
    main()