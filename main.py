from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.openai import OpenAIEmbedder
from agno.document import Document
from agno.knowledge.document import DocumentKnowledgeBase
from agno.agent import Agent
from config import llm_model

# prepare infos

infos = [
    "XStudios was founded in Istanbul in 2050.",
    "The founder of XStudios is Scarlett.",
    "XStudios has published 14 games on the Steam platform.",
    "XStudios is publishing games on the computer platform.",
    "Cities where XStudios has offices: Istanbul (main headquarters), San Francisco, New York, London, Paris, Madrid, Rome.",
    "XStudios has 226 employees.",
]

# create vectorstore
vectorstore = LanceDb(
    table_name = "xstudios",
    uri = "db/lancedb",
    search_type = SearchType.vector,
    embedder = OpenAIEmbedder(id="text-embedding-3-small")
)

# convert infos to documents
documents = [Document(content=sentence) for sentence in infos]


# create knowledge base
knowledge_base = DocumentKnowledgeBase(
    path="tmp/lancedb2",
    vector_db = vectorstore,
    documents = documents,
)

# load knowledge base. If recreate is True, the knowledge base will be recreated. After first load, recreate should be False.
knowledge_base.load(recreate=True)

agent = Agent(
    model = llm_model,
    knowledge_base = knowledge_base,
    tools = [],
    add_references = True,
    search_knowledge = True,
    show_tool_calls= True,
    add_history_to_messages = True,
    debug_mode = True,
    markdown = True,
    system_message = """
    You are a helpful assistant that can answer questions.
    First, you will search the knowledge base for the answer.
    If you cannot find the answer, you will search the internet with tavily for the answer.
    """
)
