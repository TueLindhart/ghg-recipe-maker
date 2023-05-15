from typing import Literal

from langchain import GoogleSearchAPIWrapper, GoogleSerperAPIWrapper, LLMChain
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain.chat_models import ChatOpenAI

from prompt_templates.co2_search_prompts import SEARCH_AGENT_PREFIX, SEARCH_AGENT_SUFFIX


def get_co2_google_search_agent(verbose: bool = False, search_type: Literal["google", "serper"] = "google"):
    if search_type == "google":
        search_chain = GoogleSearchAPIWrapper(k=10, search_engine="google")
    else:
        search_chain = GoogleSerperAPIWrapper(k=10, gl="dk")

    tools = [
        Tool(
            name="Search tool",
            func=search_chain.run,
            description="""Useful for finding out the kg CO2e / kg for an ingredient.""",
            # coroutine=search_chain.arun,
        ),
    ]

    en_prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=SEARCH_AGENT_PREFIX,
        suffix=SEARCH_AGENT_SUFFIX,
        input_variables=["input", "agent_scratchpad"],
    )

    llm_chain = LLMChain(
        llm=ChatOpenAI(temperature=0),  # type: ignore
        prompt=en_prompt,
    )

    tool_names = [tool.name for tool in tools]
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names)
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=verbose)

    return agent_executor
