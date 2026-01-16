from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

load_dotenv()  # Load environment variables from .env file

class ResearchOutput(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")

parser = PydanticOutputParser(pydantic_object=ResearchOutput)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that gathers information to form a research report.
            Provide a concise summary, list of sources, and tools used for research.
            Ensure the output is in the specified format with no additional text.\n{format_instructions}
            Save the output to a file using the "save_tool" tool.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,  # Add your tools here
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("\nEnter your research query: \n\n")
raw_response = agent_executor.invoke({"query": query})

try:
    structured_output = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_output)
except Exception as e:
    print(f"Error parsing output: {e}")
    print("Raw output:", raw_response)