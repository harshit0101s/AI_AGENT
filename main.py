from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
import re

load_dotenv()

# Define structured output schema
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Language model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Output parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant. You **must use both the `search` and `wiki` tools** to gather data, even if you already know the answer.
            If the user query contains the word "save", you **must call the `save_to_txt` tool** with the final output.
            Format your response as a raw JSON object only, no code blocks or markdown. Match the format:\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Agent setup
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[search_tool, wiki_tool, save_tool],
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool, wiki_tool, save_tool],
    verbose=True,
    return_intermediate_steps=True,
)

# User input
query = input("What can I help you research? ")

# Run the agent
raw_response = agent_executor.invoke({"query": query})

# Extract output string and clean if it includes ```json formatting
raw_output = raw_response.get("output", "")
cleaned_output = re.sub(r"^```(?:json)?\n?", "", raw_output).strip("`\n ")

# Parse output into structured object
structured_response = parser.parse(cleaned_output)

save_message = save_tool(structured_response.summary)  # or pass any field you want saved
print(save_message)

# Print structured response
print("\n✅ Structured Output:")
print(structured_response)


