from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import re

# Save to file function with a single string input
def save_to_txt(data: str, filename: str = "research_output.txt"):
    # Basic formatting: add line breaks after periods, question marks, and exclamation marks followed by a space
    formatted_text = re.sub(r'([.?!])\s+', r'\1\n\n', data.strip())
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"--- Research Output ---\nTimestamp: {timestamp}\n\n"
    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(header)
        f.write(formatted_text)
        f.write("\n\n")  # extra newline at end
    
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_to_txt",
    func=save_to_txt,
    description="Use this tool to save any data or result to a file. Input should be the data as a single string.",
)

# Search tool using DuckDuckGo
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

# Wikipedia tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
