from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_classic.tools import Tool
from datetime import datetime
from json import JSONDecodeError
from json import loads
from textwrap import fill

def save_to_txt(data, filename: str = "report.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    
    if isinstance(data, str):
        try:
            data = loads(data)
        except (JSONDecodeError, TypeError):
            return f"Error: Invalid data format"
    
    summary = fill(data["summary"], width=200)
    formatted_text = f"""
--- Report generated on {timestamp}---

Topic: {data['topic']}

Summary:

{summary}

Sources: {data['sources']}

Tools Used: {data['tools_used']}

"""

    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_text)
    
    return f"Report saved"

save_tool = Tool(
    name="save_report",
    func=save_to_txt,
    description="Saves the provided data string to a text file with a timestamp.",
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for recent information on a given topic.",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)