from agno.models.openai import OpenAIChat
from agno.models.deepseek import DeepSeek

# LLM configurations not currently supported by AGNO. Temporarily stored here for reference.
class LLMConfig:
    GPT_4O_MINI = OpenAIChat(
        id="gpt-4o-mini"
    )

    DEEPSEEK_R1_DISTILL_LLAMA_8B = DeepSeek(
        id="deepseek-r1-distill-llama-8b",
        base_url="http://192.168.1.10:1234/v1",
        api_key=""
    )

# Application Constants
AI_ASSISTANT_NAME = "Morganite AI"
USER_NAME = "User"
EXIT_COMMANDS = ["q", "x", "quit", "exit", "bye"]
LLM_MAX_ATTEMPTS = 1

# Information for vectorstore
INFOS = [
    "XStudios was founded in Istanbul in 2050.",
    "The founder of XStudios is Scarlett.",
    "XStudios has published 14 games on the Steam platform.",
    "XStudios is publishing games on the computer platform.",
    "Cities where XStudios has offices: Istanbul (main headquarters), San Francisco, New York, London, Paris, Madrid, Rome.",
    "XStudios has 226 employees.",
]

# Messages
WELCOME_MESSAGE = f"""
Welcome to {AI_ASSISTANT_NAME} Assistant!
You can type '{"', '".join(EXIT_COMMANDS)}' to exit.
"""

END_MESSAGE = f"""
Thank you for using {AI_ASSISTANT_NAME} Assistant!
Goodbye!
"""