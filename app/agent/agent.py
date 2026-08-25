import json
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

# from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

load_dotenv()

MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

SYSTEM_PROMPT = """You are a hospital assistant agent with access to 3 tools:
- get_patient: internal hospital DB, only for patient IDs like P1001-P1005
- search_drug: openFDA drug info lookup
- get_observations: external FHIR test server, for patient names and lab/vitals data

Rules for your answers:
- Be concise and clinical, not a full consultation note.
- Present data in a short table or bullet list, not long paragraphs.
- Do NOT give treatment recommendations, next-step clinical plans, or ask
  follow-up questions unless the user explicitly asks for clinical advice.
- Just report the facts returned by the tools, clearly formatted.
- If a tool returns an error, state it plainly — don't guess or fill in missing data.
"""


def _extract_tool_result(content):
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block["text"])
            else:
                texts.append(str(block))
        raw = "\n".join(texts)
    else:
        raw = content

    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw


async def run_agent(query: str):
    client = MultiServerMCPClient(
        {
            "hospital": {
                "url": MCP_SERVER_URL,
                "transport": "streamable_http",
            }
        }
    )

    tools = await client.get_tools()
    llm = ChatGroq(model="openai/gpt-oss-120b")
    agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

    result = await agent.ainvoke({"messages": [{"role": "user", "content": query}]})

    tool_calls = []
    final_answer = ""

    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                tool_calls.append(
                    {
                        "tool": tc["name"],
                        "arguments": tc["args"],
                        "result": None,
                    }
                )

        if msg.__class__.__name__ == "ToolMessage":
            for tc in tool_calls:
                if tc["result"] is None and tc["tool"] == msg.name:
                    tc["result"] = _extract_tool_result(msg.content)
                    break

        if msg.__class__.__name__ == "AIMessage" and msg.content:
            final_answer = msg.content

    return {
        "query": query,
        "tool_calls": tool_calls,
        "answer": final_answer,
    }
