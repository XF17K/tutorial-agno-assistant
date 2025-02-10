from agno.models.openai import OpenAIChat
from agno.models.deepseek import DeepSeek
from agno.agent import Agent

class LLMConfig:
    GPT_4O_MINI = OpenAIChat(
        id="gpt-4o-mini"
    )

    DEEPSEEK_R1_DISTILL_LLAMA_8B = DeepSeek(
        id="deepseek-r1-distill-llama-8b",
        base_url="http://192.168.1.10:1234/v1",
        api_key=""
    )

llm_model = LLMConfig.GPT_4O_MINI