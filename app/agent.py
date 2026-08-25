import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq


load_dotenv()

async def main():

    client = MultiServerMCPClient(
        {
            "hospital": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport" : "streamable_http"
            }
        }
    )

    tools = await client.get_tools()

    llm = ChatGroq(model="openai/gpt-oss-120b")

    agent = create_react_agent(llm, tools)

    query = "Find patient P1001 and tell me about the drug aspirin"

    result = await agent.ainvoke({"messages": [{"role": "user", "content": query}]})

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())