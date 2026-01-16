from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_classic.tools import Tool
from datetime import datetime

def save_to_txt(data: str, filename: str = "report.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    formatted_text = f"--- Report generated on {timestamp} ---\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_text)
    
    return f"Report saved to {filename}"

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