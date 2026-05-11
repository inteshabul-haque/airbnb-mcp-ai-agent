"""Airbnb MCP Server with Conversation Memory."""

import sys
import os
import asyncio
import traceback

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage

from langchain_mcp_adapters.client import MultiServerMCPClient

from scripts import base_tools, prompts


# =========================================================
# Project Root Setup
# =========================================================

root_dir = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

sys.path.append(root_dir)


# =========================================================
# Load Environment Variables
# =========================================================

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")


# =========================================================
# Windows UTF-8 Support
# =========================================================

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


# =========================================================
# Gemini Model Initialization
# =========================================================

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,
    temperature=0.4
)


# =========================================================
# Global Chat Memory
# =========================================================

chat_history = []


# =========================================================
# Load MCP + Custom Tools
# =========================================================

async def get_tools():

    client = MultiServerMCPClient(
        {
            "airbnb": {
                "command": "npx",
                "args": [
                    "-y",
                    "@openbnb/mcp-server-airbnb",
                    "--ignore-robots-txt"
                ],
                "transport": "stdio",
            }
        }
    )

    mcp_tools = await client.get_tools()

    tools = mcp_tools + [
        base_tools.get_weather
    ]

    print(f"\nLoaded {len(tools)} tools successfully.\n")

    return tools


# =========================================================
# AI Agent Workflow
# =========================================================

async def hotel_search(query):

    global chat_history

    tools = await get_tools()

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=prompts.AIRBNB_PROMPT
    )

    # ======================================
    # SAVE USER MESSAGE
    # ======================================

    chat_history.append(
        HumanMessage(content=query)
    )

    # ======================================
    # RUN AGENT
    # ======================================

    result = await agent.ainvoke(
        {
            "messages": chat_history
        }
    )

    print("\n============= FULL RESULT =============\n")
    print(result)
    print("\n=======================================\n")

    # ======================================
    # EXTRACT RESPONSE
    # ======================================

    response_data = result["messages"][-1].content

    # MCP sometimes returns list format
    if isinstance(response_data, list):

        cleaned_response = []

        for item in response_data:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    cleaned_response.append(
                        item.get("text", "")
                    )

            else:
                cleaned_response.append(str(item))

        response = "\n".join(cleaned_response)

    else:
        response = str(response_data)

    # ======================================
    # SAVE AI RESPONSE TO MEMORY
    # ======================================

    chat_history.append(
        AIMessage(content=response)
    )

    print("\n============= CLEAN RESPONSE =============\n")
    print(response)
    print("\n==========================================\n")

    return response


# =========================================================
# Interactive CLI Chat
# =========================================================

async def ask():

    print("=" * 60)
    print(" Airbnb MCP AI Assistant ")
    print("=" * 60)

    print("\nType 'q' or 'quit' to exit.\n")

    while True:

        query = input("You: ").strip()

        if query.lower() in ["q", "quit"]:
            print("\nExiting chat mode.\n")
            break

        if not query:
            print("Please enter a valid question.\n")
            continue

        try:

            response = await hotel_search(query)

            print("\n============== AI RESPONSE ==============\n")
            print(response)
            print("\n=========================================\n")

        except Exception:

            print("\n=========== FULL ERROR ===========\n")

            traceback.print_exc()

            print("\n==================================\n")


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":

    asyncio.run(ask())